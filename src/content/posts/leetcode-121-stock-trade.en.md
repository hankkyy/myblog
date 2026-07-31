---
lang: en
title: "LeetCode 121/122/123. Stock Trading Series: Mastering Six Problems with One Framework"
date: 2026-04-08T10:00:00+08:00
categories: ['LeetCode']
description: "One framework to solve all six stock trading problems: from single transaction to unlimited transactions, including cooldown and transaction fees."
---

The stock trading series is one of the most classic problem sets on LeetCode, and a single DP framework solves them all.

## General Framework

`dp[i][k][0]` = maximum profit on day i, with at most k transactions completed, and not holding stock.
`dp[i][k][1]` = maximum profit on day i, with at most k transactions completed, and holding stock.

State transitions:
```
dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])
dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])
```

## 121. Buy and Sell Once (k=1)

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

## 122. Buy and Sell Unlimited Times (k=∞)

Greedy: buy whenever the next day's price is higher than the previous day's.

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

## 123. At Most Two Transactions (k=2)

Expand the states into 5: no transaction, first buy, first sell, second buy, second sell.

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

## Series Summary

| Problem | k | Additional Condition |
|---------|-----|---------------------|
| 121 | 1 | None |
| 122 | ∞ | None |
| 123 | 2 | None |
| 188 | k | None |
| 309 | ∞ | With cooldown |
| 714 | ∞ | With transaction fee |

Understand the general framework and all six problems are solved at once. No matter how the interviewer twists the questions, you'll be ready.