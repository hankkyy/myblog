---
lang: en
title: "LeetCode 215. Kth Largest Element in an Array: QuickSelect vs Heap Sort"
date: 2026-02-12T15:00:00+08:00
categories: ['LeetCode']
description: "Solve the Top K problem with two approaches — QuickSelect and Heap Sort — and understand when to use each."
---

The Kth largest element is a high-frequency interview question that tests the QuickSelect algorithm.

## Problem

Find the Kth largest element in an array. For example, given `[3,2,1,5,6,4]` and k=2, the answer is 5.

## Solution 1: Heap Sort O(n log k)

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

Maintain a min-heap of size k. After traversing the array, the top of the heap is the Kth largest element.

## Solution 2: QuickSelect O(n) Average

QuickSelect is a variant of QuickSort — instead of sorting everything, it only focuses on the Kth element.

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

## Comparison

| Method | Time | Space | Best For |
|--------|------|-------|----------|
| Heap | O(n log k) | O(k) | Small k |
| QuickSelect | O(n) average | O(1) | Any k |
| Full Sort | O(n log n) | O(1) | Simple but slow |

## How to Answer in an Interview

Start with the heap approach (simplest), then move to QuickSelect (optimized) to showcase your algorithmic skills. If the interviewer asks you to implement QuickSelect, pay attention to pivot selection (you can use a random pivot to avoid the worst case).