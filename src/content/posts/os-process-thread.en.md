---
lang: en
title: "Operating System Interview Essentials: What's the Real Difference Between Processes and Threads?"
date: 2025-06-10T10:00:00+08:00
categories: ['Technology']
description: "From inter-process communication to thread synchronization, here are the most common operating system interview topics explained clearly in one go."
---

Processes and threads are the foundation of operating system interviews.

## Core Differences

| Feature | Process | Thread |
|---------|---------|--------|
| Resources | Independent memory space | Shares the process's memory |
| Creation Overhead | High (allocates memory, copies page tables) | Low |
| Communication | IPC (pipes, shared memory, etc.) | Directly reads/writes shared variables |
| Context Switch Overhead | High (switches page tables, flushes TLB) | Low |
| Independence | One crashing doesn't affect others | One thread OOMs, the entire process crashes |
| Scheduling | Scheduled by the OS | Scheduled by the OS (kernel threads) |

## Inter-Process Communication (IPC)

1. **Pipes**: One-way communication between parent and child processes, e.g., `ps aux | grep java`
2. **Message Queues**: Independent of processes, asynchronous communication
3. **Shared Memory**: Fastest but requires synchronization mechanisms
4. **Sockets**: Communication across networks

## Thread Synchronization

### synchronized (Java)

synchronized guarantees atomicity + visibility + ordering. The JMM happens-before principle: an unlock happens-before a subsequent lock on the same monitor.

### volatile

Guarantees visibility + ordering (prevents instruction reordering), but does not guarantee atomicity. Classic use case: the `instance` variable in a DCL singleton must be volatile.

### CAS (Compare And Swap)

Lock-free synchronization. `AtomicInteger` is built on CAS + spin loops. The ABA problem: a value changes from A to B and back to A, and CAS cannot detect the change. Solution: add a version number (`AtomicStampedReference`).

## Conditions for Deadlock

1. Mutual exclusion: resources cannot be shared
2. Hold and wait: holding resources while waiting for new ones
3. No preemption: others cannot forcibly take your resources
4. Circular wait: A waits for B, B waits for C, C waits for A

Breaking any one of these conditions is enough to avoid deadlock.

## Interview Talking Points

> A process is the smallest unit of resource allocation, while a thread is the smallest unit of CPU scheduling. Inter-process communication requires IPC, while threads directly share memory but need synchronization. The core of thread synchronization is ensuring atomicity, visibility, and ordering.

OS fundamentals determine how far you can go — when you optimize to the very end, you're always dealing with the operating system.