---
title: "Spring Boot + Redis 缓存实战：从注解到分布式锁"
date: 2026-05-30T16:00:00+08:00
categories: ["技术"]
description: "Spring Cache 抽象、Redis 序列化、缓存穿透/击穿/雪崩解决方案"
---

缓存是后端性能优化的第一道防线。

## Spring Cache 注解

```java
// 最简单的方式
@Cacheable(value = "users", key = "#id")
public User getUser(Long id) {
    return userMapper.selectById(id);
}

@CacheEvict(value = "users", key = "#user.id")
public void updateUser(User user) {
    userMapper.updateById(user);
}

@CachePut(value = "users", key = "#user.id")
public User saveUser(User user) {
    userMapper.insert(user);
    return user;
}
```

## Redis 序列化配置

默认 JDK 序列化可读性差，改成 JSON：

```java
@Bean
public RedisCacheConfiguration cacheConfiguration() {
    return RedisCacheConfiguration.defaultCacheConfig()
        .serializeValuesWith(
            RedisSerializationContext.SerializationPair
                .fromSerializer(new GenericJackson2JsonRedisSerializer())
        )
        .entryTtl(Duration.ofMinutes(30));
}
```

## 缓存三大问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **穿透** | 查不存在的数据，每次都到 DB | 布隆过滤器 / 缓存空值 |
| **击穿** | 热点 key 过期，大量请求打到 DB | 互斥锁 / 永不过期 |
| **雪崩** | 大量 key 同时过期 | 过期时间加随机值 |

## 分布式锁实现

```java
public String deductStock(String productId) {
    String lockKey = "lock:stock:" + productId;
    String lockValue = UUID.randomUUID().toString();
    
    // SET NX EX：获取锁，30秒过期
    Boolean locked = redisTemplate.opsForValue()
        .setIfAbsent(lockKey, lockValue, 30, TimeUnit.SECONDS);
    
    if (Boolean.FALSE.equals(locked)) {
        throw new BusyException("系统繁忙，请稍后重试");
    }
    try {
        // 扣库存逻辑
        return "success";
    } finally {
        // Lua 脚本保证原子性释放锁
        String script = "if redis.call('get', KEYS[1]) == ARGV[1] " +
            "then return redis.call('del', KEYS[1]) else return 0 end";
        redisTemplate.execute(new DefaultRedisScript<>(script, Long.class),
            Collections.singletonList(lockKey), lockValue);
    }
}
```

> 缓存不难，难的是缓存失效那一刻。
