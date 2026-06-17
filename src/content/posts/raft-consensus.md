---
title: "分布式共识算法：Raft 为什么比 Paxos 更好懂"
date: 2026-05-28T14:00:00+08:00
categories: ["分布式"]
description: "从 Leader 选举、日志复制到安全性保证，图解 Raft 共识算法"
---

分布式系统的核心难题：多个节点如何对一个值达成一致？Raft 是目前最流行的共识算法。

## Raft 的三个角色

```
┌──────────────────────────────────────┐
│  Leader   ← 处理所有客户端请求       │
│  Follower ← 被动响应 Leader          │
│  Candidate ← 选举中的临时状态        │
└──────────────────────────────────────┘
```

## Leader 选举

1. Follower 在 election timeout（150-300ms 随机）内没收到心跳 → 变成 Candidate
2. Candidate 给自己投一票，向所有节点发送 RequestVote
3. 获得多数票 → 成为 Leader，开始发送心跳
4. 票数相同 → 重新选举（随机超时避免死循环）

## 日志复制

```
Client → Leader: SET x = 1
Leader → Followers: AppendEntries(x=1, term=3, prevLogIndex=4)
Followers → Leader: ACK
Leader → Client: OK (多数确认后)
```

**关键**：Leader 只提交当前 term 的日志。这保证了安全性。

## Raft vs Paxos

| 维度 | Paxos | Raft |
|------|-------|------|
| 理解难度 | 非常高 | 相对低 |
| 工程实现 | 复杂 | 简单 |
| 日志连续性 | 允许空洞 | 严格连续 |
| 成员变更 | 复杂 | 两阶段 Joint Consensus |

## 实际应用

- **etcd**：K8s 的后端存储，使用 Raft
- **TiKV**：TiDB 的存储层
- **Consul**：HashiCorp 的服务发现

> Raft 的成功在于：用「可理解性」换来了「可实现性」。
