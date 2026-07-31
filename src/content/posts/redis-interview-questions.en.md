---
lang: en
title: "Redis High-Frequency Interview Questions: What's the Difference Between Cache Penetration, Avalanche, and Breakdown?"
date: 2025-02-28T14:00:00+08:00
categories: ['Technology']
description: "Clarify the three most commonly confused concepts in Redis interviews, with solutions and code examples."
---

These three terms are almost guaranteed to come up in interviews, and many people can't tell them apart.

## Cache Penetration

**Phenomenon**: The queried data doesn't exist in the database either, so naturally there's no cache. Every request hits the database directly.

**Solutions**:
1. Bloom filter: Pre-store all potentially queried keys in a Bloom filter, and directly filter out non-existent ones
2. Cache empty objects: Even if nothing is found, cache a null value with a short expiration time

## Cache Breakdown

**Phenomenon**: A hot key expires, and a large number of concurrent requests hit the database at the same time.

**Solutions**:
1. Mutex lock: The first request queries the database and updates the cache, while other requests wait
2. Never expire: Don't set an expiration time for hot data, update it asynchronously instead

## Cache Avalanche

**Phenomenon**: A large number of keys expire simultaneously, and all requests hit the database.

**Solutions**:
1. Add random values to expiration times: Avoid large batches expiring at the same time
2. Multi-level caching: Local cache + Redis + database
3. Rate limiting and degradation: Implement service degradation when the database can't handle the load

## How to Remember

- **Penetration**: Data doesn't exist at all → Bloom filter
- **Breakdown**: Hot key expires → Mutex lock
- **Avalanche**: Large number of keys expire simultaneously → Random expiration times

Remember the differences between these three scenarios and their solutions, and you'll be halfway to acing the Redis part of your interview.