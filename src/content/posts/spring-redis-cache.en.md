---
lang: en
title: "Spring Boot + Redis Cache in Practice: From Annotations to Distributed Locks"
date: 2026-05-30T16:00:00+08:00
categories: ["Technology"]
description: "Spring Cache abstraction, Redis serialization, solutions for cache penetration/breakdown/avalanche"
---

Caching is the first line of defense for backend performance optimization.

## Spring Cache Annotations

```java
// The simplest way
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

## Redis Serialization Configuration

The default JDK serialization has poor readability, so switch to JSON:

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

## Three Major Cache Problems

| Problem | Cause | Solution |
|---------|-------|----------|
| **Penetration** | Querying non-existent data, hitting the DB every time | Bloom filter / Cache null values |
| **Breakdown** | Hot key expires, massive requests hit the DB | Mutex lock / Never expire |
| **Avalanche** | A large number of keys expire at the same time | Add random values to expiration times |

## Distributed Lock Implementation

```java
public String deductStock(String productId) {
    String lockKey = "lock:stock:" + productId;
    String lockValue = UUID.randomUUID().toString();
    
    // SET NX EX: acquire the lock, 30-second expiration
    Boolean locked = redisTemplate.opsForValue()
        .setIfAbsent(lockKey, lockValue, 30, TimeUnit.SECONDS);
    
    if (Boolean.FALSE.equals(locked)) {
        throw new BusyException("System is busy, please try again later");
    }
    try {
        // Stock deduction logic
        return "success";
    } finally {
        // Lua script ensures atomic lock release
        String script = "if redis.call('get', KEYS[1]) == ARGV[1] " +
            "then return redis.call('del', KEYS[1]) else return 0 end";
        redisTemplate.execute(new DefaultRedisScript<>(script, Long.class),
            Collections.singletonList(lockKey), lockValue);
    }
}
```

> Caching is not hard; what's hard is the moment a cache expires.