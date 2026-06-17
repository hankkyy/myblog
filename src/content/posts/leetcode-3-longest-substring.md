---
title: "LeetCode 3. 无重复字符的最长子串：滑动窗口模板速通"
date: 2025-11-08T10:00:00+08:00
categories: ['LeetCode']
description: "用滑动窗口模板解决无重复字符的最长子串，一通百通——这套模板能解决 90% 的滑动窗口题。"
---

无重复字符的最长子串是滑动窗口的入门题，也是最经典的模板题。

## 题目

给定 `"abcabcbb"`，找出不含重复字符的最长子串长度。答案是 3（`"abc"`）。

## 滑动窗口模板

```java
int left = 0, right = 0, maxLen = 0;
while (right < s.length()) {
    // 1. 扩大窗口：加入 right 位置的字符
    char c = s.charAt(right);
    right++;
    // 更新窗口数据...
    
    // 2. 缩小窗口：当窗口不满足条件时
    while (窗口需要缩小) {
        char d = s.charAt(left);
        left++;
        // 更新窗口数据...
    }
    
    // 3. 更新答案
    maxLen = Math.max(maxLen, right - left);
}
```

## 本题代码

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

## 模板适用题

- 76. 最小覆盖子串（Hard）
- 438. 找到所有字母异位词
- 567. 字符串的排列
- 424. 替换后的最长重复字符

## 模板的核心

不要背代码，理解两个 while 的含义：
- 外层 while：不断向右扩展窗口
- 内层 while：当窗口不合法时，收缩左边

所有滑动窗口题都是这个框架的变形。掌握它就掌握了 15+ 道题。
