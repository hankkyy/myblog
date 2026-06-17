---
title: "LeetCode 146. LRU Cache：面试官最爱的设计题，手写双向链表+哈希表"
date: 2025-03-30T10:00:00+08:00
categories: ['LeetCode']
description: "用 Java 实现 O(1) 的 LRU 缓存，面试中这道题几乎必考，理解双向链表的精妙之处。"
---

LRU Cache 是面试频率最高的设计题之一。要求 get 和 put 都是 O(1)。

## 思路

核心是双向链表 + 哈希表：

- 哈希表：key → Node，O(1) 查找
- 双向链表：维护访问顺序，最近使用的在头部，最久未使用的在尾部

## 为什么不用 LinkedHashMap？

Java 自带的 LinkedHashMap 可以直接实现 LRU（设置 accessOrder=true），但面试官通常要求手写。理解底层实现比调 API 更重要。

## 代码实现

```java
class LRUCache {
    class Node {
        int key, value;
        Node prev, next;
        Node(int k, int v) { key = k; value = v; }
    }
    
    private Map<Integer, Node> map = new HashMap<>();
    private Node head = new Node(0, 0), tail = new Node(0, 0);
    private int capacity;
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }
    
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        remove(node);
        addToHead(node);
        return node.value;
    }
    
    public void put(int key, int value) {
        if (map.containsKey(key)) {
            remove(map.get(key));
        }
        Node node = new Node(key, value);
        map.put(key, node);
        addToHead(node);
        if (map.size() > capacity) {
            Node last = tail.prev;
            remove(last);
            map.remove(last.key);
        }
    }
    
    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void addToHead(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
}
```

## 关键点

- 用虚拟头尾节点（dummy head/tail）避免空指针判断
- remove 和 addToHead 是两个核心操作，其他方法基于它们
- get 时要把访问的节点移到头部
- put 时如果 key 已存在要先删除旧的

## 扩展

面试官可能会问：如果不用双向链表，还能怎么实现？答：可以用 Java 的 LinkedHashMap（一句话搞定），但手写更体现功底。
