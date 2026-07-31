---
lang: en
title: "The Silent Revolution in Database Engines: After 40 Years of B+Tree Dominance, New Players Arrive"
date: 2026-07-06T14:00:00+08:00
categories: ["Database", "Technology"]
description: "From B+Tree to LSM, vector indexes, and learned indexes—database index structures are undergoing their biggest shift in four decades, and most CRUD developers haven't noticed yet."
---

Have you ever wondered: why does MySQL use B+Tree, RocksDB use LSM Tree, and vector databases use HNSW?

Most backend developers memorize "leftmost prefix" and "table lookups" but never stop to think: **Why do different databases choose different index structures? What would happen if they swapped?**

Behind this lies a silent revolution happening at the database engine level.

## B+Tree: The Forty-Year-Old King

B+Tree's design philosophy is "read-optimized": data is arranged sequentially on disk pages, and each node of the B+Tree fits exactly into one disk page. Lookups traverse from root to leaf, with disk I/O equal to the tree's height.

This design was perfect in the mechanical hard drive era—random reads/writes were slow, sequential reads/writes were fast. B+Tree packs data tightly together to minimize seek time.

But SSDs changed the game. SSDs have no seek time, and the gap between random and sequential reads has narrowed dramatically. B+Tree's core optimization assumption has been shaken.

## LSM Tree: The Write-First Rebel

LSM (Log-Structured Merge-Tree) flips the script: writes first go to an in-memory MemTable (a skip list or red-black tree), and when full, are flushed sequentially to disk as immutable SSTable files. Background threads periodically merge these files.

The result: **LSM writes are an order of magnitude faster than B+Tree, but reads must check multiple SSTable layers**.

RocksDB, Cassandra, and Apache Doris are all based on LSM. In write-intensive scenarios like logging, time-series data, and IoT, LSM reigns supreme.

## Vector Indexes: The New Species of the AI Era

This is the hottest direction of the past two years. Traditional indexes answer "what equals X" or "what's in this range," while vector indexes answer "what's most similar to this."

FAISS, ScaNN, HNSW—these algorithms are moving from the lab into database kernels. pgvector brings vector search to PostgreSQL, and Elasticsearch and Redis have added vector search too.

My prediction: within 5 years, vector indexes will be as commonplace as B+Tree. Today you casually say "add an index to this field"; tomorrow you'll say "add a vector index to this paragraph."

## Learned Indexes: Replacing Data Structures with Models

In 2018, Jeff Dean's team at Google introduced this concept. The core idea is disruptive: a B+Tree is essentially a function mapping keys to positions. If that's the case, why not use a small neural network to learn this mapping?

Learned indexes are extremely space-efficient—a B+Tree might take several MB, while a learned index might take just tens of KB. On embedded devices and edge nodes, this is a huge advantage.

But it's still in academia. The biggest challenge is data updates—when the data distribution changes, the model needs retraining.

## Why This Matters

Most CRUD developers use B+Tree their entire careers because it's MySQL's default. But understanding these directions has several benefits:

1. **Informed choices**. Read-heavy, write-light workloads favor B+Tree; write-heavy, read-light favors LSM; semantic search calls for vector indexes—every choice has trade-offs
2. **Interview confidence**. If an interviewer asks "why does MySQL use B+Tree for indexes," you can discuss LSM, vector indexes, and learned indexes—far more impressive than reciting textbook answers
3. **Seeing the trend**. Databases are the foundation of the software stack. When the foundation shifts, everything above it shifts too

Four decades of B+Tree dominance are coming to an end. It's not that B+Tree will be eliminated—it's that viable alternatives have finally emerged, letting you make the optimal choice for your scenario. That's what real technological progress looks like.

---

**References:**

- [Google AI — The Case for Learned Index Structures (Jeff Dean et al., 2018)](https://arxiv.org/abs/1712.01208)
- [Facebook Research — FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)