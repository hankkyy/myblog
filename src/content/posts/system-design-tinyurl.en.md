---
lang: en
title: "System Design Interview Guide: Designing a Short URL Service (TinyURL)"
date: 2025-04-18T16:00:00+08:00
categories: ['Distributed Systems', 'Technology']
description: "Breaking down a structured approach to system design interviews — requirements analysis, estimation, data modeling, API design, and scaling strategies."
---

Designing a short URL service is a classic system design interview question. Let's analyze it using a structured framework.

## 1. Requirements Clarification

Don't rush to draw diagrams — ask questions first:
- Is it only for short URL generation and redirects?
- Do we need click tracking?
- How many short URLs are generated per day?
- How long should the short URLs be?
- Do we need custom short URLs?

## 2. Rough Estimation

- 100 million new short URLs per day
- Read-to-write ratio: 100:1 (reads far exceed writes)
- 5-year storage: approximately 180 billion records
- Short URL length: 7 characters (base-62, 7 characters = 3.5 trillion combinations)

## 3. Short URL Generation Algorithms

- **Hash function (MD5/SHA256) taking the first N bits**: Simple but has collision risk
- **Auto-increment ID + Base62 encoding**: No collisions but depends on a counter
- **Pre-generation approach**: Batch-generate short codes in advance and store them in a pool

The most commonly used approach is the auto-increment ID scheme.

## 4. Data Model

- Short URL table: short_code (primary key), original_url, user_id, created_at, expires_at
- Access log table (optional): short_code, timestamp, ip, user_agent

## 5. Architecture Design

```
User → CDN → API Gateway → Short URL Service → Cache (Redis) → Database (MySQL)
                                    ↓
                              302 Redirect
```

## 6. Scaling Considerations

- Caching: Hot short URLs are cached in Redis
- Database sharding: Shard by short_code prefix
- Rate limiting: Prevent abuse by individual users

There is no single correct answer in a system design interview. What you demonstrate is your approach to analyzing the problem, not the final result.