---
lang: en
title: "System Design Interview: Designing a Social Media News Feed"
date: 2025-08-22T14:00:00+08:00
categories: ['System Design', 'Technology']
description: "Using Twitter/Weibo as an example, break down the strategies for generating, pushing, and pulling a news feed, and understand the trade-offs between push-based and pull-based models."
---

The News Feed / Timeline is the core of social media and a classic system design interview question.

## Requirements

- Users see posts from people they follow
- Sorted in reverse chronological order
- Support images and videos
- Tens of millions of DAU

## Push Model vs Pull Model

**Push Model (Fan-out on Write)**:
- When a user posts, the post is pre-pushed to all followers' feeds
- Reading is done directly from Redis, O(1)
- Drawback: celebrities have hundreds of millions of followers, making write fan-out extremely costly

**Pull Model (Fan-out on Read)**:
- When a user views their feed, the latest posts from all followed users are pulled in real time
- Write operations are simple
- Drawback: the more people you follow, the slower the read operation

## Hybrid Model (the approach actually used)

- Regular users (few followers): use the push model, pushing posts to followers when they post
- Big influencers (many followers): use the pull model, pulling in real time when followers view their feed
- Final results are merged: pushed results + pulled results → sorted → returned

## Storage Design

- Post storage: MySQL sharded by database and table (sharded by user_id)
- Feed cache: Redis List (one Timeline per user, storing the most recent 1000 posts)
- Images/videos: CDN + object storage
- Hot data: posts from the last 3 days in Redis, older ones in MySQL

## Key Optimizations

- Pagination: use cursor instead of offset to avoid deep pagination issues
- Asynchronous: after posting, write first, then push to followers asynchronously in the background
- Deduplication: some followers may be both pushed to and pulled from, requiring merge and deduplication

## Interview Key Points

You must mention the hybrid model combining push and pull. This is the keyword the interviewer most wants to hear.