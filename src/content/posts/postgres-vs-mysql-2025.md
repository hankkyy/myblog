---
title: "PostgreSQL 还是 MySQL？2025 年数据库选型的重新思考"
date: 2025-03-20T14:00:00+08:00
categories: ['数据库', '技术']
description: "从个人开发者和中小项目的角度，对比 PostgreSQL 和 MySQL 在 2025 年的差异和各自的优势场景。"
---

MySQL 和 PostgreSQL 的争论从来没有停过。2025 年了，情况有些变化。

## PostgreSQL 的优势

- **JSON 支持**：Postgres 的 JSONB 类型支持索引，查询性能比 MySQL 的 JSON 好很多
- **窗口函数**：更丰富的分析函数（但 MySQL 8.0+ 也追上来了）
- **地理空间**：PostGIS 扩展是地理数据处理的标准
- **并发控制**：MVCC 实现更干净，没有 MySQL 的间隙锁问题
- **SQL 标准**：对标准 SQL 的兼容更好

## MySQL 的优势

- **简单**：安装、配置、运维都更简单
- **生态**：几乎所有 ORM、框架都把 MySQL 作为第一选择
- **云服务**：各大云厂商的 MySQL 托管服务非常成熟
- **社区**：中文社区极其活跃，中文资料多
- **阿里/腾讯**：国内大厂的 MySQL 定制版（PolarDB、TDSQL）很强

## 怎么选

- 个人项目 / 快速原型 → MySQL（上手快，生态好）
- 复杂查询 / GIS / JSON 密集 → PostgreSQL
- 国内找工作 → MySQL（市场占有率绝对优势）
- 想学「正确」的 SQL → PostgreSQL

两个都值得学。先精通一个，另一个看看文档就能上手。
