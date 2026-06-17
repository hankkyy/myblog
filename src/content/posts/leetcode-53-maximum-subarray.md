---
title: "LeetCode 53. 最大子数组和：动态规划入门第一题"
date: 2025-08-12T14:00:00+08:00
categories: ['LeetCode']
description: "Kadane 算法——用 O(n) 时间和 O(1) 空间解决经典的最大子数组和问题。"
---

最大子数组和（Maximum Subarray）是动态规划的经典入门题。

## 题目

给定 `nums = [-2,1,-3,4,-1,2,1,-5,4]`，找出和最大的连续子数组。答案是 6（子数组 `[4,-1,2,1]`）。

## 贪心思路

遍历数组，维护当前子数组和 `curSum`：
- 如果 `curSum + nums[i] < nums[i]`，说明之前的和是负担，重新开始
- 否则加上当前元素

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

## 动态规划思路

`dp[i]` = 以 `nums[i]` 结尾的最大子数组和。

`dp[i] = max(nums[i], dp[i-1] + nums[i])`

代码跟贪心一样，只是理解角度不同。

## 分治法 O(n log n)

也可以用分治：最大子数组要么在左半边、要么在右半边、要么跨越中点。但 O(n) 的贪心/DP 已经足够好了。

## Kadane 算法的精妙

只遍历一次，O(1) 额外空间。核心思想：**当之前的累加和成为负担时，果断舍弃，重新开始**。这不仅是算法，也是一种人生智慧。

## 扩展

LeetCode 152. 乘积最大子数组：类似的思路，但要同时维护最大值和最小值（因为负数乘以负数会变成正数）。
