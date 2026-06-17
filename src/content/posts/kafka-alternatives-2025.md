---
title: "Kafka 不再是唯一选择：2025 消息队列选型指南"
date: 2025-10-15T09:00:00+08:00
categories: ["分布式", "技术"]
description: "Redpanda、WarpStream、AutoMQ 等新玩家正在挑战 Kafka 的地位，消息队列的格局正在变化。"
---

Kafka 统治消息队列领域十多年了，但最近出现了很多有意思的替代品。

## Redpanda

- 用 C++ 重写的 Kafka 兼容实现
- 不需要 ZooKeeper（内置 Raft）
- 吞吐量比 Kafka 高 2-5 倍
- 完全兼容 Kafka API，迁移成本低

## WarpStream

- 基于对象存储（S3 兼容）的消息队列
- 无需本地磁盘，数据直接写 S3
- 零运维：不需要管理 broker
- 延迟稍高（P99 ~100ms），但成本极低

## AutoMQ

- 国内团队作品，基于 S3 Stream 架构
- 兼容 Kafka 协议
- 自动弹性伸缩
- 存算分离，成本比自建 Kafka 低 50%

## 选型建议

- 已有 Kafka，不想动 → 继续用
- 新项目，自建 → 可以考虑 Redpanda
- 云原生，不想运维 → WarpStream / AutoMQ
- 对延迟极度敏感 → Kafka (本地磁盘版本)

消息队列的江湖不会只有 Kafka 一家独大了。