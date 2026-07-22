---
title: "数据库引擎的静默革命：B+Tree 统治四十年后，新玩家来了"
date: 2026-07-06T14:00:00+08:00
categories: ["数据库", "技术"]
description: "从 B+Tree 到 LSM、向量索引、学习索引——数据库索引结构正在经历四十年来最大的变化，而大多数 CRUD 程序员还没注意到。"
---

你有没有想过一个问题：为什么 MySQL 用 B+Tree、RocksDB 用 LSM Tree、向量数据库用 HNSW？

大多数后端程序员背了"最左前缀"和"回表查询"，但从来没想过：**为什么不同数据库选了不同的索引结构？如果换一种会怎样？**

这背后是数据库引擎层面正在发生的一场静默革命。

## B+Tree：四十年的老国王

B+Tree 的设计哲学是"读优化"：数据按顺序排列在磁盘页上，B+Tree 的每个节点刚好填满一个磁盘页。查找时从根遍历到叶子，磁盘 I/O 次数等于树的高度。

这个设计在机械硬盘时代是完美的——随机读写慢，顺序读写快。B+Tree 把数据紧挨着放，最大限度减少寻道。

但 SSD 改变了游戏规则。SSD 没有寻道时间，随机读和顺序读的差距大大缩小。B+Tree 最核心的优化假设被动摇了。

## LSM Tree：写入优先的反叛者

LSM（Log-Structured Merge-Tree）反着来：写入先到内存的 MemTable（跳表或红黑树），满了之后直接顺序刷盘成一个不可变的 SSTable 文件。后台线程定期合并这些文件。

结果是：**LSM 的写入比 B+Tree 快一个数量级，但读取要多检查几层 SSTable**。

RocksDB、Cassandra、Apache Doris 都基于 LSM。在日志、时序数据、IoT 等写入密集型场景下，LSM 是王者。

## 向量索引：AI 时代的新物种

过去两年最火的方向。传统索引回答"等于什么"或"在什么范围"，向量索引回答"和什么最像"。

FAISS、ScaNN、HNSW——这些算法正在从实验室走进数据库内核。pgvector 让 PostgreSQL 能做向量检索，Elasticsearch 和 Redis 也加了向量搜索。

我预测：5 年内，向量索引会和 B+Tree 一样平常。你今天随口说"给这个字段加个索引"，明天会说"给这段话加个向量索引"。

## 学习索引：用模型替代数据结构

2018 年 Jeff Dean 团队在 Google 提出了这个概念。核心想法很颠覆：B+Tree 本质上就是一个把 key 映射到位置的函数。既然这样，为什么不用一个小型神经网络来学习这个映射？

学习索引的空间效率极高——一个 B+Tree 可能几 MB，一个学习索引可能几十 KB。在嵌入式设备和边缘节点上，这是巨大的优势。

但目前还在学术界。最大挑战是数据更新——数据分布一变，模型就得重训。

## 为什么这很重要

大多数 CRUD 程序员一辈子只用 B+Tree，因为 MySQL 默认就是它。但了解这些方向有几个好处：

1. **选型有依据**。读多写少选 B+Tree，写多读少用 LSM，语义搜索加向量索引——每个选择都有代价和收益
2. **面试不怯场**。如果面试官问"MySQL 索引为什么用 B+Tree"，你能聊到 LSM、向量索引、学习索引，这比背八股高级太多
3. **看到趋势**。数据库是软件大厦的地基。地基在变，上层也会变

四十年的 B+Tree 垄断正在结束。不是说 B+Tree 会被淘汰——而是终于有了足够好的替代方案，让你可以根据场景做最优选择。这才是技术进步真正的模样。

---

**参考来源：**

- [Google AI — The Case for Learned Index Structures (Jeff Dean et al., 2018)](https://arxiv.org/abs/1712.01208)
- [Facebook Research — FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)
