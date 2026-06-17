---
title: "Redis 为什么快？单线程、IO 多路复用与数据结构分析"
date: 2026-06-09T10:00:00+08:00
categories: ["技术"]
description: "从线程模型、epoll、高效数据结构三个层面解释 Redis 高性能的秘密"
---

Redis 单线程却能支撑 10 万 QPS。这篇文章解释背后的设计。

## 1. 为什么单线程？

Redis 选择单线程不是因为不会写多线程，而是**内存操作太快，多线程的上下文切换和锁竞争反而拖慢性能**。

一个 Redis 命令的执行路径：
```
解析命令 → 查找 key → 执行操作 → 返回结果
```

全部是纯内存操作，耗时微秒级。相比之下，线程切换需要 1-10 微秒，锁竞争更贵。

但 Redis 6.0 引入了**IO 多线程**——网络读写可以多线程，命令执行仍然是单线程。

## 2. IO 多路复用：epoll

单线程怎么处理几万个客户端连接？答案是 epoll。

```python
# 伪代码：epoll 工作流程
epoll_fd = epoll_create()
for client in clients:
    epoll_ctl(epoll_fd, ADD, client.fd, EPOLLIN)

while True:
    events = epoll_wait(epoll_fd, timeout=10)  # 阻塞等待
    for fd, event in events:
        handle_client(fd)  # 只处理就绪的连接
```

对比：
- `select`：遍历所有 fd → O(n)，最多 1024 个
- `poll`：遍历所有 fd → O(n)，无上限但不高效
- `epoll`：只返回就绪的 fd → O(1)，基于红黑树 + 就绪链表

## 3. 高效数据结构

Redis 快不只是因为内存，还因为数据结构设计得巧妙。

**SDS (Simple Dynamic String)**：
```c
struct sdshdr {
    int len;     // 已用长度
    int free;    // 剩余空间
    char buf[];  // 实际数据
};
```
- O(1) 获取字符串长度（C 字符串要 O(n)）
- 预分配空间，减少 realloc
- 二进制安全

**ziplist**：连续内存存储，省指针开销。小数据量时比链表紧凑 5-10 倍。

**skiplist**：ZSet 的底层结构，平均 O(log n)，实现比平衡树简单。

## 4. 性能数据

| 操作 | 单机 QPS | 延迟 P99 |
|------|----------|----------|
| GET | 120,000 | < 1ms |
| SET | 110,000 | < 1ms |
| INCR | 115,000 | < 1ms |
| LPUSH | 105,000 | < 1ms |

> Redis 的快是「正确的架构选择 × 极致的数据结构优化」的结果，不是蛮力堆机器能比的。
