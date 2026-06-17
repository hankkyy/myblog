---
title: "Apache Pulsar 入门：下一代消息队列有什么不一样？"
date: 2025-02-22T15:00:00+08:00
categories: ['分布式', '技术']
description: "了解 Pulsar 的架构设计——存算分离、分层存储、多租户，以及它和 Kafka 的核心差异。"
---

Apache Pulsar 被称为「下一代消息队列」，它和 Kafka 最大的区别是架构。

## 存算分离

Kafka 的数据存储在 Broker 本地磁盘上，Broker 既负责计算也负责存储。扩容时要同时考虑计算和存储。

Pulsar 把计算（Broker）和存储（BookKeeper）分开了：
- Broker：无状态，只负责消息路由和服务
- BookKeeper：负责持久化存储

这意味着你可以单独扩容 Broker（增加吞吐）或 BookKeeper（增加存储），不会互相影响。

## 多租户

Pulsar 原生支持多租户：一个集群可以服务多个团队/业务线，租户之间完全隔离。Kafka 在这方面主要靠命名约定来区分。

## 分层存储

Pulsar 可以把冷数据自动迁移到廉价存储（S3、HDFS），热数据留在 BookKeeper 里。这对长期存储场景（比如审计日志、合规数据）非常有用。

## 什么时候选 Pulsar

- 你需要在同一个集群里服务多个租户
- 消息需要长期存储
- 团队有专门的运维团队（Pulsar 的运维复杂度比 Kafka 高）

Kafka 依然是事实标准，但 Pulsar 在特定场景下确实更合适。
