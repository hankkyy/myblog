---
lang: en
title: "AGENTS.md: A Project Manual for AI"
date: 2026-06-05T15:00:00+08:00
categories: ["Technology"]
description: "Why you should put an AGENTS.md file in every project, and how to write one"
---

If you use AI-assisted programming (Copilot, Cursor, Claude Code), there's a simple but underrated practice: **put an `AGENTS.md` file in your project root**.

## What It Is

`AGENTS.md` is a project manual written for AI. Placed in the project root, AI coding assistants will automatically read it.

```markdown
# Project Name - Development Guide

## Build & Run
npm install && npm run dev

## Project Structure
src/ — main code
tests/ — tests

## Conventions
- TypeScript strict mode
- Components use named exports
```

## Why It Matters

Without AGENTS.md, AI will:

- Use the wrong package manager (`pip` vs `poetry`)
- Guess your code style incorrectly (`snake_case` vs `camelCase`)
- Not know how to run tests
- Get confused about the project structure

With AGENTS.md, AI knows the project rules from the start.

## Common Contents

```
1. Project overview (one sentence)
2. Environment requirements (Node 20+, Python 3.11+)
3. Local development commands
4. Quick project structure overview
5. Code style conventions
6. Git branch guidelines
7. Gotchas / pitfalls
```

## Best Practices

- **Keep it short**: 200-500 lines is ideal; if it's too long, AI might not read it all
- **Be specific, not abstract**: Write "components go in `components/`, pages go in `pages/`" instead of "follow separation of concerns"
- **Keep it separate from README**: README is for humans, AGENTS.md is for AI
- **Put it in the root**: AI tools read `AGENTS.md` or `.cursorrules` from the root by default

> Spending 20 minutes writing AGENTS.md is like onboarding every AI collaborator at once.

---

**References:**

- [Model Context Protocol Official Documentation](https://modelcontextprotocol.io/)