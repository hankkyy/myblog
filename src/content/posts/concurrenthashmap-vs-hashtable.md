---
title: "ConcurrentHashMap 为什么比 Hashtable 快？锁分段到 CAS 的优化之路"
date: 2025-11-05T16:00:00+08:00
categories: ['技术']
description: "从 JDK 7 的 Segment 锁到 JDK 8 的 CAS + synchronized，理解并发容器的演进。"
---

Hashtable 和 ConcurrentHashMap 都是线程安全的 Map，但性能天差地别。

## Hashtable 的问题

Hashtable 用 `synchronized` 修饰所有方法。这意味着任何时候只有一个线程能操作整个 Map——读也锁，写也锁。并发度 = 1。

## JDK 7：分段锁（Segment）

JDK 7 的 ConcurrentHashMap 把整个 Map 分成 16 个 Segment（默认），每个 Segment 自带一把锁。

- 写操作：只锁对应的 Segment，其他 Segment 不受影响
- 读操作：不加锁（volatile 保证可见性）
- 并发度 = 16

分段锁的思想：不要把一整条路封了，只封正在施工的那一段。

## JDK 8：CAS + synchronized

JDK 8 放弃了 Segment 设计，改为更细粒度的锁：

- 桶为空 → CAS 操作直接插入（无锁）
- 桶不为空 → synchronized 锁住桶的头节点
- 链表转红黑树 → 提升查找效率

读操作依然不需要锁。

## 为什么放弃分段锁

1. Segment 的数量一开始就固定了（16），无法动态调整
2. 粒度还是不够细——一个 Segment 里有多个桶
3. JDK 8 的 synchronized 优化后性能不输 ReentrantLock

## 面试怎么答

1. Hashtable 全表锁，性能差
2. JDK 7 ConcurrentHashMap 用分段锁，并发度 16
3. JDK 8 用 CAS + synchronized 锁桶头节点，粒度更细
4. 结合红黑树的查找优化

能讲清楚 JDK 7 到 JDK 8 的演进，面试官会对你印象深刻。
