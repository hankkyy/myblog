---
lang: en
title: "LeetCode 3. Longest Substring Without Repeating Characters: Sliding Window Template"
date: 2025-11-08T10:00:00+08:00
categories: ['LeetCode']
description: "Solve the longest substring without repeating characters using the sliding window template — once you master this, you can solve 90% of sliding window problems."
---

The longest substring without repeating characters is the entry-level sliding window problem and the most classic template problem.

## Problem

Given `"abcabcbb"`, find the length of the longest substring without repeating characters. The answer is 3 (`"abc"`).

## Sliding Window Template

```java
int left = 0, right = 0, maxLen = 0;
while (right < s.length()) {
    // 1. Expand the window: add the character at position right
    char c = s.charAt(right);
    right++;
    // Update window data...
    
    // 2. Shrink the window: when the window no longer satisfies the condition
    while (window needs shrinking) {
        char d = s.charAt(left);
        left++;
        // Update window data...
    }
    
    // 3. Update the answer
    maxLen = Math.max(maxLen, right - left);
}
```

## Solution for This Problem

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> window = new HashMap<>();
    int left = 0, right = 0, maxLen = 0;
    
    while (right < s.length()) {
        char c = s.charAt(right);
        right++;
        window.put(c, window.getOrDefault(c, 0) + 1);
        
        while (window.get(c) > 1) {
            char d = s.charAt(left);
            left++;
            window.put(d, window.get(d) - 1);
        }
        
        maxLen = Math.max(maxLen, right - left);
    }
    return maxLen;
}
```

## Problems That Use This Template

- 76. Minimum Window Substring (Hard)
- 438. Find All Anagrams in a String
- 567. Permutation in String
- 424. Longest Repeating Character Replacement

## The Core of the Template

Don't memorize the code — understand the meaning of the two while loops:
- Outer while: continuously expand the window to the right
- Inner while: when the window becomes invalid, shrink from the left

Every sliding window problem is a variation of this framework. Master it and you'll solve 15+ problems.