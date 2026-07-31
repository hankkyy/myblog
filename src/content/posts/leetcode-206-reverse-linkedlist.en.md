---
lang: en
title: "LeetCode 206. Reverse Linked List: Iterative and Recursive Solutions, a Must-Know for Interviews"
date: 2025-06-20T09:00:00+08:00
categories: ['LeetCode']
description: "Reversing a linked list may seem simple, but you need to know both the iterative and recursive approaches — interviewers often ask you to switch between them."
---

Reversing a linked list is a fundamental operation. An interviewer may ask you to write the iterative version first, then the recursive one.

## Iterative Solution

Use three pointers: prev (previous), cur (current), and next (next).

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode cur = head;
    while (cur != null) {
        ListNode next = cur.next;  // Save the next node
        cur.next = prev;           // Reverse the pointer
        prev = cur;                // Move forward
        cur = next;                // Move forward
    }
    return prev;
}
```

Visualize it: each step, you change cur's arrow from pointing to next to pointing to prev.

## Recursive Solution

```java
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;
    
    ListNode newHead = reverseList(head.next);
    head.next.next = head;  // Point the next node back to the current one
    head.next = null;       // Break the original pointer
    
    return newHead;
}
```

The recursive idea: assume the rest of the list is already reversed, then append the current node to the end of the reversed list.

## Recursive Execution Walkthrough

Using `1→2→3→null` as an example:

1. Recurse to the deepest level with `head=3`, return 3
2. Backtrack to `head=2`: `2.next.next = 2` (3 points to 2), `2.next = null`
3. Backtrack to `head=1`: `1.next.next = 1` (2 points to 1), `1.next = null`

Result: `3→2→1→null`

## Interview Key Points

- In the iterative solution, remember to save next — otherwise, you lose access to the remaining nodes after reversing
- In the recursive solution, the key line is `head.next.next = head`
- Know both approaches — interviewers often switch between them to test you