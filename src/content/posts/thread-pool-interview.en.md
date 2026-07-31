---
lang: en
title: "Eight Key Thread Pool Interview Questions: Core Parameters, Rejection Policies, and Tuning Strategies"
date: 2025-07-05T14:00:00+08:00
categories: ['Technology']
description: "Explain the core parameters and execution flow of Java thread pools clearly, so you can answer interview questions with confidence."
---

Thread pools are a high-frequency topic in Java concurrency programming interviews.

## Seven Core Parameters

```java
new ThreadPoolExecutor(
    corePoolSize,   // Core thread count
    maximumPoolSize,// Maximum thread count
    keepAliveTime,  // Idle thread survival time
    unit,           // Time unit
    workQueue,      // Blocking queue
    threadFactory,  // Thread factory
    handler         // Rejection policy
)
```

## Execution Flow

1. When a task arrives, if the thread count is < corePoolSize, create a new thread to execute it
2. If corePoolSize is reached, place the task into the workQueue
3. If the workQueue is full, create new threads (up to maximumPoolSize)
4. If maximumPoolSize is reached, execute the rejection policy

## Common Blocking Queues

- **LinkedBlockingQueue** (default): Unbounded queue (theoretically), may cause OOM
- **ArrayBlockingQueue**: Bounded queue, capacity must be specified
- **SynchronousQueue**: Does not store tasks; they must be processed by a thread immediately upon submission

## Four Rejection Policies

- **AbortPolicy** (default): Throws an exception
- **CallerRunsPolicy**: The thread submitting the task executes it itself
- **DiscardPolicy**: Silently discards the task
- **DiscardOldestPolicy**: Discards the oldest task in the queue

## Pitfalls of ThreadPoolExecutor

The maximum thread count of `Executors.newCachedThreadPool()` is `Integer.MAX_VALUE`—effectively unlimited, which can create a massive number of threads and cause OOM in extreme cases.

Alibaba's coding guidelines explicitly prohibit creating thread pools with Executors; you must use `new ThreadPoolExecutor` with explicit parameters.

## How to Determine Thread Count

- CPU-intensive: N(CPU) + 1
- IO-intensive: N(CPU) * 2

But these are only empirical values. The best approach is load testing.

Thread pools are a must-know for every backend developer. If you cover these points thoroughly in an interview, you'll basically pass.