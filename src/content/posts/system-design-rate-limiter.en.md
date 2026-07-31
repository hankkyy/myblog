---
lang: en
title: "System Design Interview: Designing an API Rate Limiter"
date: 2026-01-25T10:00:00+08:00
categories: ['System Design', 'Technology']
description: "From token bucket to sliding window, break down the core ideas behind rate limiting algorithms and implementation approaches for distributed rate limiting."
---

API rate limiting is a fundamental capability every backend system needs. In interviews, you're often asked to design a rate limiter.

## Requirements

- Limit the request frequency per user/API Key
- For example: maximum 100 requests per minute
- Return 429 Too Many Requests when the limit is exceeded
- Need to support distributed deployment

## Common Algorithms

### Fixed Window

Divide time into fixed windows (e.g., per minute), with each window counting independently. Simple but has a problem—at window boundaries, you can send 2x the requests (last second of the previous minute + first second of the current minute).

### Sliding Window Log

Record the timestamp of each request and query the number of requests within the last N seconds. Accurate but consumes significant memory.

### Sliding Window Counter

Combine the request count from the previous window with weighted calculation. Can be implemented using Redis `ZSET`.

### Token Bucket (Most Commonly Used)

Add tokens to the bucket at a fixed rate (e.g., 10 per second). When a request arrives, take a token—if one is available, it passes; if not, it's rejected. The bucket has a capacity limit, allowing for a certain amount of burst traffic.

## Implementation

```java
// Implement token bucket using Redis
String key = "rate_limit:" + userId;
long now = System.currentTimeMillis();
long tokens = redis.incr(key);
redis.expire(key, 60); // 60-second window

if (tokens > 100) return 429;
// Process the request...
```

## Distributed Rate Limiting

When deployed across multiple nodes, you need a shared counter—use Redis to solve this. However, Redis itself can become a bottleneck. Solutions:
- Two-tier approach: local rate limiting + global rate limiting
- Coarse-grained local limiting (e.g., 1000/s per node), strict global limiting (e.g., 5000/s overall)

## Interview Key Points

You must mention the difference between the token bucket and sliding window algorithms. Being able to describe the two-tier approach for distributed rate limiting is a plus.