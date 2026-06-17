---
title: "LeetCode 25. K 个一组翻转链表：递归解法的简洁与优雅"
date: 2025-07-08T16:00:00+08:00
categories: ['技术']
description: "用递归思路解决链表翻转的 Hard 题，代码虽短但逻辑极强，面试中能写出递归解会加分很多。"
---

K 个一组翻转链表是链表题中的 Hard，但用递归来做非常简洁。

## 题目

给定链表 `1→2→3→4→5`，k=3，输出 `3→2→1→4→5`（最后不足 k 个的保持原样）。

## 递归思路

- 从当前节点开始，数 k 个节点
- 如果够 k 个，翻转这 k 个节点，然后递归处理剩下的
- 如果不够 k 个，直接返回当前节点

## 代码

```java
public ListNode reverseKGroup(ListNode head, int k) {
    // 检查是否有 k 个节点
    ListNode cur = head;
    int count = 0;
    while (cur != null && count < k) {
        cur = cur.next;
        count++;
    }
    
    if (count == k) {
        // 翻转前 k 个
        ListNode prev = null;
        cur = head;
        for (int i = 0; i < k; i++) {
            ListNode next = cur.next;
            cur.next = prev;
            prev = cur;
            cur = next;
        }
        // head 现在成了翻转后的尾节点，连接递归结果
        head.next = reverseKGroup(cur, k);
        return prev; // prev 是翻转后的头节点
    }
    
    return head; // 不足 k 个，不翻转
}
```

## 代码精妙之处

1. 先检查够不够 k 个——不够直接返回，够了才翻转
2. 翻转后 head 变成尾节点，递归处理剩下的接在 head.next
3. prev 是翻转后的新头节点
4. 递归终止条件：不足 k 个

## 迭代解法对比

迭代解需要更复杂的指针操作。递归解虽然简洁但需要注意栈深度——题目保证链表长度不超过 5000，递归是安全的。

这道题是链表题的集大成者，面试中能写出递归解非常加分。
