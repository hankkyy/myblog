---
lang: en
title: "The Three Generations of Distributed Locks: From Redis to Etcd to Lock-Free Design"
date: 2025-03-15T10:00:00+08:00
categories: ["Distributed Systems", "Technology"]
description: "An in-depth analysis of three distributed lock implementations and their pros and cons, including the Redlock controversy and Etcd's lease mechanism."
---

Distributed locks may seem simple, but they are full of pitfalls.

## First Generation: Redis Distributed Lock

```java
// The most common implementation
String lockKey = "order:" + orderId;
boolean locked = redis.set(lockKey, uuid, "NX", "PX", 30000);
```

Problems:
1. The lock expiration time is hard to set — if it's too short, the lock auto-releases before the business logic finishes; if it's too long, you have to wait a long time if the process crashes
2. The lock can be lost during master-slave failover

Martin Kleppmann's famous "Redlock is unsafe" article has led many people to avoid using Redis for distributed locks to this day.

## Second Generation: Etcd/Consul Distributed Lock

Leveraging Etcd's Lease mechanism:
- The client renews the lease periodically
- The lease automatically expires if the client crashes
- Raft ensures consistency

The downside is that performance is not as good as Redis, and Etcd's bottleneck lies in write throughput.

## Third Generation: Lock-Free Design

The best distributed lock is one that doesn't require a distributed lock at all.

Some approaches:
- Idempotency design (e.g., database unique keys + state machines)
- Optimistic locking (version numbers/CAS)
- Message queues for serialized processing
- Database row-level locks (e.g., `SELECT ... FOR UPDATE`)

## My Recommendation

If you can use database row-level locks, don't use distributed locks; if you can use a lock-free design, don't lock at all. When distributed locks are truly necessary, choose between Redis (accepting occasional failures) or Etcd (accepting lower performance) based on your business's tolerance.