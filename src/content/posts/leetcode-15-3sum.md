---
title: "LeetCode 15. 三数之和：排序+双指针的经典模板"
date: 2025-04-20T10:00:00+08:00
categories: ['LeetCode']
description: "从 O(n³) 暴力到 O(n²) 双指针，掌握这道常考题的三步优化思路。"
---

三数之和（3Sum）是面试高频题，核心是排序 + 双指针。

## 题目

给定 `nums = [-1,0,1,2,-1,-4]`，找出所有和为 0 的不重复三元组。答案：`[[-1,-1,2], [-1,0,1]]`。

## 解法演进

**暴力 O(n³)**：三重循环 — 太慢。

**哈希表 O(n²)/O(n)**：固定第一个数，剩下两个用两数之和的哈希表解法。但去重比较麻烦。

**排序+双指针 O(n²)/O(1)**：最优解。

## 代码

```java
public List<List<Integer>> threeSum(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(nums);
    
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue; // 去重
        if (nums[i] > 0) break; // 最小的都>0，不可能和为0
        
        int left = i + 1, right = nums.length - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                while (left < right && nums[left] == nums[left+1]) left++; // 去重
                while (left < right && nums[right] == nums[right-1]) right--;
                left++; right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    return result;
}
```

## 去重是关键

1. 外层：`if (i > 0 && nums[i] == nums[i-1]) continue` — 跳过重复的第一个数
2. 内层：找到解后跳过重复的 left 和 right

## 剪枝优化

`if (nums[i] > 0) break` — 排序后如果第一个数已经大于 0，后面不可能有解。

## 扩展

- LeetCode 18. 四数之和：再加一层循环
- LeetCode 16. 最接近的三数之和：不用找等于 0，找最接近 target 的

双指针的核心：排序后用首尾指针逼近目标值。
