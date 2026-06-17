---
title: "HashMap 源码深度解析：JDK 8 的红黑树化和扩容机制"
date: 2025-10-05T10:00:00+08:00
categories: ['技术']
description: "逐行分析 HashMap 的 put 方法和扩容逻辑，理解为什么面试官总问 HashMap。"
---

HashMap 是 Java 面试出场率最高的数据结构。

## 数据结构

JDK 8 的 HashMap = 数组 + 链表 + 红黑树。数组的每个位置是一个「桶」（bucket），桶里可能是链表或红黑树。

## put 方法的流程

```java
public V put(K key, V value) {
    // 1. 计算 hash
    int hash = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    
    // 2. 定位桶位置
    int index = (n - 1) & hash;  // 等价于 hash % n，但位运算更快
    
    // 3. 如果桶为空，直接放
    // 4. 如果桶不为空，遍历链表/树
    //     - 找到相等的 key，更新 value
    //     - 没找到，插入
    // 5. 链表长度 >= 8 且数组长度 >= 64，转为红黑树
    // 6. size > threshold，扩容
}
```

## 为什么用 (n-1) & hash

因为 n（数组长度）总是 2 的幂，（n-1）的二进制全是 1。`(n-1) & hash` 等价于 `hash % n`，但位运算比取模快得多。

## 为什么 hash 要 >>> 16

把 hashCode 的高 16 位和低 16 位混合，让高位也参与索引计算。否则当数组较小时，只有低位参与运算，分布不均匀。

## 红黑树化

链表长度 >= 8（TREEIFY_THRESHOLD）且数组长度 >= 64（MIN_TREEIFY_CAPACITY）时转为红黑树，提升查找效率（O(n) → O(log n)）。

为什么阈值是 8？官方注释说，在理想的 hash 分布下，链表达到 8 的概率是 0.00000006。

## 扩容

当 `size > threshold`（容量 * 负载因子，默认 0.75）时扩容为原来的两倍。扩容时重新计算每个元素的位置——要么在原来位置，要么在原来位置 + 旧容量。

HashMap 的设计处处体现着对性能的极致追求。理解了它的源码，你对数据结构的理解会上一个台阶。
