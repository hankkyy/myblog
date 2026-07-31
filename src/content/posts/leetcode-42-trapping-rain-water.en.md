---
lang: en
title: "LeetCode 42. Trapping Rain Water: From Brute Force to Two Pointers"
date: 2026-01-15T15:00:00+08:00
categories: ['LeetCode']
description: "Three progressive solutions — brute force, dynamic programming, and two pointers — to understand how to optimize space complexity step by step."
---

Trapping Rain Water is a classic Hard problem, but once you understand it, the logic becomes very clear.

## Problem

Given `height = [0,1,0,2,1,0,1,3,2,1,2,1]`, find how much water can be trapped. The answer is 6.

## Core Idea

The amount of water a position can hold = `min(max height on the left, max height on the right) - current height`. If the result is negative, it means no water can be trapped (i.e., 0).

## Solution 1: Brute Force O(n²)

For each position, scan left and right to find the maximum heights. Too slow.

## Solution 2: Dynamic Programming O(n)/O(n)

Precompute two arrays:
- `leftMax[i]`: the maximum height to the left of position i
- `rightMax[i]`: the maximum height to the right of position i

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

## Solution 3: Two Pointers O(n)/O(1)

Key insight: we only care about the smaller of the two maximum heights on either side.

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

## Why Learn All Three Solutions

In interviews, start with the brute force approach to demonstrate your optimization thinking. Going from O(n²) → O(n)/O(n) → O(n)/O(1) is a perfect showcase of progressive problem-solving skills.