---
title: "Redis Cluster 入门：从单机到集群的那些坑"
date: 2025-06-20T14:00:00+08:00
categories: ["技术", "分布式"]
description: "学习 Redis Cluster 的部署、扩容和常见故障处理，总结学习过程中踩过的坑。"
---

最近在学习 Redis Cluster，搭了一套 3 主 3 从的环境，过程中踩了不少坑。

## 搭建过程

Redis Cluster 最少需要 6 个节点（3 主 3 从），用 `redis-cli --cluster create` 一条命令就能创建。关键是理解槽位（slot）的概念：整个集群有 16384 个哈希槽，每个主节点负责一部分。

## 扩容时的问题

手动做槽位迁移，如果在业务高峰期迁移，Redis 会返回 MOVED 错误。

解决办法：选择低峰期迁移，并且用逐槽迁移的方式。

## 大 Key 的坑

一个 Hash 存了大量数据，迁移时非常慢。最好的做法是拆分大 Key，比如 `user:{id}:info` 而不是一个超大的 `users` hash。

## 脑裂问题

如果网络抖动导致主节点被孤立，Cluster 自动选主，可能出现两个主同时写入的情况。

解决办法：配置 `min-slaves-to-write 1`，确保主节点至少有一个从节点正常时才接受写入。

Redis Cluster 比单机 Redis 复杂不少，但对于需要高可用的场景来说值得学习。