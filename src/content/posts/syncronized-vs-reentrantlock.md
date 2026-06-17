---
title: "synchronized vs ReentrantLock：从面试被问到源码实现"
date: 2025-05-30T16:00:00+08:00
categories: ['技术']
description: "对比 Java 内置锁和显式锁的差异，包括锁升级过程和 AQS 原理。"
---

synchronized 和 ReentrantLock 有什么区别？十个面试九个问。

## 用法对比

```java
// synchronized
synchronized (lock) {
    // 临界区
}

// ReentrantLock
lock.lock();
try {
    // 临界区
} finally {
    lock.unlock();  // 必须在 finally 中释放！
}
```

## 核心区别

| 特性 | synchronized | ReentrantLock |
|------|-------------|---------------|
| 实现 | JVM 内置（monitorenter/exit）| JDK 层面（AQS） |
| 可中断 | 不支持 | lockInterruptibly() |
| 超时获取 | 不支持 | tryLock(time, unit) |
| 公平锁 | 非公平 | 可公平可非公平 |
| 多条件 | 一个条件队列 | 多个 Condition |
| 性能 | JDK 6+ 优化后旗鼓相当 | 差不多 |

## JDK 6 的锁升级

synchronized 在 JDK 6 之前是重量级锁（直接操作系统互斥量）。JDK 6 引入了锁升级：

1. **无锁**：没有线程竞争
2. **偏向锁**：同一个线程多次获取，直接通过（CAS 标记线程 ID）
3. **轻量级锁**：多个线程交替执行（CAS 自旋）
4. **重量级锁**：真正的阻塞（操作系统层面）

## ReentrantLock 底层：AQS

ReentrantLock 基于 AQS（AbstractQueuedSynchronizer）。AQS 维护了一个 state（volatile int）和一个 FIFO 等待队列。

- 加锁：CAS 把 state 从 0 改为 1
- 重入：同一个线程再获取，state + 1
- 释放：state - 1，state 为 0 时唤醒等待线程

## 什么时候用 ReentrantLock

- 需要尝试获取锁（tryLock）
- 需要可中断的锁
- 需要公平锁（先来先得）

能用 synchronized 就用 synchronized。代码更简单，出错的概率更小。
