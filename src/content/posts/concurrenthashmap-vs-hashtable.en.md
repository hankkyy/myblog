---
lang: en
title: "Why Is ConcurrentHashMap Faster Than Hashtable? The Optimization Path from Lock Striping to CAS"
date: 2025-11-05T16:00:00+08:00
categories: ['Technology']
description: "From JDK 7's Segment locks to JDK 8's CAS + synchronized, understand the evolution of concurrent containers."
---

Hashtable and ConcurrentHashMap are both thread-safe Maps, but their performance differs vastly.

## The Problem with Hashtable

Hashtable uses `synchronized` to guard all its methods. This means only one thread can operate on the entire Map at any given time—reads are locked, and writes are locked. Concurrency level = 1.

## JDK 7: Segment Locks

JDK 7's ConcurrentHashMap divides the entire Map into 16 Segments (by default), each with its own lock.

- Write operations: only lock the corresponding Segment; other Segments remain unaffected
- Read operations: no locking (volatile ensures visibility)
- Concurrency level = 16

The idea behind lock striping: don't block the entire road—only seal off the section under construction.

## JDK 8: CAS + synchronized

JDK 8 abandoned the Segment design in favor of finer-grained locking:

- Bucket is empty → CAS operation for direct insertion (lock-free)
- Bucket is not empty → synchronized locks the head node of the bucket
- Linked list converts to red-black tree → improves lookup efficiency

Read operations still require no locks.

## Why Lock Striping Was Abandoned

1. The number of Segments was fixed at initialization (16) and could not be adjusted dynamically
2. The granularity was still not fine enough—a Segment contained multiple buckets
3. After JDK 8's synchronized optimizations, its performance is on par with ReentrantLock

## How to Answer in an Interview

1. Hashtable uses a table-wide lock, resulting in poor performance
2. JDK 7's ConcurrentHashMap uses Segment locks, providing a concurrency level of 16
3. JDK 8 uses CAS + synchronized to lock the bucket head node, achieving finer granularity
4. Combined with red-black tree lookup optimizations

If you can clearly explain the evolution from JDK 7 to JDK 8, the interviewer will be impressed.