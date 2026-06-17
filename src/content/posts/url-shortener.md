---
title: "系统设计面试：设计一个 URL 短链接服务"
date: 2026-05-25T09:00:00+08:00
categories: ["系统设计"]
description: "从需求分析到数据库选型，完整的短链接服务设计方案"
---

几乎所有系统设计面试都会出现这道题。

## 需求澄清

- **功能**：长 URL → 短 URL，访问短 URL → 302 跳转到长 URL
- **规模**：日生成 1 亿条，读写比 100:1
- **短链接长度**：7 位字符（62^7 ≈ 3.5 万亿，够用）

## 核心算法：Base62 编码

```python
CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def id_to_short(id: int) -> str:
    result = []
    while id > 0:
        result.append(CHARS[id % 62])
        id //= 62
    return "".join(reversed(result))
```

分布式场景下，用 **Snowflake ID** 生成唯一 ID，再 Base62 编码。

## 数据库设计

```sql
CREATE TABLE urls (
  id BIGINT PRIMARY KEY,
  short_key VARCHAR(10) UNIQUE NOT NULL,
  original_url TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_short_key ON urls(short_key);
```

**为什么不用 MySQL 自增 ID**：分布式场景下多实例会冲突。

## 缓存策略

读多写少 → **Redis 缓存热点 URL**：

```
用户访问短链 → Redis GET → 命中？302跳转 : 查MySQL → 写Redis → 302
```

缓存策略：LRU，过期时间 7 天。预估 20% 的 URL 承担 80% 访问量。

## 关键数字

| 指标 | 数值 |
|------|------|
| 日写入量 | 1 亿 |
| QPS（写） | ~1,200 |
| QPS（读） | ~120,000 |
| 存储（3年） | ~30TB |
| 带宽 | ~400Mbps |

> 短链接问题的精髓在于「唯一 ID 生成」+「缓存策略」，其他都是常规操作。
