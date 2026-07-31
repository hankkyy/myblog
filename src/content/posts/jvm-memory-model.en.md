---
lang: en
title: "JVM Memory Model Interview Guide: Heap, Stack, Method Area, and Metaspace"
date: 2025-02-20T09:00:00+08:00
categories: ['Technology']
description: "Break down the JVM runtime data area into several parts, using actual code examples to illustrate what each region stores."
---

The JVM memory model is the foundation for understanding how Java programs run.

## JVM Runtime Data Areas

```
┌─────────────────────────────┐
│     Method Area/Metaspace    │  ← Class info, constants, static variables
├─────────────────────────────┤
│            Heap              │  ← Object instances, arrays
├──────────┬──────────────────┤
│  VM Stack │  Native Method   │  ← Method calls, local variables
│           │      Stack       │
├──────────┴──────────────────┤
│        Program Counter       │  ← Current thread execution position
└─────────────────────────────┘
```

## Heap

- Stores all object instances and arrays
- Shared across threads
- Primary area for GC
- Generational: Young Generation (Eden + S0 + S1) + Old Generation

## VM Stack

- One stack per thread
- Each method call = one stack frame
- Stack frame contains: local variable table, operand stack, dynamic linking, return value
- StackOverflowError: stack depth exceeds limit (infinite recursion)
- OutOfMemoryError: stack memory exhausted

## Method Area → Metaspace

The method area (PermGen) in JDK 7 was removed in JDK 8 and replaced with Metaspace.

Metaspace uses native memory (not heap memory), which solves the OOM problem of PermGen. However, if the size is not limited (`-XX:MaxMetaspaceSize`), it can theoretically exhaust native memory as well.

## String Constant Pool

Starting from JDK 7, it was moved from the method area to the heap. Why? The GC trigger conditions for the method area are strict, and string constants are easier to reclaim in the heap.

## Interview Script

> JVM memory is divided into the heap and method area (Metaspace) shared by threads, as well as the stack and program counter that are private to each thread. The heap stores objects, and the stack stores method calls. In JDK 8, Metaspace replaced PermGen, using native memory to avoid OOM.

The key is being able to explain what each region stores and when OOM or StackOverflow might occur.