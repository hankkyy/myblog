---
title: "实时计算入门：Flink 和 Spark Structured Streaming 该怎么选？"
date: 2026-02-10T13:00:00+08:00
categories: ["技术", "分布式"]
description: "学习 Flink 和 Spark Structured Streaming 的区别，了解各自的适用场景。"
---

最近在看实时计算相关的资料，对比了 Flink 和 Spark Structured Streaming。

## Flink

- 真正的流处理，每条数据独立处理
- 状态管理很强大
- 阿里双十一验证过的技术
- 学习曲线比较陡（Watermark、Window 概念多）

## Spark Structured Streaming

- 底层是微批次处理，延迟稍高
- SQL 表达能力很强
- 和 Spark 生态（MLlib、GraphX）集成好
- 批流一体，同一套代码

## 选型思路

- 纯实时场景、毫秒级延迟要求 → Flink
- 批流混合、团队有 Spark 经验 → Spark
- 想深入学习流处理原理 → 先学 Flink
- 公司有 Hadoop/Hive 生态 → Spark 更自然

对于学习来说，建议两个都了解一下，理解它们的设计哲学区别更重要。