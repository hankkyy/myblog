---
lang: en
title: "synchronized vs ReentrantLock: From Interview Questions to Source Code Implementation"
date: 2025-05-30T16:00:00+08:00
categories: ['Technology']
description: "Comparing the differences between Java's built-in lock and explicit lock, including lock upgrade process and AQS principles."
---

What's the difference between synchronized and ReentrantLock? Nine out of ten interviews ask this question.

## Usage Comparison

```java
// synchronized
synchronized (lock) {
    // critical section
}

// ReentrantLock
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();  // Must be released in finally!
}
```

## Core Differences

| Feature | synchronized | ReentrantLock |
|---------|-------------|---------------|
| Implementation | JVM built-in (monitorenter/exit) | JDK level (AQS) |
| Interruptible | Not supported | lockInterruptibly() |
| Timeout acquisition | Not supported | tryLock(time, unit) |
| Fair lock | Unfair | Can be fair or unfair |
| Multiple conditions | One condition queue | Multiple Conditions |
| Performance | Comparable after JDK 6+ optimization | About the same |

## Lock Upgrade in JDK 6

Before JDK 6, synchronized was a heavyweight lock (directly using OS mutex). JDK 6 introduced lock upgrade:

1. **No lock**: No thread contention
2. **Biased lock**: Same thread acquires multiple times, passes directly (CAS marks thread ID)
3. **Lightweight lock**: Multiple threads execute alternately (CAS spin)
4. **Heavyweight lock**: True blocking (OS level)

## ReentrantLock Under the Hood: AQS

ReentrantLock is based on AQS (AbstractQueuedSynchronizer). AQS maintains a state (volatile int) and a FIFO waiting queue.

- Locking: CAS changes state from 0 to 1
- Reentrancy: Same thread acquires again, state + 1
- Release: state - 1, when state reaches 0, wake up waiting threads

## When to Use ReentrantLock

- Need to try acquiring the lock (tryLock)
- Need an interruptible lock
- Need a fair lock (first come, first served)

Use synchronized whenever possible. The code is simpler, and the chance of errors is lower.