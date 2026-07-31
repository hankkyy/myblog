---
lang: en
title: "Deep Dive into HashMap Source Code: Red-Black Tree Conversion and Resizing in JDK 8"
date: 2025-10-05T10:00:00+08:00
categories: ['Technology']
description: "A line-by-line analysis of HashMap's put method and resizing logic, explaining why interviewers always ask about HashMap."
---

HashMap is the most frequently asked data structure in Java interviews.

## Data Structure

HashMap in JDK 8 = array + linked list + red-black tree. Each position in the array is a "bucket," which may contain a linked list or a red-black tree.

## The put Method Flow

```java
public V put(K key, V value) {
    // 1. Calculate hash
    int hash = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    
    // 2. Locate bucket index
    int index = (n - 1) & hash;  // Equivalent to hash % n, but bitwise is faster
    
    // 3. If bucket is empty, insert directly
    // 4. If bucket is not empty, traverse the linked list/tree
    //     - If an equal key is found, update the value
    //     - If not found, insert
    // 5. If linked list length >= 8 and array length >= 64, convert to red-black tree
    // 6. If size > threshold, resize
}
```

## Why Use (n-1) & hash

Because n (the array length) is always a power of 2, the binary representation of (n-1) is all 1s. `(n-1) & hash` is equivalent to `hash % n`, but bitwise operations are much faster than modulo.

## Why hash >>> 16

This mixes the high 16 bits and low 16 bits of the hashCode, allowing the high bits to participate in index calculation. Otherwise, when the array is small, only the low bits are involved, leading to uneven distribution.

## Red-Black Tree Conversion

When the linked list length >= 8 (TREEIFY_THRESHOLD) and the array length >= 64 (MIN_TREEIFY_CAPACITY), the linked list is converted to a red-black tree to improve lookup efficiency (O(n) → O(log n)).

Why is the threshold 8? According to the official comments, under an ideal hash distribution, the probability of a linked list reaching length 8 is 0.00000006.

## Resizing

When `size > threshold` (capacity * load factor, default 0.75), the HashMap resizes to twice its original size. During resizing, each element's position is recalculated—it either stays in its original position or moves to the original position + old capacity.

HashMap's design reflects an extreme pursuit of performance at every turn. Once you understand its source code, your understanding of data structures will reach a new level.