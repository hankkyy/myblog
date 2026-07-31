---
lang: en
title: "CAP Theorem Interview Deep Dive: You Can Only Pick Two, But Reality Is More Complex"
date: 2025-08-20T09:00:00+08:00
categories: ['Distributed Systems', 'Technology']
description: "Explaining the CAP theorem with real database examples, especially why P is not optional and the CP vs AP trade-off."
---

The CAP theorem is a must-know topic in distributed systems interviews.

## What is CAP

- **C (Consistency)**: All nodes see the same data at the same time
- **A (Availability)**: Every request receives a non-error response
- **P (Partition Tolerance)**: The system continues to operate despite network failures

## You Can Only Pick Two—But You Actually Have No Choice

The most misunderstood aspect of CAP: **P is not optional**. In a distributed system, network partitions can happen at any time. So in reality, you can only choose between CP or AP.

## Real-World Examples of CP vs AP

**CP systems (sacrificing availability for consistency)**:
- ZooKeeper: When the Leader goes down, a new election is required, during which the system is unavailable
- Etcd: Like ZooKeeper, based on Raft
- HBase: Strong consistency

**AP systems (sacrificing consistency for availability)**:
- Eureka: You can still query even if a service is down (you might get stale data)
- Cassandra: Eventual consistency
- DynamoDB: Eventually consistent by default

## It's All About Trade-offs

No system can satisfy all three simultaneously. CAP doesn't tell you "how to design a perfect system"—it tells you that "every technology choice involves a trade-off."

## Interview Script

> The CAP theorem tells us: in a distributed system, network partitions are inevitable. When a partition occurs, you must choose between consistency (C) and availability (A). For example, ZooKeeper is CP—during a network failure, it would rather be unavailable than return stale data. Eureka is AP—it would rather return stale data than compromise availability.

The key is to provide examples. Memorizing definitions alone won't help. If you can explain why ZooKeeper is CP and why Eureka is AP, interviewers will take notice.

---

**References:**

- [Eric Brewer — CAP Theorem (PODC 2000)](https://dl.acm.org/)