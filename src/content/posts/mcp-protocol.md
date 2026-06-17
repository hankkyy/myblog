---
title: "MCP 协议：让 LLM 安全调用外部工具的标准化方案"
date: 2026-06-03T14:00:00+08:00
categories: ["技术"]
description: "Model Context Protocol — Anthropic 开源的 AI 工具调用标准，解决了 Agent 与外部系统交互的碎片化问题"
---

MCP（Model Context Protocol）是 Anthropic 2024 年底开源的标准协议。它的核心目标：**让 LLM 和外部工具/数据源的交互有一个统一标准**。

## 问题

现在的 AI Agent 调用工具有多乱：

```
Claude → 自己的工具格式
GPT → Function Calling
开源模型 → 各家用各的
```

每个工具都要单独适配。MCP 要解决的问题：**就像 USB-C 统一了接口，MCP 统一了 AI 的工具调用协议**。

## 架构

```
┌──────────┐     MCP Protocol     ┌──────────────┐
│  Host    │◄────────────────────►│  MCP Server  │
│ (Claude  │   JSON-RPC over      │  (tools)     │
│  Desktop)│   stdio/HTTP          │              │
└──────────┘                      └──────────────┘
```

- **Host**：AI 应用（Claude Desktop、VS Code、自定义 App）
- **Client**：Host 内的协议实现
- **Server**：提供具体能力的服务（文件系统、数据库、API）

## 快速上手

```bash
# 安装 MCP 服务端
npx @anthropic/mcp-server-filesystem /path/to/allowed/dir

# Claude Desktop 配置
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@anthropic/mcp-server-filesystem", "/path"]
    }
  }
}
```

## 已有生态

| Server | 能力 |
|--------|------|
| filesystem | 读写文件 |
| github | 管理仓库/PR |
| postgres | 数据库查询 |
| slack | 发送消息 |
| puppeteer | 浏览器自动化 |

## 核心概念

- **Tools**：LLM 可调用的函数（`read_file`、`search_docs`）
- **Resources**：LLM 可读取的数据（文件内容、数据库记录）
- **Prompts**：预定义的 prompt 模板

## 为什么重要

之前 AI 工具调用是碎片化的——每个平台自己定义格式。MCP 让「一次编写，到处运行」在 AI 工具领域成为可能。

> 如果你在 2026 年做 AI Agent 开发，MCP 是绕不开的基础设施。
