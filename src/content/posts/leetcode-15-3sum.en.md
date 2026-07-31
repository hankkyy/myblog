---
lang: en
title: "LeetCode 15. 3Sum: The Classic Two-Pointer Template"
date: 2025-04-20T10:00:00+08:00
categories: ['LeetCode']
description: "From O(n³) brute force to O(n²) two pointers, master the three-step optimization approach for this frequently asked problem."
---

3Sum is a high-frequency interview question. The core approach is sorting + two pointers.

## Problem

Given `nums = [-1,0,1,2,-1,-4]`, find all unique triplets that sum to 0. Answer: `[[-1,-1,2], [-1,0,1]]`.

## Solution Evolution

**Brute force O(n³)**: Triple nested loops — too slow.

**Hash map O(n²)/O(n)**: Fix the first number, then solve the remaining two using the two-sum hash map approach. However, deduplication is cumbersome.

**Sorting + two pointers O(n²)/O(1)**: The optimal solution.

## Code

```java
public List<List<Integer>> threeSum(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(nums);
    
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue; // deduplicate
        if (nums[i] > 0) break; // smallest is > 0, sum can't be 0
        
        int left = i + 1, right = nums.length - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                while (left < right && nums[left] == nums[left+1]) left++; // deduplicate
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

## Deduplication is Key

1. Outer loop: `if (i > 0 && nums[i] == nums[i-1]) continue` — skip duplicate first numbers
2. Inner loop: after finding a solution, skip duplicate left and right values

## Pruning Optimization

`if (nums[i] > 0) break` — after sorting, if the first number is already greater than 0, no solution can exist beyond this point.

## Extensions

- LeetCode 18. 4Sum: Add one more nested loop
- LeetCode 16. 3Sum Closest: Instead of finding sum equal to 0, find the sum closest to target

The core of two pointers: after sorting, use left and right pointers to converge toward the target value.