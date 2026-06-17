---
title: "Git 工作流最佳实践：从单人项目到团队协作"
date: 2025-04-28T09:00:00+08:00
categories: ['技术']
description: "从 commit message 规范到分支策略，整理一套适合个人开发者和中小团队的 Git 工作流。"
---

Git 用了很久，但好的习惯是逐渐养成的。

## Commit Message

推荐 Conventional Commits 规范：

```
feat: 新功能
fix: 修 bug
docs: 文档
refactor: 重构（不改变功能）
style: 代码格式
test: 测试
chore: 杂项（依赖更新等）
```

一个好的 commit message 应该回答「为什么改」而不是「改了什么」（代码本身已经说明了改了什么）。

## 分支策略

对于个人项目和 1-3 人的小团队：

- main：生产环境，只接受 PR
- dev：开发分支，日常提交
- feat/xxx：新功能分支，从 dev 切出，合并回 dev
- fix/xxx：修 bug 分支

不需要 GitFlow 那么复杂。分支越少越好，合并越频繁越好。

## Squash vs Merge

- Squash Merge：把多个 commit 压成一个，commit 历史干净
- Merge Commit：保留所有 commit，历史完整但比较乱

个人项目建议 Squash，团队项目看团队习惯。

## 一个实用的习惯

在 push 之前做一次 interactive rebase（`git rebase -i`），整理 commit 历史——把「fix typo」「再次修改」之类的合并掉。这会让你的 Git 历史像一本可读的故事书，而不是草稿纸。
