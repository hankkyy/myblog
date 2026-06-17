---
title: "AGENTS.md：给 AI 写一份项目说明书"
date: 2026-06-05T15:00:00+08:00
categories: ["技术"]
description: "为什么应该在每个项目里放一个 AGENTS.md 文件，以及怎么写"
---

如果你用 AI 辅助编程（Copilot、Cursor、Claude Code），有个简单但被低估的做法：**在项目根目录放一个 `AGENTS.md`**。

## 它是什么

`AGENTS.md` 是一份写给 AI 的项目说明书。放在项目根目录，AI 编程助手会自动读取它。

```markdown
# Project Name - Development Guide

## Build & Run
npm install && npm run dev

## Project Structure
src/ — 主代码
tests/ — 测试

## Conventions
- TypeScript strict mode
- 组件用 named export
```

## 为什么重要

没有 AGENTS.md，AI 会：

- 用错包管理器（`pip` vs `poetry`）
- 猜错你的代码风格（`snake_case` vs `camelCase`）
- 不知道测试怎么跑
- 搞不清项目结构

有 AGENTS.md，AI 开局就知道项目规则。

## 常见内容

```
1. 项目简介（一句话）
2. 环境要求（Node 20+, Python 3.11+）
3. 本地开发命令
4. 项目结构速览
5. 代码风格约定
6. Git 分支规范
7. 注意事项/坑
```

## 最佳实践

- **简短优先**：200-500 行最合适，太长 AI 可能不读完
- **具体不抽象**：写「组件放 `components/`，页面放 `pages/`」而不是「遵循关注点分离」
- **和 README 分开**：README 给人看，AGENTS.md 给 AI 看
- **放根目录**：AI 工具默认读取根目录的 `AGENTS.md` 或 `.cursorrules`

> 花 20 分钟写 AGENTS.md，等于给每个 AI 协作者做一次 onboarding。
