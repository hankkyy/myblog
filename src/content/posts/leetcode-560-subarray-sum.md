---
title: "LeetCode 560. 和为 K 的子数组：前缀和 + HashMap 的巧妙组合"
date: 2025-09-10T14:00:00+08:00
categories: ['LeetCode']
description: "从 O(n²) 的暴力到 O(n) 的哈希表优化，理解前缀和这种「空间换时间」的经典技巧。"
---

和为 K 的子数组是一道非常好的 Medium 题，教会我们前缀和的妙用。

## 题目

给定数组 `[1,2,3]` 和 k=3，求连续子数组和为 3 的个数。答案是 2：`[1,2]` 和 `[3]`。

## 暴力解法 O(n²)

枚举所有子数组并求和。时间复杂度太高。

## 前缀和

前缀和 `prefix[i]` 表示 `nums[0]` 到 `nums[i-1]` 的和。

子数组 `nums[i..j]` 的和 = `prefix[j+1] - prefix[i]`。

所以问题转化为：找到有多少对 (i, j) 满足 `prefix[j] - prefix[i] = k`。

## 哈希表优化

遍历时维护一个 HashMap，key 是前缀和，value 是该前缀和出现的次数。

对于当前前缀和 `sum`，如果 `sum - k` 在 HashMap 中，说明之前出现过和为 `sum - k` 的前缀，那么中间那段的和就是 k。

## 代码

```java
public int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> map = new HashMap<>();
    map.put(0, 1); // 前缀和为 0 出现 1 次
    int sum = 0, count = 0;
    
    for (int num : nums) {
        sum += num;
        if (map.containsKey(sum - k)) {
            count += map.get(sum - k);
        }
        map.put(sum, map.getOrDefault(sum, 0) + 1);
    }
    return count;
}
```

## 为什么 map.put(0, 1)

想象数组第一个元素就等于 k。此时 `sum - k = 0`，我们需要有一个「前缀和为 0 出现了 1 次」的记录。

## 扩展

前缀和 + HashMap 是处理「子数组和」类问题的通用技巧。类似的题：
- LeetCode 974（和可被 K 整除的子数组）
- LeetCode 523（连续子数组和是 K 的倍数）

掌握这个技巧，能解决一类问题。
