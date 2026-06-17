---
title: "线程池面试八连问：核心参数、拒绝策略和调优思路"
date: 2025-07-05T14:00:00+08:00
categories: ['技术']
description: "把 Java 线程池的核心参数和执行流程讲透，面试时对答如流。"
---

线程池是 Java 并发编程面试的高频题。

## 七个核心参数

```java
new ThreadPoolExecutor(
    corePoolSize,   // 核心线程数
    maximumPoolSize,// 最大线程数
    keepAliveTime,  // 空闲线程存活时间
    unit,           // 时间单位
    workQueue,      // 阻塞队列
    threadFactory,  // 线程工厂
    handler         // 拒绝策略
)
```

## 执行流程

1. 任务来了，如果线程数 < corePoolSize，创建新线程执行
2. 如果达到了 corePoolSize，任务放入 workQueue
3. 如果 workQueue 满了，创建新线程（不超过 maximumPoolSize）
4. 如果达到了 maximumPoolSize，执行拒绝策略

## 常见阻塞队列

- **LinkedBlockingQueue**（默认）：无界队列（理论上），可能导致 OOM
- **ArrayBlockingQueue**：有界队列，必须指定容量
- **SynchronousQueue**：不存储任务，提交后必须立刻被线程处理

## 四种拒绝策略

- **AbortPolicy**（默认）：抛异常
- **CallerRunsPolicy**：由提交任务的线程自己执行
- **DiscardPolicy**：直接丢弃
- **DiscardOldestPolicy**：丢弃队列最老的任务

## ThreadPoolExecutor 的坑

`Executors.newCachedThreadPool()` 的最大线程数是 `Integer.MAX_VALUE`——相当于没有上限，极端情况下会创建大量线程导致 OOM。

阿里规约明确禁止用 Executors 创建线程池，必须用 `new ThreadPoolExecutor` 显式传参。

## 线程数怎么定

- CPU 密集型：N(CPU) + 1
- IO 密集型：N(CPU) * 2

但这只是经验值。最好的方式是压测。

线程池是每个后端开发必须掌握的。面试把这几个点答全，基本就过关了。
