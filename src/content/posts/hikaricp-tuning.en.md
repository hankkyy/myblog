---
lang: en
title: "Backend Performance Optimization: A Practical Guide to Database Connection Pool Tuning"
date: 2026-06-17
categories: ["Technology", "Database"]
description: "A detailed guide to HikariCP connection pool parameters and performance testing, from default settings to production-optimal configuration."
---

The connection pool is one of the most overlooked performance bottlenecks in backend systems. Many teams go live with Spring Boot's default parameters, only to encounter connection timeouts and thread blocking during traffic spikes.

This article documents my recent connection pool tuning process, from identifying the problem to the final configuration, complete with actual load test data.

## Why Tune the Connection Pool

Spring Boot 2.x uses HikariCP by default, and its default configuration is perfectly adequate for low-concurrency scenarios. However, as QPS climbs, the default `maximumPoolSize=10` quickly becomes a bottleneck.

A typical symptom: after request volume increases, API response times suddenly jump from tens of milliseconds to hundreds of milliseconds or even seconds—not because SQL queries have slowed down, but because threads are waiting for connections.

## Key Parameters

HikariCP has several critical parameters you need to understand:

**maximumPoolSize** — The maximum number of connections in the pool. Default is 10. For production, a good starting point is `CPU cores * 2 + 1`, adjusted based on actual load.

**minimumIdle** — The minimum number of idle connections maintained in the pool. By default, it equals `maximumPoolSize`, meaning all connections are created at startup. If you don't need pre-warming, you can set it lower.

**connectionTimeout** — The maximum time (in milliseconds) to wait for a connection. The default of 30 seconds is too long; I recommend 3-5 seconds so requests fail fast instead of blocking indefinitely.

**idleTimeout** — The maximum time an idle connection can remain in the pool. Default is 10 minutes; keeping it or slightly reducing it is recommended.

**maxLifetime** — The maximum lifetime of a connection. Default is 30 minutes, and it should be shorter than the database's connection timeout.

**leakDetectionThreshold** — The threshold for connection leak detection. For development, 10 seconds is recommended; for production, set it to 0 (disabled) to avoid additional overhead.

## A Real-World Case Study

We had a service running with default settings and `maximumPoolSize=10`. Initially, with a few hundred thousand requests per day, everything was fine. But when business volume grew to nearly one million QPS, monitoring showed:

- Database connections were consistently capped at 10
- API P99 latency skyrocketed from 50ms to over 2 seconds
- HikariCP logs were flooded with `Connection is not available` warnings

Analysis revealed that each request required an average of 15ms of database operation time. With 10 connections, the theoretical throughput was `1000ms / 15ms * 10 ≈ 666` requests per second. But in practice, network latency and transaction waits added to the overhead.

The adjusted configuration:

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 30
      minimum-idle: 10
      connection-timeout: 5000
      idle-timeout: 600000
      max-lifetime: 1800000
      leak-detection-threshold: 0
```

After the adjustment, P99 latency dropped to under 200ms, and API success rates recovered to 99.99%.

## How to Determine the Right Connection Count

A simple formula:

```
Connections ≈ (QPS × Average Query Time) + Buffer
```

For example, with QPS of 1000 and an average query time of 20ms:

```
Connections = (1000 × 0.02) + Buffer = 20 + 5~10 = 25~30
```

But this is just a theoretical value. In practice, you also need to consider:

- The database server's `max_connections` limit
- If multiple service instances share the same database, the connection count needs to be divided among them
- How long connections are held during transactions

## Don't Over-Tune

More connections isn't always better. Each connection consumes database memory and CPU resources. MySQL's default `max_connections=151` means that if 5 instances each open 50 connections, you've already exceeded the limit.

Generally speaking:

- Fewer than 50 connections suits most scenarios
- 50–100 requires confirming the database can handle it
- 100+ usually indicates an architectural issue—consider introducing caching or read-write splitting

## Summary

Key takeaways for connection pool tuning:

1. Understand what the default parameters mean before making changes
2. Base decisions on monitoring data, not intuition
3. Set `connectionTimeout` shorter to allow the system to fail fast
4. Match connection count with database capacity
5. Always validate with load testing after tuning

Connection pool tuning is one of the simplest and highest-ROI performance optimizations. Spending half an hour adjusting parameters can save days of troubleshooting later.