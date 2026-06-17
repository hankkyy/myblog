---
title: "LeetCode 200. 岛屿数量：DFS/BFS 遍历二维网格的模板"
date: 2025-10-22T10:00:00+08:00
categories: ['LeetCode']
description: "用 DFS 解决经典的「岛屿问题」，理解二维网格中的深度优先搜索。这套模板能解决 80% 的网格题。"
---

岛屿数量是 DFS/BFS 在二维网格中的经典应用。

## 题目

给定二维网格，'1' 是陆地，'0' 是水。求岛屿数量（连通的陆地算一个岛）。

## DFS 解法

```java
public int numIslands(char[][] grid) {
    int count = 0;
    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == '1') {
                count++;
                dfs(grid, i, j);
            }
        }
    }
    return count;
}

private void dfs(char[][] grid, int i, int j) {
    if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length 
        || grid[i][j] != '1') return;
    
    grid[i][j] = '0';  // 标记为已访问
    
    dfs(grid, i + 1, j);
    dfs(grid, i - 1, j);
    dfs(grid, i, j + 1);
    dfs(grid, i, j - 1);
}
```

## 为什么不用 visited 数组

直接把访问过的 '1' 改成 '0'，省掉了额外空间。这种「原地修改」是很常见的技巧。

## BFS 解法

用队列代替递归，处理逻辑一样。用 BFS 的好处是不怕栈溢出（虽然这题网格不会太大）。

## 网格 DFS 通用模板

```java
void dfs(int[][] grid, int r, int c) {
    if (!inArea(grid, r, c)) return;
    if (grid[r][c] != 目标值) return;
    
    grid[r][c] = 标记值;
    
    dfs(grid, r - 1, c);
    dfs(grid, r + 1, c);
    dfs(grid, r, c - 1);
    dfs(grid, r, c + 1);
}
```

## 同类型题

- 695. 最大岛屿面积
- 463. 岛屿的周长
- 130. 被围绕的区域（反向思维）
- 417. 太平洋大西洋水流问题

掌握这套模板 = 10+ 道题。
