---
lang: en
title: "Java Collections Framework Interview Guide: ArrayList, LinkedList, HashMap Under the Hood"
date: 2025-01-10T10:00:00+08:00
categories: ['Technology']
description: "From ArrayList resizing to HashMap treeification, the Collections Framework is the first hurdle in Java interviews."
---

The Java Collections Framework is a must-know topic in interviews, and it's usually the first question.

## ArrayList vs LinkedList

**ArrayList**:
- Underlying: Object[] array
- Lookup: O(1) (index-based)
- Insertion/Deletion: O(n) (requires shifting elements)
- Resizing: Default grows to 1.5x
- Memory: Contiguous memory space

**LinkedList**:
- Underlying: Doubly linked list
- Lookup: O(n)
- Insertion/Deletion: O(1) (if the node is already located)
- Implements the Deque interface, so it can be used as a queue

Interview tip: Use ArrayList in most scenarios. LinkedList only has an advantage when you frequently insert or delete at the head.

## HashSet vs TreeSet

- HashSet: Based on HashMap, O(1) operations, unordered
- TreeSet: Based on TreeMap (red-black tree), O(log n) operations, ordered

## HashMap 1.7 vs 1.8

| Feature | JDK 7 | JDK 8 |
|---------|-------|-------|
| Structure | Array + linked list | Array + linked list + red-black tree |
| Insertion | Head insertion | Tail insertion |
| Hash algorithm | 4 perturbations | 1 perturbation |
| Concurrency issue | Infinite loop (resize) | Data overwrite |

The head insertion method during resizing in JDK 7 can reverse the linked list, potentially forming a circular linked list under multithreading (CPU at 100%). JDK 8 switched to tail insertion, which resolves the infinite loop but still has concurrency issues—use ConcurrentHashMap for multithreaded scenarios.

## fail-fast Mechanism

If a collection is modified during iteration (not via the iterator's own remove method), a ConcurrentModificationException is thrown. The principle: the collection maintains an internal modCount that increments on every modification, and the iterator checks this value during traversal.

In real interviews, the key to collection questions is not just knowing the API, but understanding the underlying data structures and the trade-offs in time complexity.