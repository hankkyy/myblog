---
title: "Spring Boot 3 + Virtual Threads：性能测试与踩坑记录"
date: 2026-06-12T11:00:00+08:00
categories: ["技术"]
description: "Java 21 Virtual Threads 在 Spring Boot 3 中的实际表现，1000并发下的对比测试"
---

Java 21 的 Virtual Threads（虚拟线程）是 Project Loom 的最终成果。Spring Boot 3.2 开始正式支持。我最近在项目里做了测试。

## 配置方式

```yaml
# application.yml
spring:
  threads:
    virtual:
      enabled: true  # Spring Boot 3.2+
```

或者在代码里：

```java
@Bean
public TomcatProtocolHandlerCustomizer<?> protocolHandlerVirtualThreadExecutor() {
    return protocolHandler -> {
        protocolHandler.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
    };
}
```

## 测试环境

- CPU: Apple M2 Pro
- 内存: 16GB
- Spring Boot 3.2.1 + Java 21
- 测试工具: wrk, 1000 并发连接, 60s

## 测试结果

### 场景一：纯阻塞 I/O (sleep 100ms 模拟 DB)

| 线程模型 | QPS | P99 延迟 | 最大线程数 |
|----------|-----|----------|------------|
| 平台线程 (200) | 1,980 | 580ms | 200 (池满) |
| 虚拟线程 | **19,500** | 105ms | ~10,000 |

**10 倍 QPS 提升**。虚拟线程不会被阻塞消耗平台线程。

### 场景二：计算密集型 (斐波那契)

| 线程模型 | QPS | CPU 使用率 |
|----------|-----|------------|
| 平台线程 | 45 | 85% |
| 虚拟线程 | 43 | 82% |

几乎一样。**虚拟线程不加速计算，只解决阻塞问题。**

## 踩过的坑

### 1. 不要在虚拟线程里用 synchronized

```java
// ❌ 错误：synchronized 会 pin 住载体线程
synchronized (this) {
    Thread.sleep(1000);
}

// ✅ 正确：用 ReentrantLock
lock.lock();
try {
    Thread.sleep(1000);
} finally {
    lock.unlock();
}
```

### 2. 连接池要配大

原来 Tomcat 线程池 200 个，MySQL 连接池也配 200。换成虚拟线程后，可能有 10,000 个并发请求，连接池需要相应调整。建议用 HikariCP + `maximumPoolSize=500` 起步。

### 3. ThreadLocal 内存泄漏

虚拟线程数量巨大，每个 ThreadLocal 都占内存。建议：

```java
// 用完手动清理
threadLocal.remove();
```

## 什么时候该用虚拟线程？

| 场景 | 建议 |
|------|------|
| 大量阻塞 I/O (HTTP/DB) | ✅ 强烈推荐 |
| 纯计算 | ❌ 没用 |
| 已有异步代码 (WebFlux) | ⚠️ 可以简化但不一定更快 |
| 大量 ThreadLocal | ⚠️ 注意内存 |

> 一句话：**虚拟线程让「一个请求一个线程」模型重新变得可行**。MVC 从此不怕高并发。
