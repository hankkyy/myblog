---
lang: en
title: "Getting Started with Apache Pulsar: What Makes the Next-Generation Message Queue Different?"
date: 2025-02-22T15:00:00+08:00
categories: ['Distributed Systems', 'Technology']
description: "Learn about Pulsar's architecture design—storage and compute separation, tiered storage, multi-tenancy, and its core differences from Kafka."
---

Apache Pulsar is known as the "next-generation message queue," and its biggest difference from Kafka lies in its architecture.

## Storage and Compute Separation

In Kafka, data is stored on the Broker's local disk, meaning the Broker handles both compute and storage. Scaling requires considering both compute and storage simultaneously.

Pulsar separates compute (Broker) from storage (BookKeeper):
- Broker: Stateless, responsible only for message routing and serving
- BookKeeper: Handles persistent storage

This means you can scale Brokers (to increase throughput) or BookKeepers (to increase storage) independently, without affecting each other.

## Multi-Tenancy

Pulsar natively supports multi-tenancy: a single cluster can serve multiple teams/business lines with complete isolation between tenants. Kafka relies mainly on naming conventions to distinguish between them.

## Tiered Storage

Pulsar can automatically migrate cold data to cheap storage (S3, HDFS), while keeping hot data in BookKeeper. This is highly useful for long-term storage scenarios (such as audit logs and compliance data).

## When to Choose Pulsar

- You need to serve multiple tenants within the same cluster
- Messages need long-term storage
- Your team has dedicated operations staff (Pulsar's operational complexity is higher than Kafka's)

Kafka remains the de facto standard, but Pulsar is indeed more suitable in specific scenarios.

---

**References:**

- [Apache Pulsar Official Documentation](https://pulsar.apache.org/)