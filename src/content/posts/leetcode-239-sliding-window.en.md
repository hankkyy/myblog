---
lang: en
title: "LeetCode 239. Sliding Window Maximum: A Classic Application of Monotonic Queue"
date: 2025-05-15T11:00:00+08:00
categories: ['LeetCode']
description: "Use a double-ended queue (Deque) to solve the sliding window maximum in O(n) time, and understand the core idea of a monotonic queue."
---

Sliding Window Maximum is a classic Hard problem, but solving it with a monotonic queue is very elegant.

## Problem

Given the array `nums = [1,3,-1,-3,5,3,6,7]` and `k = 3`, return the maximum value for each window: `[3,3,5,5,6,7]`.

## Brute Force Solution

Iterate through each window and find the maximum each time. Time complexity is O(n*k).

## Monotonic Queue Solution

Maintain a double-ended queue that stores indices (not values), keeping the queue in decreasing order from front to back.

When the window slides:
1. If the front element has slid out of the window, remove it
2. Starting from the back, remove all elements smaller than the current value
3. Add the current element to the back
4. The front element is the maximum of the current window

Each element is enqueued and dequeued at most once, so the time complexity is O(n).

## Code

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>(); // stores indices
    
    for (int i = 0; i < n; i++) {
        // 1. Remove elements outside the window
        if (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
            deque.pollFirst();
        }
        // 2. Maintain monotonic decreasing order
        while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) {
            deque.pollLast();
        }
        // 3. Add the current element
        deque.offerLast(i);
        // 4. Record the result
        if (i >= k - 1) {
            result[i - k + 1] = nums[deque.peekFirst()];
        }
    }
    return result;
}
```

## The Essence of a Monotonic Queue

A monotonic queue = queue + monotonicity. It is not an ordinary FIFO queue, but rather an "enhanced queue" that supports operations at both ends. This data structure is highly efficient for solving "sliding window extremum" type problems.

Similar problems: LeetCode 1438 (Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit), LeetCode 862 (Shortest Subarray with Sum at Least K).