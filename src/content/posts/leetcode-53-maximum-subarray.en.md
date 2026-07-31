---
lang: en
title: "LeetCode 53. Maximum Subarray: The First Dynamic Programming Problem"
date: 2025-08-12T14:00:00+08:00
categories: ['LeetCode']
description: "Kadane's algorithm — solving the classic maximum subarray problem in O(n) time and O(1) space."
---

Maximum Subarray is a classic introductory problem for dynamic programming.

## Problem

Given `nums = [-2,1,-3,4,-1,2,1,-5,4]`, find the contiguous subarray with the largest sum. The answer is 6 (subarray `[4,-1,2,1]`).

## Greedy Approach

Traverse the array while maintaining the current subarray sum `curSum`:
- If `curSum + nums[i] < nums[i]`, the previous sum is a burden — start over
- Otherwise, add the current element

```java
public int maxSubArray(int[] nums) {
    int maxSum = nums[0];
    int curSum = nums[0];
    
    for (int i = 1; i < nums.length; i++) {
        curSum = Math.max(nums[i], curSum + nums[i]);
        maxSum = Math.max(maxSum, curSum);
    }
    return maxSum;
}
```

## Dynamic Programming Approach

`dp[i]` = the maximum subarray sum ending at `nums[i]`.

`dp[i] = max(nums[i], dp[i-1] + nums[i])`

The code is the same as the greedy approach — only the way we understand it differs.

## Divide and Conquer O(n log n)

We can also use divide and conquer: the maximum subarray either lies entirely in the left half, entirely in the right half, or crosses the midpoint. But the O(n) greedy/DP solution is already good enough.

## The Elegance of Kadane's Algorithm

It traverses only once, using O(1) extra space. The core idea: **when the accumulated sum becomes a burden, decisively discard it and start fresh**. This is not just an algorithm — it's also a life lesson.

## Extensions

LeetCode 152. Maximum Product Subarray: a similar idea, but you need to maintain both the maximum and minimum values (because a negative times a negative becomes positive).