---
title: "Doris vs ClickHouse：2025 年 OLAP 数据库怎么选？"
date: 2025-04-10T15:00:00+08:00
categories: ["数据库", "技术"]
description: "从架构、性能、SQL兼容性、运维成本等维度对比 Doris 和 ClickHouse。"
---

团队在评估 OLAP 数据库，把 Doris 和 ClickHouse 做了个全面对比。

## 架构对比

**ClickHouse：**
- 纯列存，MergeTree 引擎
- 单表性能极致
- JOIN 能力弱（不适合星型模型）
- 物化视图功能有限

**Doris：**
- 列存 + MPP 架构
- 标准 SQL 支持好
- JOIN 能力强（支持 Broadcast/Shuffle Join）
- 物化视图 + Rollup 灵活

## 性能

- 单表聚合：ClickHouse 略优（10-20% 优势）
- 多表 JOIN：Doris 优（2-5 倍优势）
- 高并发点查：Doris 优（支持主键索引）
- 数据更新：Doris 优（Unique Key 模型天然支持 Upsert）

## 运维

- ClickHouse：单机部署简单，但集群配置复杂。ZooKeeper 依赖是痛点。
- Doris：FE + BE 架构清晰，自动均衡，运维相对友好。

## 结论

- 纯日志分析 / 单表聚合场景 → ClickHouse
- 需要 JOIN / 报表 / 实时写入 → Doris
- 团队有 Java 经验（Doris 基于 Java）→ Doris
- 团队有 C++ 经验（ClickHouse 基于 C++）→ ClickHouse

最终我们选了 Doris，因为业务场景更复杂，Join 需求多。