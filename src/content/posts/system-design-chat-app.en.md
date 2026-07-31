---
lang: en
title: "System Design Interview: Designing an Instant Messaging System (WhatsApp/WeChat)"
date: 2025-06-28T10:00:00+08:00
categories: ['System Design', 'Technology']
description: "From one-on-one chat to group chat, online status, and message reliability, break down the core design of an instant messaging system."
---

Designing an instant messaging system like WhatsApp or WeChat is a common question in system design interviews.

## Core Requirements

- One-on-one chat and group chat
- Message reliability (no message loss)
- Online status
- Message history
- Support 1 billion users

## Architecture Overview

```
Clients ←→ WebSocket persistent connection ←→ Chat Service
                                                    ↓
                                          Message Queue (Kafka)
                                                    ↓
                                          Message Storage (HBase/Cassandra)
```

## Why WebSocket Instead of HTTP Polling

HTTP polling has high latency and wastes bandwidth. With WebSocket, after establishing a persistent connection, the server can proactively push messages to clients. However, HTTP is acceptable for sending messages (it's simpler).

## Message Reliability

1. Client sends a message → Server returns an ACK
2. Server stores the message and pushes it to the recipient
3. Recipient returns an ACK
4. If no ACK is received, the server retries

For group chat, you only need to store the message once and use the "inbox" pattern — each user has their own message queue.

## Online Status

Users send a heartbeat every 30 seconds. The server records the last heartbeat time. If no heartbeat is received for more than 1 minute, the user is marked as offline.

## Storage Selection

- Message content: HBase or Cassandra (high-throughput writes sorted by time)
- User relationships and groups: MySQL
- Images/Videos: Object storage (S3/OSS) + CDN
- Recent message list: Redis

## Extensions

- End-to-end encryption (WhatsApp's Signal protocol)
- Message read receipts
- Message recall
- Multi-device sync

Instant messaging seems simple, but supporting hundreds of millions of users without losing messages is extremely complex.