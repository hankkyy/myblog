---
lang: en
title: "Neovim Configuration Guide: Is the Terminal Editor Still Worth It in 2025?"
date: 2025-06-25T18:00:00+08:00
categories: ['Technology']
description: "Set up a modern Neovim development environment from scratch, covering LSP, autocompletion, file tree, and Git integration."
---

After using Neovim for a year, here are my configuration insights.

## Why Neovim

- Fast startup (50ms vs Code's 5s)
- Low memory usage (200MB vs Code's 1GB+)
- Pure keyboard operation, no mouse needed
- Config files are code, version-controllable
- Works on remote servers too

## Core Plugins

I don't use many plugins, but the ones I do are essential:

- Lazy.nvim: Plugin manager (replacing Packer)
- nvim-lspconfig: LSP configuration (code completion, go-to-definition, error diagnostics)
- nvim-cmp: Autocompletion engine
- Telescope: Fuzzy finder (files, symbols, Git)
- neo-tree: File explorer
- gitsigns: Git status display
- tokyonight: Color scheme

## Configuration Approach

Don't just copy someone else's config. The best way is:
1. Start with the minimum number of plugins
2. Find solutions when you hit pain points
3. Understand each plugin's configuration
4. Regularly clean up unused plugins

## Should VS Code Users Switch?

- If you often write code on remote servers → Highly recommended
- If you primarily write Java/C# → Skip it (IDEs are better)
- If you write Python/Go/Rust/JS → Worth trying
- If you pursue a "hands never leave the keyboard" experience → Must try

Neovim's learning curve is indeed steep, but once you get used to it, there's no going back.