---
lang: en
title: "My Terminal Toolchain: 2025 Development Efficiency Suite"
date: 2025-04-05T12:00:00+08:00
categories: ['Technology', 'Random Thoughts']
description: "Sharing the terminal tools I use frequently in daily development, from file management to network debugging, to boost work efficiency."
---

Let me share the terminal tools I use frequently in my daily work.

## File Operations

- **fd**: A faster and better file search than `find`
- **ripgrep (rg)**: Code search that's 10x faster than `grep`
- **bat**: A `cat` replacement with syntax highlighting
- **fzf**: Interactive fuzzy search that can be combined with any command

## Git Enhancements

- **lazygit**: A Git GUI in the terminal, especially handy for rebase and cherry-pick
- **delta**: A prettier `git diff` with syntax highlighting
- **tig**: A text-mode interface browser for Git repositories

## JSON/Data Processing

- **jq**: Command-line JSON processor, a lifesaver for handling API responses
- **fx**: Interactive JSON viewer
- **xsv**: Command-line tool for CSV files

## Others

- **tmux**: Terminal multiplexer, split one window into multiple panes
- **htop**: A beautiful process manager
- **ncdu**: Disk space analyzer (a graphical `du`)
- **httpie**: A more user-friendly HTTP client than `curl` (`http GET api.example.com`)

## Installation

On macOS, most of these can be installed via Homebrew: `brew install fd ripgrep bat fzf lazygit jq tmux htop ncdu httpie`

The common trait of these tools is that they "do one thing well." Combined together, they bring a huge boost in efficiency.