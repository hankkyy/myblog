---
lang: en
title: "LeetCode 560. Subarray Sum Equals K: The Clever Combination of Prefix Sum + HashMap"
date: 2025-09-10T14:00:00+08:00
categories: ['LeetCode']
description: "From O(n²) brute force to O(n) hash map optimization, understand the classic 'space for time' technique of prefix sums."
---

Subarray Sum Equals K is an excellent Medium problem that teaches us the beauty of prefix sums.

## Problem

Given the array `[1,2,3]` and k=3, find the number of contiguous subarrays whose sum equals 3. The answer is 2: `[1,2]` and `[3]`.

## Brute Force Solution O(n²)

Enumerate all subarrays and compute their sums. The time complexity is too high.

## Prefix Sum

The prefix sum `prefix[i]` represents the sum of `nums[0]` through `nums[i-1]`.

The sum of subarray `nums[i..j]` = `prefix[j+1] - prefix[i]`.

So the problem transforms into: find how many pairs (i, j) satisfy `prefix[j] - prefix[i] = k`.

## Hash Map Optimization

While iterating, maintain a HashMap where the key is the prefix sum and the value is the number of times that prefix sum has occurred.

For the current prefix sum `sum`, if `sum - k` exists in the HashMap, it means a prefix with sum `sum - k` appeared before, so the sum of the segment in between equals k.

## Code

```java
public int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> map = new HashMap<>();
    map.put(0, 1); // prefix sum 0 occurs once
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

## Why map.put(0, 1)

Imagine the first element of the array equals k. At that point, `sum - k = 0`, so we need a record that "prefix sum 0 has occurred once."

## Extension

Prefix sum + HashMap is a general technique for handling "subarray sum" type problems. Similar problems include:
- LeetCode 974 (Subarray Sums Divisible by K)
- LeetCode 523 (Continuous Subarray Sum)

Mastering this technique allows you to solve a whole class of problems.