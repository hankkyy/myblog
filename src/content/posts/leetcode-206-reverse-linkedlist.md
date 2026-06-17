---
title: "LeetCode 206. 反转链表：迭代和递归两种解法，面试必会"
date: 2025-06-20T09:00:00+08:00
categories: ['LeetCode']
description: "反转链表看似简单，但迭代和递归两种写法都要会，面试中让你换着写是常事。"
---

反转链表是链表操作的基础，面试官可能让你先写迭代，再写递归。

## 迭代解法

用三个指针：prev（前一个）、cur（当前）、next（下一个）。

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode cur = head;
    while (cur != null) {
        ListNode next = cur.next;  // 保存下一个
        cur.next = prev;           // 反转指向
        prev = cur;                // 前移
        cur = next;                // 前移
    }
    return prev;
}
```

画图理解：每次把 cur 的箭头从指向 next 变成指向 prev。

## 递归解法

```java
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;
    
    ListNode newHead = reverseList(head.next);
    head.next.next = head;  // 把后一个节点指向自己
    head.next = null;       // 断开原来的指向
    
    return newHead;
}
```

递归的思路：假设后面的链表已经反转好了，把当前节点接到已反转链表的末尾。

## 递归执行过程

以 `1→2→3→null` 为例：

1. 递归到最深处 `head=3`，返回 3
2. 回溯到 `head=2`：`2.next.next = 2`（3 指向 2），`2.next = null`
3. 回溯到 `head=1`：`1.next.next = 1`（2 指向 1），`1.next = null`

结果：`3→2→1→null`

## 面试要点

- 迭代解注意保存 next，否则反转后就找不到后续节点了
- 递归解关键是 `head.next.next = head` 这一行
- 两种方法都要会，面试官经常换着考
