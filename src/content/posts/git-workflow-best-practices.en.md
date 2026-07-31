---
lang: en
title: "Git Workflow Best Practices: From Solo Projects to Team Collaboration"
date: 2025-04-28T09:00:00+08:00
categories: ['Technology']
description: "From commit message conventions to branching strategies, a practical Git workflow for individual developers and small to medium-sized teams."
---

I've been using Git for a long time, but good habits are developed gradually.

## Commit Messages

The Conventional Commits specification is recommended:

```
feat: New feature
fix: Bug fix
docs: Documentation
refactor: Refactoring (no functional changes)
style: Code formatting
test: Testing
chore: Miscellaneous (dependency updates, etc.)
```

A good commit message should answer "why it was changed" rather than "what was changed" (the code itself already shows what was changed).

## Branching Strategy

For personal projects and small teams of 1-3 people:

- main: Production environment, only accepts PRs
- dev: Development branch, for daily commits
- feat/xxx: Feature branches, branched from dev and merged back into dev
- fix/xxx: Bug fix branches

No need for something as complex as GitFlow. The fewer branches, the better; the more frequent the merges, the better.

## Squash vs Merge

- Squash Merge: Compresses multiple commits into one, keeping the commit history clean
- Merge Commit: Preserves all commits, with a complete but messier history

Squash is recommended for personal projects; for team projects, it depends on the team's preferences.

## A Practical Habit

Before pushing, do an interactive rebase (`git rebase -i`) to tidy up the commit history—squashing commits like "fix typo" or "another modification." This will make your Git history read like a storybook rather than a rough draft.