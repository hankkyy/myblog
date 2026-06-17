---
title: "SQL 优化面试指南：从 EXPLAIN 到索引设计的实战思路"
date: 2025-05-20T16:00:00+08:00
categories: ['数据库', '技术']
description: "用实际慢 SQL 案例讲解 EXPLAIN 的输出字段和索引优化的核心原则。"
---

SQL 优化是后端面试的高频题，也是日常开发必备技能。

## EXPLAIN 核心字段

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 100 AND status = 'paid';
```

| 字段 | 含义 | 好的表现 |
|------|------|---------|
| type | 访问类型 | const > ref > range > index > ALL |
| key | 使用的索引 | 不是 NULL |
| rows | 扫描行数 | 越少越好 |
| Extra | 额外信息 | Using index（覆盖索引） |

## type 字段（从好到差）

- **const**：主键或唯一索引等值查询（最快）
- **ref**：非唯一索引等值查询
- **range**：索引范围查询（>、<、BETWEEN、LIKE 'abc%'）
- **index**：全索引扫描
- **ALL**：全表扫描（最差，必须优化）

## 索引设计原则

1. **最左前缀**：联合索引 `(a, b, c)` 只能用 `WHERE a = 1` 或 `WHERE a = 1 AND b = 2`
2. **高选择性**：字段的值越分散越好（性别只有男女，选择性低；用户 ID 有百万个，选择性高）
3. **避免索引失效**：
   - WHERE 中使用函数：`WHERE YEAR(create_time) = 2025` 不走索引
   - 隐式类型转换：`WHERE phone = 13800138000` 如果 phone 是 varchar，不走索引
   - OR 连接非索引列会导致全表扫描
4. **覆盖索引**：查询的列都在索引里，Using index，不回表

## 一个典型案例

```sql
-- 慢查询：type=ALL, rows=1000000
SELECT * FROM orders WHERE user_id = 123 ORDER BY create_time DESC LIMIT 10;

-- 优化：加联合索引
ALTER TABLE orders ADD INDEX idx_user_time (user_id, create_time);

-- 优化后：type=ref, rows=100, Extra=Using index
```

## 面试话术

> 遇到慢 SQL，先用 EXPLAIN 看访问类型和扫描行数。ALL 类型全表扫描必须优化。加索引的核心原则是最左前缀+高选择性。覆盖索引能避免回表，性能更好。最后用 profiles 对比优化前后的耗时。

会 EXPLAIN 比会写 SQL 更重要。
