---
lang: en
title: "Java 25 Released: Virtual Threads Stable, String Templates Officially GA"
date: 2026-03-18T10:00:00+08:00
categories: ["Technology"]
description: "Java 25 brings major features like the official release of virtual threads and string templates, taking Java backend performance to the next level."
---

Java 25 has been officially released, and several features are worth paying attention to.

## Virtual Threads Officially GA

Virtual threads were in Preview in Java 21 and are now stable.

```java
// Before: one request per platform thread, blocking when the thread pool is exhausted
ExecutorService exec = Executors.newFixedThreadPool(200);

// Now: one request per virtual thread, with virtually no limits
ExecutorService exec = Executors.newVirtualThreadPerTaskExecutor();
```

In real-world testing, with the same machine resource configuration, throughput improved by 3-5 times when using virtual threads. This is because virtual threads don't occupy OS threads—when blocked, they are automatically suspended, freeing up the underlying platform threads.

## String Templates

Say goodbye to StringBuilder hell:

```java
// Before
String sql = "SELECT * FROM users WHERE id = " + userId;

// Now
String sql = STR."SELECT * FROM users WHERE id = \{userId}";
```

Note: String templates include SQL injection protection by default, and different processors have different escaping rules.

## Other Improvements

- Pattern Matching further refined
- Foreign Function & Memory API officially GA
- ZGC generational mode enabled by default

Java's evolution pace in recent years has been remarkably fast, keeping up with the demands of the cloud-native era.

---

**References:**

- [OpenJDK — JEP Index](https://openjdk.org/jeps/)