---
title: "LeetCode 215. 数组中的第 K 个最大元素：快选 vs 堆排"
date: 2026-02-12T15:00:00+08:00
categories: ['LeetCode']
description: "用快速选择（QuickSelect）和堆排序两种方法解 Top K 问题，理解各自的适用场景。"
---

第 K 大元素是高频面试题，考察 QuickSelect 算法。

## 题目

找数组中第 K 个最大的元素。比如 `[3,2,1,5,6,4]`，k=2，答案是 5。

## 解法一：堆排序 O(n log k)

```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>();
    for (int num : nums) {
        heap.offer(num);
        if (heap.size() > k) heap.poll();
    }
    return heap.peek();
}
```

维护一个大小为 k 的小顶堆。遍历完后堆顶就是第 k 大的元素。

## 解法二：快速选择 O(n) 平均

QuickSelect 是 QuickSort 的变体——不排序全部，只关注第 K 个。

```java
public int findKthLargest(int[] nums, int k) {
    return quickSelect(nums, 0, nums.length - 1, nums.length - k);
}

private int quickSelect(int[] nums, int left, int right, int target) {
    int pivot = nums[right];
    int i = left;
    for (int j = left; j < right; j++) {
        if (nums[j] <= pivot) {
            swap(nums, i, j);
            i++;
        }
    }
    swap(nums, i, right);
    
    if (i == target) return nums[i];
    else if (i < target) return quickSelect(nums, i + 1, right, target);
    else return quickSelect(nums, left, i - 1, target);
}
```

## 对比

| 方法 | 时间 | 空间 | 适用 |
|------|------|------|------|
| 堆 | O(n log k) | O(k) | k 很小 |
| QuickSelect | O(n) 平均 | O(1) | k 任意 |
| 全排序 | O(n log n) | O(1) | 简单但慢 |

## 面试怎么答

先说堆（最简单），再说 QuickSelect（优化），展示你的算法功底。如果面试官让你实现 QuickSelect，注意 pivot 的选择（可以用随机 pivot 避免最坏情况）。
