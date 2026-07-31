---
lang: en
title: "Spring Boot 3 + Virtual Threads: Performance Testing and Pitfalls"
date: 2026-06-12T11:00:00+08:00
categories: ["Technology"]
description: "Real-world performance of Java 21 Virtual Threads in Spring Boot 3, benchmarked under 1000 concurrent connections"
---

Java 21's Virtual Threads are the culmination of Project Loom. Spring Boot 3.2 officially supports them. I recently ran tests in my project.

## Configuration

```yaml
# application.yml
spring:
  threads:
    virtual:
      enabled: true  # Spring Boot 3.2+
```

Or programmatically:

```java
@Bean
public TomcatProtocolHandlerCustomizer<?> protocolHandlerVirtualThreadExecutor() {
    return protocolHandler -> {
        protocolHandler.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
    };
}
```

## Test Environment

- CPU: Apple M2 Pro
- Memory: 16GB
- Spring Boot 3.2.1 + Java 21
- Benchmark tool: wrk, 1000 concurrent connections, 60s

## Test Results

### Scenario 1: Pure Blocking I/O (100ms sleep simulating DB)

| Thread Model | QPS | P99 Latency | Max Threads |
|--------------|-----|-------------|-------------|
| Platform Threads (200) | 1,980 | 580ms | 200 (pool exhausted) |
| Virtual Threads | **19,500** | 105ms | ~10,000 |

**10x QPS improvement**. Virtual threads don't consume platform threads while blocked.

### Scenario 2: CPU-Intensive (Fibonacci)

| Thread Model | QPS | CPU Usage |
|--------------|-----|-----------|
| Platform Threads | 45 | 85% |
| Virtual Threads | 43 | 82% |

Nearly identical. **Virtual threads don't speed up computation — they only solve blocking.**

## Pitfalls Encountered

### 1. Don't use synchronized inside virtual threads

```java
// ❌ Wrong: synchronized pins the carrier thread
synchronized (this) {
    Thread.sleep(1000);
}

// ✅ Correct: use ReentrantLock
lock.lock();
try {
    Thread.sleep(1000);
} finally {
    lock.unlock();
}
```

### 2. Connection pools need to be larger

Originally, the Tomcat thread pool had 200 threads and the MySQL connection pool was also set to 200. After switching to virtual threads, you might have 10,000 concurrent requests, so the connection pool needs to scale accordingly. I recommend starting with HikariCP + `maximumPoolSize=500`.

### 3. ThreadLocal memory leaks

With massive numbers of virtual threads, every ThreadLocal consumes memory. Recommendation:

```java
// Manually clean up after use
threadLocal.remove();
```

## When Should You Use Virtual Threads?

| Scenario | Recommendation |
|----------|----------------|
| Heavy blocking I/O (HTTP/DB) | ✅ Strongly recommended |
| Pure computation | ❌ No benefit |
| Existing async code (WebFlux) | ⚠️ Can simplify but not necessarily faster |
| Heavy ThreadLocal usage | ⚠️ Watch out for memory |

> In one sentence: **Virtual threads make the "one request, one thread" model viable again. MVC no longer fears high concurrency.**

---

**References:**

- [OpenJDK — JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [Spring Boot 3.2 Documentation](https://docs.spring.io/spring-boot/)