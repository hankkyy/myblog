---
title: "Java 25 发布：虚拟线程稳定版、字符串模板正式 GA"
date: 2026-03-18T10:00:00+08:00
categories: ["技术"]
description: "Java 25 带来了虚拟线程正式版和字符串模板等重磅特性，Java 后端的性能又提升了一个台阶。"
---

Java 25 正式发布，几个特性很值得关注。

## 虚拟线程（Virtual Threads）正式 GA

虚拟线程在 Java 21 里是 Preview，现在已经稳定。

```java
// 以前：一个请求一个平台线程，线程池耗尽就阻塞
ExecutorService exec = Executors.newFixedThreadPool(200);

// 现在：一个请求一个虚拟线程，几乎没有限制
ExecutorService exec = Executors.newVirtualThreadPerTaskExecutor();
```

实测下来，同样的机器资源配置，使用虚拟线程后吞吐量提升了 3-5 倍。因为虚拟线程不占用 OS 线程，阻塞时会被自动挂起，释放底层平台线程。

## 字符串模板（String Templates）

告别 StringBuilder 地狱：

```java
// 以前
String sql = "SELECT * FROM users WHERE id = " + userId;

// 现在
String sql = STR."SELECT * FROM users WHERE id = \{userId}";
```

注意：字符串模板默认做了 SQL 注入防护，不同处理器有不同转义规则。

## 其他改进

- Pattern Matching 进一步完善
- Foreign Function & Memory API 正式 GA
- ZGC 分代模式默认开启

Java 这几年的演进速度真的快，跟上了云原生时代的需求。