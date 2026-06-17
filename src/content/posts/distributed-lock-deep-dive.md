---
title: "分布式锁的三代演进：从 Redis 到 Etcd 再到无锁设计"
date: 2025-03-15T10:00:00+08:00
categories: ["分布式", "技术"]
description: "深入分析分布式锁的三种实现方案及其优缺点，包括 Redlock 争议和 Etcd 租约机制。"
---

分布式锁看着简单，实际上坑很多。

## 第一代：Redis 分布式锁

```java
// 最常见的写法
String lockKey = "order:" + orderId;
boolean locked = redis.set(lockKey, uuid, "NX", "PX", 30000);
```

问题：
1. 锁过期时间不好设定——设短了业务还没执行完，锁就自动释放了；设长了，万一挂了要等很久
2. 主从切换时锁可能丢失

Martin Kleppmann 那篇著名的"Redlock 不安全"文章，导致很多人至今不敢在 Redis 上做分布式锁。

## 第二代：Etcd/Consul 分布式锁

利用 Etcd 的租约（Lease）机制：
- 客户端定期续约
- 客户端挂了租约自动过期
- Raft 保证一致性

缺点是性能不如 Redis，而且 Etcd 的瓶颈在写吞吐。

## 第三代：无锁设计

最好的分布式锁是不需要分布式锁。

一些思路：
- 幂等性设计（比如数据库唯一键 + 状态机）
- 乐观锁（版本号/CAS）
- 消息队列做串行化处理
- 数据库行级锁（比如 `SELECT ... FOR UPDATE`）

## 我的建议

能用数据库行级锁就别用分布式锁，能用无锁设计就别锁。实在需要分布式锁，选 Redis（接受可能偶尔失效）还是 Etcd（接受性能较低），看业务容忍度。