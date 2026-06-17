---
title: "LeetCode 239. 滑动窗口最大值：单调队列的经典应用"
date: 2025-05-15T11:00:00+08:00
categories: ['技术']
description: "用双端队列（Deque）在 O(n) 时间内解决滑动窗口最大值，理解单调队列的核心思想。"
---

滑动窗口最大值是一道经典的 Hard 题，但用单调队列来做非常优雅。

## 题目

给定数组 `nums = [1,3,-1,-3,5,3,6,7]` 和 `k = 3`，返回每个窗口的最大值：`[3,3,5,5,6,7]`。

## 暴力解法

遍历每个窗口，每次都找最大值。时间复杂度 O(n*k)。

## 单调队列解法

维护一个双端队列，队列里存的是索引（不是值），保持队列从大到小递减。

当窗口滑动时：
1. 如果队首元素已经滑出窗口，移除
2. 从队尾开始，把所有小于当前值的元素移出
3. 当前元素入队
4. 队首就是当前窗口的最大值

每个元素最多入队出队一次，所以是 O(n)。

## 代码

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>(); // 存索引
    
    for (int i = 0; i < n; i++) {
        // 1. 移除窗口外的元素
        if (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
            deque.pollFirst();
        }
        // 2. 维护单调递减
        while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) {
            deque.pollLast();
        }
        // 3. 当前元素入队
        deque.offerLast(i);
        // 4. 记录结果
        if (i >= k - 1) {
            result[i - k + 1] = nums[deque.peekFirst()];
        }
    }
    return result;
}
```

## 单调队列的本质

单调队列 = 队列 + 单调性。它不是普通意义的 FIFO 队列，而是能在两端进行操作的「加强版队列」。这种数据结构在解决「滑动窗口最值」类问题时非常高效。

类似的题：LeetCode 1438（绝对差不超过限制的最长连续子数组）、LeetCode 862（最短子数组）。
