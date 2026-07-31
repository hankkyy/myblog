---
lang: en
title: "Redis Cluster Getting Started: Pitfalls from Single-Node to Cluster"
date: 2025-06-20T14:00:00+08:00
categories: ["Technology", "Distributed Systems"]
description: "Learn about Redis Cluster deployment, scaling, and common troubleshooting, summarizing the pitfalls encountered during the learning process."
---

I've been learning Redis Cluster recently and set up a 3-master 3-slave environment, hitting quite a few pitfalls along the way.

## Setup Process

Redis Cluster requires a minimum of 6 nodes (3 masters and 3 slaves), and you can create it with a single command using `redis-cli --cluster create`. The key is understanding the concept of slots: the entire cluster has 16,384 hash slots, with each master node responsible for a portion of them.

## Issues During Scaling

When manually migrating slots, if you do it during peak business hours, Redis will return MOVED errors.

Solution: Choose off-peak hours for migration and migrate slot by slot.

## The Big Key Pitfall

A single Hash storing a large amount of data makes migration very slow. The best practice is to split large keys, such as `user:{id}:info` instead of one oversized `users` hash.

## Split-Brain Problem

If network jitter causes a master node to become isolated, Cluster will automatically elect a new master, potentially resulting in two masters accepting writes simultaneously.

Solution: Configure `min-slaves-to-write 1` to ensure a master node only accepts writes when it has at least one healthy slave.

Redis Cluster is significantly more complex than single-node Redis, but it's worth learning for scenarios that require high availability.