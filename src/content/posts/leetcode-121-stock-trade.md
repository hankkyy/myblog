---
title: "LeetCode 121/122/123. 股票买卖系列：从一道题到六道题的融会贯通"
date: 2026-04-08T10:00:00+08:00
categories: ['LeetCode']
description: "一个框架解决六道股票题：从只能买卖一次到任意次、含冷冻期、含手续费，一网打尽。"
---

股票买卖系列是 LeetCode 上最经典的一组题，一个 DP 框架解决所有。

## 通用框架

`dp[i][k][0]` = 第 i 天，最多完成 k 笔交易，不持有股票的最大利润。
`dp[i][k][1]` = 第 i 天，最多完成 k 笔交易，持有股票的最大利润。

状态转移：
```
dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])
dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])
```

## 121. 只能买卖一次（k=1）

```java
public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE, maxProfit = 0;
    for (int price : prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    return maxProfit;
}
```

## 122. 可以买卖无数次（k=∞）

贪心：只要后一天比前一天高就买。

```java
public int maxProfit(int[] prices) {
    int profit = 0;
    for (int i = 1; i < prices.length; i++) {
        if (prices[i] > prices[i-1])
            profit += prices[i] - prices[i-1];
    }
    return profit;
}
```

## 123. 最多交易两次（k=2）

把状态展开为 5 个：未交易、第一次买入、第一次卖出、第二次买入、第二次卖出。

```java
int buy1 = -prices[0], sell1 = 0;
int buy2 = -prices[0], sell2 = 0;
for (int price : prices) {
    buy1 = Math.max(buy1, -price);
    sell1 = Math.max(sell1, buy1 + price);
    buy2 = Math.max(buy2, sell1 - price);
    sell2 = Math.max(sell2, buy2 + price);
}
return sell2;
```

## 系列总结

| 题目 | k | 额外条件 |
|------|-----|---------|
| 121 | 1 | 无 |
| 122 | ∞ | 无 |
| 123 | 2 | 无 |
| 188 | k | 无 |
| 309 | ∞ | 含冷冻期 |
| 714 | ∞ | 含手续费 |

理解通用框架，六道题一次打通。面试官换着花样考你也不怕。
