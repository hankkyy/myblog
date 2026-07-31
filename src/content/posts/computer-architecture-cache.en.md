---
lang: en
title: "Computer Architecture Interview Primer: CPU Cache and False Sharing"
date: 2025-10-10T14:00:00+08:00
categories: ['Tech']
description: "Understand how the CPU's three-level cache works, and why false sharing slows down multithreaded programs."
---

Knowledge of computer architecture lets you write high-performance code.

## Memory Hierarchy

```
Registers (0 cycles)
  ↓
L1 Cache (~4 clock cycles, 32KB)
  ↓
L2 Cache (~12 clock cycles, 256KB)
  ↓
L3 Cache (~40 clock cycles, 8MB-32MB, shared)
  ↓
Main Memory (~200 clock cycles)
  ↓
SSD (~100μs)
```

Each step down the hierarchy introduces an order-of-magnitude difference in speed. This is why the principle of locality (temporal locality + spatial locality) is so important.

## CPU Cache Line

CPU caches are not accessed byte-by-byte, but in "cache lines"—fixed-size blocks (typically 64 bytes). Even if you only read a single int (4 bytes), the CPU loads the entire cache line.

## False Sharing

**What is false sharing**:

```java
class Counter {
    volatile long a;  // Thread 1 only writes a
    volatile long b;  // Thread 2 only writes b
}
```

a and b may reside in the same 64-byte cache line. When Thread 1 modifies a, the entire cache line is marked "dirty," and Thread 2's copy of the cache line on another core is invalidated. Even though they operate on different variables, they must repeatedly synchronize the cache line.

**Solution**: Padding.

```java
class Counter {
    @Contended  // JDK 8+ annotation (requires -XX:-RestrictContended)
    volatile long a;
    @Contended
    volatile long b;
}
```

Or manual padding:

```java
class PaddedLong {
    volatile long value = 0;
    long p1, p2, p3, p4, p5, p6, p7; // Pad to 64 bytes
}
```

## Why Learn This

Disruptor (a high-performance queue) leverages a deep understanding of cache lines and is 5-10x faster than ArrayBlockingQueue. The bottleneck in high-performance programming is often not the algorithm, but the hardware.