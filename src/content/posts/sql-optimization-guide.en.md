---
lang: en
title: "SQL Optimization Interview Guide: Practical Insights from EXPLAIN to Index Design"
date: 2025-05-20T16:00:00+08:00
categories: ['Database', 'Technology']
description: "A practical guide to understanding EXPLAIN output fields and core index optimization principles using real slow SQL cases."
---

SQL optimization is a frequent topic in backend interviews and an essential skill for everyday development.

## Core EXPLAIN Fields

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 100 AND status = 'paid';
```

| Field | Meaning | Good Indicator |
|-------|---------|----------------|
| type | Access type | const > ref > range > index > ALL |
| key | Index used | Not NULL |
| rows | Rows scanned | The fewer, the better |
| Extra | Additional info | Using index (covering index) |

## The type Field (From Best to Worst)

- **const**: Equality lookup on primary key or unique index (fastest)
- **ref**: Equality lookup on non-unique index
- **range**: Index range scan (>, <, BETWEEN, LIKE 'abc%')
- **index**: Full index scan
- **ALL**: Full table scan (worst, must optimize)

## Index Design Principles

1. **Leftmost prefix**: A composite index `(a, b, c)` can only be used with `WHERE a = 1` or `WHERE a = 1 AND b = 2`
2. **High selectivity**: The more distinct the values in a column, the better (gender has only two values, low selectivity; user IDs number in the millions, high selectivity)
3. **Avoid index invalidation**:
   - Using functions in WHERE: `WHERE YEAR(create_time) = 2025` won't use the index
   - Implicit type conversion: `WHERE phone = 13800138000` won't use the index if phone is a varchar
   - OR conditions connecting non-indexed columns can trigger a full table scan
4. **Covering index**: When all queried columns are within the index, Using index appears, avoiding table lookups

## A Typical Case Study

```sql
-- Slow query: type=ALL, rows=1000000
SELECT * FROM orders WHERE user_id = 123 ORDER BY create_time DESC LIMIT 10;

-- Optimization: add a composite index
ALTER TABLE orders ADD INDEX idx_user_time (user_id, create_time);

-- After optimization: type=ref, rows=100, Extra=Using index
```

## Interview Talking Points

> When encountering a slow SQL, first use EXPLAIN to check the access type and the number of rows scanned. An ALL type full table scan must be optimized. The core principles for adding indexes are leftmost prefix + high selectivity. A covering index avoids table lookups and delivers better performance. Finally, use profiles to compare the execution time before and after optimization.

Knowing how to use EXPLAIN matters more than just knowing how to write SQL.