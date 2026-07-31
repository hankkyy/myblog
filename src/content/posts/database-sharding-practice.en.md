---
lang: en
title: "MySQL Sharding Study Notes: From Single Database to Sharding"
date: 2025-08-15T11:00:00+08:00
categories: ["Database", "Technology"]
description: "Learn the core concepts of database sharding, shard key selection strategies, and common pitfalls, suitable for beginners."
---

I've been studying database sharding solutions recently, and here's my summary.

## Why Sharding Is Needed

When a table's data volume exceeds tens of millions of rows, a single database hits performance bottlenecks. Although indexes help with queries, the B+Tree depth increases, and the buffer pool can no longer hold all the data.

## How to Choose a Shard Key

This is the most critical step. Common choices:
- User ID: Data for the same user resides in the same shard, making user-level queries fast
- Order ID: Distributes by order number, but querying all orders for a user requires cross-shard access
- Time: Partition by month or year, suitable for log-type data

## Common Approaches

Use ShardingSphere or implement routing logic yourself:

1. First, plan how many databases and how many tables per database
2. Determine the sharding algorithm (modulo, hash, range)
3. During data migration, use dual-write plus gray release switching
4. Avoid cross-shard queries whenever possible; if needed, use Elasticsearch as an index

Sharding is not a silver bullet—avoid it if you can. But as data grows, you'll eventually have to face it.