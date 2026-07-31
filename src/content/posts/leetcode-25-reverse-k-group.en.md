---
lang: en
title: "LeetCode 25. Reverse Nodes in k-Group: The Elegance of a Recursive Solution"
date: 2025-07-08T16:00:00+08:00
categories: ['LeetCode']
description: "Using a recursive approach to solve this Hard-level linked list reversal problem. The code is short but highly logical, and writing a recursive solution in an interview earns major points."
---

Reverse Nodes in k-Group is a Hard-level linked list problem, but solving it recursively is remarkably concise.

## Problem

Given the linked list `1→2→3→4→5` and k=3, the output is `3→2→1→4→5` (the last group with fewer than k nodes remains unchanged).

## Recursive Approach

- Starting from the current node, count k nodes
- If there are at least k nodes, reverse these k nodes, then recursively process the rest
- If there are fewer than k nodes, return the current node as-is

## Code

```java
public ListNode reverseKGroup(ListNode head, int k) {
    // Check if there are at least k nodes
    ListNode cur = head;
    int count = 0;
    while (cur != null && count < k) {
        cur = cur.next;
        count++;
    }
    
    if (count == k) {
        // Reverse the first k nodes
        ListNode prev = null;
        cur = head;
        for (int i = 0; i < k; i++) {
            ListNode next = cur.next;
            cur.next = prev;
            prev = cur;
            cur = next;
        }
        // head is now the tail of the reversed group; connect it to the recursive result
        head.next = reverseKGroup(cur, k);
        return prev; // prev is the new head of the reversed group
    }
    
    return head; // Fewer than k nodes, no reversal
}
```

## Key Insights of the Code

1. First check if there are enough nodes — if not, return immediately; only reverse when there are k nodes
2. After reversal, head becomes the tail node; recursively process the rest and attach it to head.next
3. prev is the new head of the reversed group
4. Recursion termination condition: fewer than k nodes remaining

## Comparison with the Iterative Solution

The iterative solution requires more complex pointer manipulation. The recursive solution is more concise, but you need to be mindful of stack depth — the problem guarantees the linked list length does not exceed 5000, so recursion is safe.

This problem is a comprehensive test of linked list skills, and writing a recursive solution in an interview earns significant bonus points.