---
lang: en
title: "Distributed Consensus Algorithms: Why Raft Is Easier to Understand Than Paxos"
date: 2026-05-28T14:00:00+08:00
categories: ["Distributed Systems"]
description: "From Leader election and log replication to safety guarantees, an illustrated guide to the Raft consensus algorithm"
---

The core challenge of distributed systems: how can multiple nodes agree on a single value? Raft is currently the most popular consensus algorithm.

## The Three Roles in Raft

```
┌──────────────────────────────────────┐
│  Leader   ← Handles all client requests │
│  Follower ← Passively responds to Leader │
│  Candidate ← Temporary state during election │
└──────────────────────────────────────┘
```

## Leader Election

1. A Follower that receives no heartbeat within the election timeout (random 150-300ms) → becomes a Candidate
2. The Candidate votes for itself and sends RequestVote to all nodes
3. Receives a majority of votes → becomes Leader and starts sending heartbeats
4. Tie in votes → re-election (random timeouts prevent infinite loops)

## Log Replication

```
Client → Leader: SET x = 1
Leader → Followers: AppendEntries(x=1, term=3, prevLogIndex=4)
Followers → Leader: ACK
Leader → Client: OK (after majority acknowledgment)
```

**Key point**: The Leader only commits logs from the current term. This ensures safety.

## Raft vs Paxos

| Dimension | Paxos | Raft |
|------|-------|------|
| Ease of understanding | Very high difficulty | Relatively low |
| Engineering implementation | Complex | Simple |
| Log continuity | Allows gaps | Strictly continuous |
| Membership changes | Complex | Two-phase Joint Consensus |

## Real-World Applications

- **etcd**: Backend storage for K8s, uses Raft
- **TiKV**: Storage layer for TiDB
- **Consul**: HashiCorp's service discovery

> Raft's success lies in: trading "understandability" for "implementability."

---

**References:**

- [Diego Ongaro — Raft Consensus Algorithm (2014)](https://raft.github.io/)