---
title: "我的终端工具链：2025 年开发效率套件分享"
date: 2025-04-05T12:00:00+08:00
categories: ['技术', '杂谈']
description: "分享日常开发中高频使用的终端工具，从文件管理到网络调试，提升工作效率。"
---

分享一下我日常高频使用的终端工具。

## 文件操作

- **fd**：比 find 更快更好用的文件搜索
- **ripgrep (rg)**：比 grep 快 10 倍的代码搜索
- **bat**：带语法高亮的 cat 替代品
- **fzf**：交互式模糊搜索，可以跟任何命令组合

## Git 增强

- **lazygit**：终端里的 Git GUI，处理 rebase、cherry-pick 特别方便
- **delta**：更好看的 git diff，带语法高亮
- **tig**：Git 仓库的文本界面浏览器

## JSON/数据处理

- **jq**：命令行 JSON 处理器，处理 API 返回的神器
- **fx**：交互式 JSON 查看器
- **xsv**：CSV 命令行工具

## 其他

- **tmux**：终端复用器，一个窗口分多个面板
- **htop**：漂亮的进程管理器
- **ncdu**：磁盘空间分析（图形化 du）
- **httpie**：比 curl 更好用的 HTTP 客户端（`http GET api.example.com`）

## 安装方式

macOS 上大部分可以通过 Homebrew 安装：`brew install fd ripgrep bat fzf lazygit jq tmux htop ncdu httpie`

这些工具的特点都是「做好一件事」。组合起来用，效率提升巨大。
