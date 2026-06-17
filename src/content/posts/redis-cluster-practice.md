---
title: "Redis Cluster 生产环境踩坑记录：从 3 主 3 从到 9 主 9 从"
date: 2025-06-20T14:00:00+08:00
categories: ["技术", "分布式"]
description: "总结 Redis Cluster 在生产环境中的扩容、故障转移和性能调优经验。"
---

记录一下 Redis Cluster 在生产环境踩过的坑。

## 背景

公司核心业务依赖 Redis 做缓存和分布式锁。最开始是 3 主 3 从的 Cluster 架构，随着流量增长逐步扩容到 9 主 9 从。

## 踩过的坑

### 1. 槽位迁移导致超时

扩容时需要迁移 slot（哈希槽）。如果在迁移过程中有大量请求，Redis 会返回 MOVED 错误。

**解决方案**：选择低峰期（凌晨 3 点）做迁移，并且使用 `CLUSTER SETSLOT node_id MIGRATING` 做逐槽迁移。

### 2. 大 Key 问题

一个 Hash 存了 100 万条数据，导致迁移时非常慢。

**解决方案**：大 Key 拆分，比如 `user:{user_id}:info` 而不是一个大的 `users` hash。

### 3. 脑裂

网络抖动导致一个主节点被"孤立"，Cluster 重新选主。原来的主节点恢复后变成两个主节点同时写入，数据不一致。

**解决方案**：配置 `min-slaves-to-write 1`，确保主节点至少有一个从节点正常时才接受写入。

## 监控要点

- `cluster_state`：必须是 ok
- `cluster_slots_ok`：所有槽位必须被覆盖
- 每个主节点的内存使用率（避免不均衡）

Redis Cluster 虽然复杂，但稳定性确实比 Sentinel + 主从好很多。