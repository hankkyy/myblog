---
title: "计算机架构面试入门：CPU 缓存和伪共享（False Sharing）"
date: 2025-10-10T14:00:00+08:00
categories: ['技术']
description: "理解 CPU 三级缓存的工作机制，以及为什么伪共享会让多线程程序变慢。"
---

计算机架构的知识让你写出高性能代码。

## 存储层次

```
寄存器（0 延迟）
  ↓
L1 Cache（~4 个时钟周期，32KB）
  ↓
L2 Cache（~12 个时钟周期，256KB）
  ↓
L3 Cache（~40 个时钟周期，8MB-32MB，共享）
  ↓
主存（~200 个时钟周期）
  ↓
SSD（~100μs）
```

每往下走一层，速度差一个数量级。这就是为什么局部性原理（时间局部性 + 空间局部性）如此重要。

## CPU 缓存行（Cache Line）

CPU 缓存不是按字节存取的，而是按「缓存行」——固定大小的块（通常 64 字节）。即使你只读一个 int（4 字节），CPU 也会加载整个缓存行。

## 伪共享（False Sharing）

**什么是伪共享**：

```java
class Counter {
    volatile long a;  // 线程 1 只写 a
    volatile long b;  // 线程 2 只写 b
}
```

a 和 b 可能在同一个 64 字节的缓存行里。线程 1 修改 a 时，整个缓存行被标记为「脏」，线程 2 在另一个核心上的缓存行副本就失效了。即使它们操作的是不同的变量，也要反复同步缓存行。

**解决**：填充（Padding）。

```java
class Counter {
    @Contended  // JDK 8+ 的注解（需要 -XX:-RestrictContended）
    volatile long a;
    @Contended
    volatile long b;
}
```

或者手动填充：

```java
class PaddedLong {
    volatile long value = 0;
    long p1, p2, p3, p4, p5, p6, p7; // 填充到 64 字节
}
```

## 为什么要学这个

Disruptor（高性能队列）利用了对缓存行的深刻理解，比 ArrayBlockingQueue 快 5-10 倍。高性能编程的瓶颈往往不在算法，而在硬件。
