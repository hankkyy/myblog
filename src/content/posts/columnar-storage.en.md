---
lang: en
title: "Why Is ClickHouse 100x Faster Than MySQL? The Principle of Columnar Storage"
date: 2026-06-10T16:00:00+08:00
categories: ["Technology"]
description: "Understanding the performance advantages of columnar storage from three perspectives: disk I/O, compression, and vectorized execution"
---

A common interview question: "Why do OLAP databases use columnar storage instead of row-based storage?"

Let's let the data speak for itself. Suppose we have a table:

```sql
CREATE TABLE orders (
  id INT, user_id INT, amount DECIMAL,
  status VARCHAR, created_at DATETIME
);
-- 100 million rows
```

Query: `SELECT SUM(amount) FROM orders WHERE status = 'paid'`

## Row-Based Storage (MySQL/InnoDB)

Data is arranged row by row on disk:

```
[1|101|99.9|paid|2026-01-01][2|102|50.0|pending|2026-01-02]...
```

Executing `SUM(amount) WHERE status = 'paid'`:

1. Reads the entire row (all 5 columns) → **significant unnecessary I/O**
2. Parses each row, extracting status and amount
3. Filters + aggregates

**Actual data read: 5 columns × 100 million rows ≈ 2GB+**

## Columnar Storage (ClickHouse/Doris)

Data is arranged column by column on disk:

```
amount:  [99.9 | 50.0 | 30.0 | ...]   ← only read this column
status:  [paid | pending | paid | ...] ← and this column
```

Executing the same query:

1. **Only reads the amount and status columns**
2. Column data is stored contiguously, enabling a single scan
3. Uses SIMD vectorized comparison: compares 256 values at once

**Actual data read: 2 columns × 100 million rows ≈ 800MB, less than 40% of row-based storage.**

## Compression Advantage

In columnar storage, values in the same column share the same data type, resulting in extremely high compression ratios:

| Compression Algorithm | Row-Based Compression Ratio | Columnar Compression Ratio |
|----------|------------|------------|
| LZ4 | 2-3x | 5-10x |
| ZSTD | 3-5x | 10-20x |

Because the `status` column only contains a few distinct values (paid/pending/cancelled), dictionary encoding can compress it to nearly 1% of its original size.

## Vectorized Execution

This is the biggest source of performance gains in columnar storage:

```cpp
// Traditional row-by-row processing
for (int i = 0; i < n; i++) {
    if (status[i] == PAID)
        sum += amount[i];
}

// Vectorized: processes 256 rows at once
__m256i status_vec = _mm256_load_si256(&status[i]);
__m256i mask = _mm256_cmpeq_epi32(status_vec, paid_vec);
sum += _mm256_mask_add(mask, amount_vec);
```

CPU SIMD instructions process 8 32-bit integers at a time (AVX2) or 16 (AVX-512). Columnar storage keeps data contiguous in memory, making it naturally suited for vectorization.

## When Should You Use Columnar Storage?

| Scenario | Recommendation |
|------|------|
| `SELECT *` returning full rows | Row-based |
| Aggregation queries (SUM/COUNT/AVG) | **Columnar** |
| Full table scans + filtering | **Columnar** |
| Point queries (WHERE id = 1) | Row-based |
| Frequent updates | Row-based |

## Real-World Performance Comparison

Tested on a 16-core, 64GB machine with a 100-million-row TPC-H lineitem table:

| Query | MySQL 8.0 | ClickHouse | Speedup |
|------|-----------|------------|------|
| `SUM(quantity)` | 4.2s | 0.18s | **23x** |
| `GROUP BY returnflag` | 12.8s | 0.35s | **36x** |
| `WHERE + GROUP BY + ORDER BY` | 45.6s | 0.42s | **108x** |

> Columnar storage isn't fast because of faster hardware — it's **less data read** + **better compression** + **vectorized execution**. These three factors combined create the 100x performance gap.