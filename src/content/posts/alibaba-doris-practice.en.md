---
lang: en
title: "Alibaba's Real-Time Data Warehouse Practice with Doris: 50 Billion Records Daily"
date: 2026-03-28T16:00:00+08:00
categories: ["Database", "Technology"]
description: "Alibaba Cloud shares its experience building a real-time data warehouse with Apache Doris, processing 50 billion records daily with P99 query latency under 1 second."
---

I recently came across the real-time data warehouse practice based on Doris shared by Alibaba Cloud's database team, and it's packed with valuable insights.

## Business Scenarios

- Real-time dashboards for Taobao/Tmall
- Real-time ROI analysis for ad campaigns
- Real-time optimization of logistics routes

Daily data volume: 50 billion records. Storage per single table: PB-level.

## Key Technical Points

### 1. Data Layering

```
ODS (Raw Data) → DWD (Detail Data) → DWS (Summary Data) → ADS (Application Data)
```

Doris primarily handles query workloads at the DWS and ADS layers, while the ODS/DWD layers use Flink for real-time ETL.

### 2. Partitioning and Bucketing Strategy

- Partition by day, retaining 30 days of hot data
- Choose high-cardinality fields (e.g., user_id) as the bucketing key
- Keep each bucket at 1-3GB to ensure query parallelism

### 3. Materialized Views for Acceleration

Create materialized views for high-frequency aggregation queries (e.g., "GMV in the past hour"), reducing query latency from 3s to 50ms.

## Takeaways for Learners

Doris is gaining significant traction in China. Compared to ClickHouse, Doris offers better standard SQL compatibility and operational friendliness. If you're looking to pursue a career in data infrastructure, Doris is definitely worth learning.

---

**References:**

- [Apache Doris Official Documentation](https://doris.apache.org/)