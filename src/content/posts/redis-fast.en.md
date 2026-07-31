---
lang: en
title: "Why Is Redis Fast? Analysis of Single-Threading, IO Multiplexing, and Data Structures"
date: 2026-06-09T10:00:00+08:00
categories: ["Technology"]
description: "Explaining the secret behind Redis's high performance from three perspectives: thread model, epoll, and efficient data structures"
---

Redis is single-threaded yet can handle 100,000 QPS. This article explains the design behind it.

## 1. Why Single-Threaded?

Redis chose single-threading not because it can't write multi-threaded code, but because **memory operations are so fast that multi-threading's context switching and lock contention actually slow things down**.

The execution path of a Redis command:
```
Parse command → Look up key → Execute operation → Return result
```

All are pure in-memory operations, taking microseconds. In comparison, thread switching takes 1-10 microseconds, and lock contention is even more expensive.

However, Redis 6.0 introduced **IO multi-threading** — network reads/writes can be multi-threaded, but command execution remains single-threaded.

## 2. IO Multiplexing: epoll

How does a single thread handle tens of thousands of client connections? The answer is epoll.

```python
# Pseudocode: epoll workflow
epoll_fd = epoll_create()
for client in clients:
    epoll_ctl(epoll_fd, ADD, client.fd, EPOLLIN)

while True:
    events = epoll_wait(epoll_fd, timeout=10)  # Blocking wait
    for fd, event in events:
        handle_client(fd)  # Only handle ready connections
```

Comparison:
- `select`: Iterates over all fds → O(n), max 1024
- `poll`: Iterates over all fds → O(n), no upper limit but not efficient
- `epoll`: Only returns ready fds → O(1), based on red-black tree + ready list

## 3. Efficient Data Structures

Redis is fast not just because of memory, but also because of cleverly designed data structures.

**SDS (Simple Dynamic String)**:
```c
struct sdshdr {
    int len;     // Used length
    int free;    // Remaining space
    char buf[];  // Actual data
};
```
- O(1) string length retrieval (C strings require O(n))
- Pre-allocated space reduces realloc calls
- Binary safe

**ziplist**: Contiguous memory storage saves pointer overhead. 5-10x more compact than linked lists for small data volumes.

**skiplist**: The underlying structure for ZSet, average O(log n), simpler to implement than balanced trees.

## 4. Performance Data

| Operation | Single-node QPS | P99 Latency |
|-----------|-----------------|-------------|
| GET | 120,000 | < 1ms |
| SET | 110,000 | < 1ms |
| INCR | 115,000 | < 1ms |
| LPUSH | 105,000 | < 1ms |

> Redis's speed is the result of "correct architectural choices × extreme data structure optimization," not something brute-force hardware scaling can match.