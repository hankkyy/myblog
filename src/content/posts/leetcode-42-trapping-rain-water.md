---
title: "LeetCode 42. 接雨水：从暴力到双指针的思维提升"
date: 2026-01-15T15:00:00+08:00
categories: ['LeetCode']
description: "用三种解法层层递进——暴力、动态规划、双指针，理解如何一步步优化空间复杂度。"
---

接雨水是经典的 Hard 题，但理解后会发现思路非常清晰。

## 题目

给定 `height = [0,1,0,2,1,0,1,3,2,1,2,1]`，求能接多少雨水。答案是 6。

## 思路核心

每个位置能接的雨水量 = `min(左边最高, 右边最高) - 当前高度`。如果结果是负数，说明接不了水（为 0）。

## 解法一：暴力 O(n²)

对每个位置，向左向右扫描找最高。太慢。

## 解法二：动态规划 O(n)/O(n)

预处理两个数组：
- `leftMax[i]`：i 位置左边的最高
- `rightMax[i]`：i 位置右边的最高

```java
public int trap(int[] height) {
    int n = height.length;
    int[] leftMax = new int[n], rightMax = new int[n];
    leftMax[0] = height[0];
    rightMax[n-1] = height[n-1];
    
    for (int i = 1; i < n; i++)
        leftMax[i] = Math.max(leftMax[i-1], height[i]);
    for (int i = n-2; i >= 0; i--)
        rightMax[i] = Math.max(rightMax[i+1], height[i]);
    
    int result = 0;
    for (int i = 0; i < n; i++)
        result += Math.min(leftMax[i], rightMax[i]) - height[i];
    return result;
}
```

## 解法三：双指针 O(n)/O(1)

核心洞察：只关心左右两边较小的那个最大值。

```java
public int trap(int[] height) {
    int left = 0, right = height.length - 1;
    int leftMax = 0, rightMax = 0, result = 0;
    
    while (left < right) {
        leftMax = Math.max(leftMax, height[left]);
        rightMax = Math.max(rightMax, height[right]);
        
        if (leftMax < rightMax) {
            result += leftMax - height[left];
            left++;
        } else {
            result += rightMax - height[right];
            right--;
        }
    }
    return result;
}
```

## 为什么要会三种解法

面试时从暴力开始说，展示优化思路。从 O(n²) → O(n)/O(n) → O(n)/O(1)，这是一次完美的思维提升展示。
