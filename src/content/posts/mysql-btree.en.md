---
lang: en
title: "MySQL Indexing Principles: Why B+Tree Rules the Database World"
date: 2026-05-22T11:00:00+08:00
categories: ["Technology"]
description: "From disk I/O, B+Tree structure, clustered indexes to covering indexes, this article explains MySQL indexing thoroughly"
---

A classic interview question: "Why does MySQL use B+Tree instead of binary trees/hash tables/B-Trees?"

## Disk I/O Is the Root Cause

```
CPU L1 Cache:  ~1ns
Memory access:      ~100ns
SSD random read:    ~100μs   ← 1000x slower than memory
HDD random read:    ~10ms    ← 100,000x slower than memory
```

The bottleneck of databases is always disk I/O. The goal of indexing: **find data with minimal disk I/O**.

## B+Tree Structure

```
              [30|60]          ← Non-leaf nodes store only keys
            /    |    \
      [5|15]  [40|50]  [70|80]  ← Internal nodes
       /  \    /  \    /  \
    [Leaf nodes — store all data + doubly linked list]
```

- All data is stored in leaf nodes
- Leaf nodes are connected via a doubly linked list (range-query friendly)
- Non-leaf nodes store only keys, so one page can hold more → shorter tree

## Why Not Other Structures

| Structure | Problem |
|------|------|
| Binary search tree | Can degenerate into a linked list, O(n) |
| Red-black tree | Binary tree, deep, more I/O |
| Hash table | No range queries, no sorting |
| B-Tree | Internal nodes also store data, fewer keys per page |

## Clustered Index vs Secondary Index

```sql
-- InnoDB's clustered index: data stored in leaf nodes
-- The primary key is the clustered index
SELECT * FROM users WHERE id = 100;  -- One B+Tree lookup

-- Secondary index: leaf nodes store primary key values
-- Requires "table lookup" (back to the clustered index)
SELECT * FROM users WHERE name = 'Alice';
-- 1. Find the primary key id in the name index
-- 2. Use the id to find the full row in the clustered index
```

**Covering index**: when all queried columns are in the index, avoiding the table lookup.

```sql
-- No table lookup needed
SELECT id, name FROM users WHERE name = 'Alice';
```

> B+Tree has dominated databases for 40 years, thanks to its extreme optimization for disk I/O.