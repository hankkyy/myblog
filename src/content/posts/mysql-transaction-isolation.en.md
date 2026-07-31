---
lang: en
title: "MySQL Transaction Isolation Levels Explained for Interviews: How to Distinguish Dirty Reads, Phantom Reads, and Non-Repeatable Reads?"
date: 2025-03-25T10:00:00+08:00
categories: ['Database', 'Technology']
description: "Use real-world scenarios to explain the four isolation levels and three concurrency issues, so you'll never mix them up again."
---

Transaction isolation levels are almost a guaranteed question in MySQL interviews.

## Three Concurrency Issues

**Dirty Read**: Reading data that hasn't been committed by someone else. If they roll back, what you read is dirty data.
> Scenario: A transfers 100 yuan to B, but hasn't committed yet. B checks their balance and sees an extra 100. A rolls back. B's excitement was short-lived.

**Non-Repeatable Read**: Within the same transaction, reading the same row twice yields different results (someone else did an UPDATE).
> Scenario: Transaction A reads a balance of 500. Transaction B changes the balance to 600 and commits. Transaction A reads again, and it's now 600.

**Phantom Read**: Within the same transaction, a second query returns more rows than the first (someone else did an INSERT).
> Scenario: Transaction A queries all users with a balance greater than 500 and finds 3. Transaction B inserts a new user with a balance of 800. Transaction A queries again and now finds 4.

## Four Isolation Levels

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-------|------------|---------------------|--------------|
| Read Uncommitted | ✓ | ✓ | ✓ |
| Read Committed | ✗ | ✓ | ✓ |
| Repeatable Read (default) | ✗ | ✗ | Partially solved |
| Serializable | ✗ | ✗ | ✗ |

## How InnoDB Implements Repeatable Read

- **MVCC (Multi-Version Concurrency Control)**: Each transaction sees a "snapshot" rather than real-time data
- **Next-Key Lock**: Row lock + gap lock, solving the phantom read problem

## Interview Talking Points

> MySQL's default isolation level is Repeatable Read. It uses MVCC to implement snapshot reads, ensuring that data read within the same transaction is consistent. For write operations, it uses Next-Key Lock to prevent phantom reads—locking not only the queried rows but also the gaps between them.

Don't just memorize the table. If you can mention the two keywords MVCC and Next-Key Lock, the interviewer will know you truly understand.