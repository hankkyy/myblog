---
lang: en
title: "Distributed Consensus: Why Raft Is Easier to Understand Than Paxos"
date: 2026-05-28T14:00:00+08:00
categories: ["Distributed Systems"]
description: "From Leader Election to Log Replication to Safety Guarantees — the Raft consensus algorithm explained with diagrams"
---

The core challenge of distributed systems: how do multiple nodes agree on a single value? Raft is currently the most popular consensus algorithm.

## Raft's Three Roles

```
┌──────────────────────────────────────┐
│  Leader   ← Handles all client requests│
│  Follower ← Passively responds to Leader│
│  Candidate ← Temporary election state  │
└──────────────────────────────────────┘
```

## Leader Election

1. A Follower receives no heartbeat within election timeout (randomized 150-300ms) → becomes Candidate
2. Candidate votes for itself, sends RequestVote to all nodes
3. Wins majority → becomes Leader, starts sending heartbeats
4. Split vote → re-election (randomized timeouts prevent loops)

## Log Replication

```
Client → Leader: SET x = 1
Leader → Followers: AppendEntries(x=1, term=3, prevLogIndex=4)
Followers → Leader: ACK
Leader → Client: OK (after majority confirmation)
```

**Key**: The Leader only commits logs from its current term. This guarantees safety.

## Raft vs Paxos

| Dimension | Paxos | Raft |
|------|-------|------|
| Understandability | Very hard | Relatively easy |
| Implementation | Complex | Straightforward |
| Log continuity | Gaps allowed | Strictly sequential |
| Membership changes | Complex | Two-phase Joint Consensus |

## Real-World Usage

- **etcd**: Kubernetes' backend store, uses Raft
- **TiKV**: TiDB's storage layer
- **Consul**: HashiCorp's service discovery

> Raft's success comes from trading "theoretical elegance" for "practical understandability."

---

**References:**

- [Diego Ongaro — Raft Consensus Algorithm (2014)](https://raft.github.io/)
