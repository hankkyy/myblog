---
title: "Doris vs ClickHouse：OLAP 数据库学习对比"
date: 2025-04-10T15:00:00+08:00
categories: ["数据库", "技术"]
description: "学习对比 Doris 和 ClickHouse 的架构差异、性能特点和适用场景。"
---

最近在学习 OLAP 数据库，把 Doris 和 ClickHouse 做了一个对比。

## 架构差异

**ClickHouse：**
- 纯列存，MergeTree 引擎很强大
- 单表聚合性能极致
- JOIN 能力比较弱
- 俄罗斯 Yandex 开源

**Doris：**
- MPP + 列存架构
- 标准 SQL 兼容性好
- JOIN 能力强
- 百度开源，国内社区活跃

## 性能对比

- 单表聚合：ClickHouse 略快
- 多表 JOIN：Doris 更强
- 高并发查询：Doris 的 Unique Key 模型有优势
- 数据更新：Doris 原生支持 Upsert

## 学习建议

两个都是优秀的 OLAP 引擎。如果想入门数据分析，Doris 的 SQL 兼容性更好，上手更快。如果做纯日志分析，ClickHouse 的单表性能更极致。

可以根据业务场景选择，或者两个都学，理解它们的架构设计思想。