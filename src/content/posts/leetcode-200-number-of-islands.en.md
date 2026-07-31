---
lang: en
title: "LeetCode 200. Number of Islands: A Template for DFS/BFS Traversal of 2D Grids"
date: 2025-10-22T10:00:00+08:00
categories: ['LeetCode']
description: "Solve the classic 'Islands Problem' with DFS and understand depth-first search in 2D grids. This template can solve 80% of grid-based problems."
---

Number of Islands is a classic application of DFS/BFS in 2D grids.

## Problem

Given a 2D grid, '1' represents land and '0' represents water. Count the number of islands (connected land cells form one island).

## DFS Solution

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
    
    grid[i][j] = '0';  // Mark as visited
    
    dfs(grid, i + 1, j);
    dfs(grid, i - 1, j);
    dfs(grid, i, j + 1);
    dfs(grid, i, j - 1);
}
```

## Why Not Use a Visited Array

By directly changing visited '1's to '0', we save extra space. This "in-place modification" is a very common technique.

## BFS Solution

Use a queue instead of recursion, with the same logic. The advantage of BFS is that it avoids stack overflow (though the grid in this problem won't be too large).

## Generic Grid DFS Template

```java
void dfs(int[][] grid, int r, int c) {
    if (!inArea(grid, r, c)) return;
    if (grid[r][c] != targetValue) return;
    
    grid[r][c] = markedValue;
    
    dfs(grid, r - 1, c);
    dfs(grid, r + 1, c);
    dfs(grid, r, c - 1);
    dfs(grid, r, c + 1);
}
```

## Similar Problems

- 695. Max Area of Island
- 463. Island Perimeter
- 130. Surrounded Regions (reverse thinking)
- 417. Pacific Atlantic Water Flow

Master this template = 10+ problems solved.