---
title: "2026 年实时计算选型：Flink 还是 Spark Structured Streaming？"
date: 2026-02-10T13:00:00+08:00
categories: ["技术", "分布式"]
description: "对比 Flink 和 Spark Streaming 在 2026 年的技术现状、性能表现和生态发展。"
---

最近部门在选实时计算引擎，做了 Flink 和 Spark Structured Streaming 的对比调研。

## Flink

**优势：**
- 真正的流处理（每条数据独立处理）
- 状态管理成熟（RocksDB 后端）
- Checkpoint/Savepoint 机制可靠
- 阿里大规模验证（双十一峰值数十亿/秒）

**劣势：**
- 学习曲线陡峭（Watermark、Window 概念多）
- SQL 功能不如 Spark 完善
- 批处理性能一般

## Spark Structured Streaming

**优势：**
- SQL 表达能力强
- 批流一体（同一套代码）
- 生态成熟（MLlib、GraphX）
- Delta Lake 集成无缝

**劣势：**
- 微批次架构导致延迟下限较高（100ms+）
- 状态管理不如 Flink 灵活
- 大规模集群稳定性有待验证

## 选型建议

- 纯实时场景（毫秒级延迟要求）：选 Flink
- 批流混合（既有实时又有离线）：选 Spark + Delta Lake
- 团队有 Java/Flink 经验：选 Flink
- 团队有 Spark/Hive 经验：选 Spark

我们最终选了 Flink，因为业务对延迟要求很高。