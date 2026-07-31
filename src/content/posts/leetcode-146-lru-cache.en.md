---
lang: en
title: "LeetCode 146. LRU Cache: The Interviewer's Favorite Design Problem — Hand-Writing a Doubly Linked List + Hash Map"
date: 2025-03-30T10:00:00+08:00
categories: ['LeetCode']
description: "Implement an O(1) LRU cache in Java. This problem is almost a guaranteed interview question — understand the elegance of the doubly linked list."
---

The LRU Cache is one of the most frequently asked design problems in interviews. It requires both `get` and `put` to run in O(1) time.

## Approach

The core is a doubly linked list + hash map:

- Hash map: key → Node, for O(1) lookup
- Doubly linked list: maintains access order — most recently used at the head, least recently used at the tail

## Why Not Use LinkedHashMap?

Java's built-in `LinkedHashMap` can directly implement LRU (by setting `accessOrder=true`), but interviewers usually expect you to write it by hand. Understanding the underlying implementation matters more than just calling an API.

## Code Implementation

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

## Key Points

- Use dummy head/tail nodes to avoid null pointer checks
- `remove` and `addToHead` are the two core operations; all other methods build on them
- On `get`, move the accessed node to the head
- On `put`, if the key already exists, delete the old node first

## Follow-Up

Interviewers might ask: if you couldn't use a doubly linked list, how else could you implement it? Answer: you could use Java's `LinkedHashMap` (one-liner), but writing it by hand demonstrates deeper understanding.