---
lang: en
title: "System Design Interview: Designing a URL Shortening Service"
date: 2026-05-25T09:00:00+08:00
categories: ["System Design"]
description: "A complete design plan for a URL shortening service, from requirements analysis to database selection"
---

Almost every system design interview includes this question.

## Requirements Clarification

- **Functionality**: Long URL → Short URL, accessing the short URL → 302 redirect to the long URL
- **Scale**: 100 million new URLs per day, read-to-write ratio of 100:1
- **Short URL length**: 7 characters (62^7 ≈ 3.5 trillion, more than enough)

## Core Algorithm: Base62 Encoding

```python
CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def id_to_short(id: int) -> str:
    result = []
    while id > 0:
        result.append(CHARS[id % 62])
        id //= 62
    return "".join(reversed(result))
```

In distributed scenarios, use **Snowflake ID** to generate unique IDs, then encode them with Base62.

## Database Design

```sql
CREATE TABLE urls (
  id BIGINT PRIMARY KEY,
  short_key VARCHAR(10) UNIQUE NOT NULL,
  original_url TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_short_key ON urls(short_key);
```

**Why not use MySQL auto-increment IDs**: In distributed scenarios, multiple instances would cause conflicts.

## Caching Strategy

Read-heavy, write-light → **Use Redis to cache hot URLs**:

```
User accesses short URL → Redis GET → Hit? 302 redirect : Query MySQL → Write to Redis → 302
```

Caching strategy: LRU, with a 7-day expiration. It's estimated that 20% of URLs account for 80% of traffic.

## Key Numbers

| Metric | Value |
|--------|-------|
| Daily writes | 100 million |
| QPS (write) | ~1,200 |
| QPS (read) | ~120,000 |
| Storage (3 years) | ~30TB |
| Bandwidth | ~400Mbps |

> The essence of the URL shortening problem lies in "unique ID generation" + "caching strategy"; everything else is standard practice.