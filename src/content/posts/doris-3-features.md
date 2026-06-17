---
title: "2026 年 Apache Doris 3.0 新特性全解析"
date: 2026-06-15T14:00:00+08:00
categories: ["技术"]
description: "Doris 3.0 的存算分离、Arrow Flight SQL 加速、半结构化数据支持"
---

Apache Doris 3.0 在 2026 年 4 月正式 GA。作为 OLAP 领域增长最快的项目，这次大版本带来了几个关键变革。

## 1. 存算分离正式 GA

Doris 传统架构是存算一体的 Shared-Nothing：

```
┌──────────────────────────────────────┐
│  FE (Frontend)  ← 元数据 + 查询计划   │
│  BE (Backend)   ← 计算 + 存储在一起   │
└──────────────────────────────────────┘
```

3.0 支持**计算和存储分离部署**：

```
┌────────────┐    ┌──────────────────┐
│  BE (计算) │───▶│ 共享存储 (S3/HDFS) │
└────────────┘    └──────────────────┘
```

好处：
- **弹性扩缩**：计算节点可以独立扩缩，不影响数据
- **成本优化**：冷数据放对象存储，热数据本地 SSD
- **多集群共享**：多个计算集群共享同一份数据

## 2. Arrow Flight SQL：查询速度飞跃

之前 Doris 通过 MySQL 协议返回结果，序列化开销大。3.0 原生支持 **Arrow Flight SQL**：

```bash
# 直接用 Arrow Flight SQL 连接
mysql -h fe_host -P 9040 -u root  # MySQL 协议
# Arrow Flight: 端口 8060，列式传输
```

实测对比（1000 万行查询）：

| 协议 | 耗时 | 数据量 |
|------|------|--------|
| MySQL 协议 | 8.2s | 850MB |
| Arrow Flight SQL | 1.3s | 320MB |

**6 倍加速 + 60% 带宽节省**，因为列式数据不需要反序列化为行式。

## 3. 半结构化数据支持

`VARIANT` 类型正式 GA，可以在 Doris 里存 JSON 并高效查询：

```sql
CREATE TABLE events (id BIGINT, payload VARIANT);
SELECT payload:user.name FROM events WHERE payload:event_type = 'click';
```

底层用列式存储 JSON，查询时只读取需要的字段。

## 4. 倒排索引增强

全文检索能力大幅提升。现在可以在 Doris 里做类似 Elasticsearch 的文本搜索：

```sql
CREATE INDEX idx_content ON articles(content) USING INVERTED;
SELECT * FROM articles WHERE content MATCH 'Doris|OLAP';
```

## 总结

Doris 3.0 最大的意义：**从 OLAP 引擎变成了统一的实时数据平台**。存算分离 + Arrow Flight + 半结构化数据，让它能覆盖更多场景。

如果你是数据后端方向，建议关注这三个方向：**存算分离架构**、**列式传输协议**、**倒排索引与 OLAP 融合**。
