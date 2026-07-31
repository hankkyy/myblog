---
lang: en
title: "MySQL Index Interview Essentials: Why Is the Leftmost Prefix Match the Most Asked Question?"
date: 2025-06-15T11:00:00+08:00
categories: ['Database', 'Technology']
description: "Using a concrete query example to explain the leftmost prefix principle, covering index, and index condition pushdown for composite indexes."
---

MySQL index interview questions always revolve around the "leftmost prefix."

## Storage Structure of a Composite Index

Suppose there is a composite index `(a, b, c)`. In the B+Tree, it is first sorted by `a`, then by `b` for rows with the same `a`, and then by `c` for rows with the same `b`. It's like a dictionary — first by the initial letter, then the second letter, then the third.

## Which Queries Can Use This Index

```sql
-- ✅ Can use: starts with a (leftmost column)
WHERE a = 1

-- ✅ Can use: a = constant, b can be a range query
WHERE a = 1 AND b > 2

-- ✅ Can use: both a and b have equality conditions
WHERE a = 1 AND b = 2

-- ❌ Cannot use: skipped a
WHERE b = 2

-- ❌ Cannot use: columns after a range query cannot use the index
WHERE a > 1 AND b = 2  -- b cannot use the index
```

## Why Is It Called "Leftmost Prefix"

Because the index is sorted by the leftmost column first. It's like looking up a dictionary — if you don't know the first letter, you can't use the pinyin index. It's the same logic as why `LIKE 'abc%'` can use an index but `LIKE '%abc'` cannot.

## Two Bonus Concepts

**Covering Index**: All queried columns are in the index, so no table lookup (回表) is needed. In `EXPLAIN`, the `Extra` column shows `Using index`.

**Index Condition Pushdown (ICP)**: A MySQL 5.6 feature that pushes some filter conditions down to the storage engine layer, reducing the number of table lookups.

## Answer Framework for Interviews

1. Start with the sorting characteristics of the B+Tree
2. Explain the leftmost prefix using the storage order of a composite index
3. Give positive and negative examples
4. Mention covering index and index condition pushdown

Indexes are the foundation of databases. Once you understand them thoroughly, you'll rarely stumble in interviews.