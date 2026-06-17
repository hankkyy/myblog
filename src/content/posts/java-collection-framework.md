---
title: "Java 集合框架面试全解：ArrayList、LinkedList、HashMap 底层原理"
date: 2025-01-10T10:00:00+08:00
categories: ['技术']
description: "从 ArrayList 的扩容到 HashMap 的树化，集合框架是 Java 面试的第一关。"
---

Java 集合框架是面试的必考题，而且通常是第一道。

## ArrayList vs LinkedList

**ArrayList**：
- 底层：Object[] 数组
- 查询：O(1)（基于索引）
- 插入/删除：O(n)（需要移动元素）
- 扩容：默认扩容到 1.5 倍
- 内存：连续内存空间

**LinkedList**：
- 底层：双向链表
- 查询：O(n)
- 插入/删除：O(1)（如果已经定位到节点）
- 实现了 Deque 接口，可以当队列用

面试话术：大多数场景用 ArrayList。LinkedList 只在频繁在头部插入删除时才有优势。

## HashSet vs TreeSet

- HashSet：基于 HashMap，O(1) 操作，无序
- TreeSet：基于 TreeMap（红黑树），O(log n) 操作，有序

## HashMap 1.7 vs 1.8

| 特性 | JDK 7 | JDK 8 |
|------|-------|-------|
| 结构 | 数组+链表 | 数组+链表+红黑树 |
| 插入 | 头插法 | 尾插法 |
| Hash 算法 | 4 次扰动 | 1 次扰动 |
| 并发问题 | 死循环（resize） | 数据覆盖 |

JDK 7 扩容时的头插法会导致链表反转，多线程下可能形成环形链表（CPU 100%）。JDK 8 改用尾插法，解决了死循环但仍有并发问题——多线程下推荐用 ConcurrentHashMap。

## fail-fast 机制

遍历集合时如果集合被修改（非 iterator 自己的 remove），会抛出 ConcurrentModificationException。原理：集合内部有一个 modCount，每次修改 +1，遍历时检查这个值。

实际面试中，集合问题的关键是不仅要会 API，还要理解底层数据结构和时间复杂度的取舍。
