---
lang: en
title: "Doris vs ClickHouse: A Comparative Study of OLAP Databases"
date: 2025-04-10T15:00:00+08:00
categories: ["Database", "Technology"]
description: "A comparative study of the architectural differences, performance characteristics, and use cases of Doris and ClickHouse."
---

I've been studying OLAP databases recently and put together a comparison between Doris and ClickHouse.

## Architectural Differences

**ClickHouse:**
- Pure columnar storage with a powerful MergeTree engine
- Exceptional performance for single-table aggregations
- Weaker JOIN capabilities
- Open-sourced by Yandex (Russia)

**Doris:**
- MPP + columnar storage architecture
- Better standard SQL compatibility
- Stronger JOIN capabilities
- Open-sourced by Baidu with an active domestic community

## Performance Comparison

- Single-table aggregation: ClickHouse is slightly faster
- Multi-table JOIN: Doris is stronger
- High-concurrency queries: Doris's Unique Key model has an advantage
- Data updates: Doris natively supports Upsert

## Learning Recommendations

Both are excellent OLAP engines. If you're getting started with data analysis, Doris offers better SQL compatibility and a gentler learning curve. If you're doing pure log analysis, ClickHouse delivers superior single-table performance.

Choose based on your business use case, or learn both to understand their architectural design philosophies.

---

**References:**

- [Apache Doris](https://doris.apache.org/)
- [ClickHouse](https://clickhouse.com/)