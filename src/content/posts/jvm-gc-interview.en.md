---
lang: en
title: "JVM Garbage Collection Interview Deep Dive: From CMS to G1 to ZGC"
date: 2025-05-25T09:00:00+08:00
categories: ['Technology']
description: "A breakdown of core JVM GC concepts and evolution history, so you can clearly explain the use cases for each garbage collector in interviews."
---

JVM garbage collection is a frequent topic in Java interviews. Don't just say "mark-and-sweep" anymore.

## Evolution of GC Algorithms

- **Mark-Sweep**: The simplest, but generates memory fragmentation
- **Mark-Compact**: Compacts memory after sweeping, solving the fragmentation issue
- **Mark-Copy**: Copies surviving objects to a new area, most efficient (used by the Young Generation)

## Generational Collection

The JVM divides the heap into the Young Generation and the Old Generation:
- Young Generation uses the copying algorithm (most objects die young)
- Old Generation uses the mark-compact algorithm

The Young Generation is further divided into Eden, Survivor0, and Survivor1. Objects are first allocated in Eden, and after surviving several GC cycles, they are promoted to the Old Generation.

## Classic GC Combinations

- **Serial + Serial Old**: Single-threaded, suitable for client-side applications
- **Parallel Scavenge + Parallel Old**: Multi-threaded, optimized for throughput
- **CMS + ParNew**: Low latency, but deprecated (removed in JDK 14)
- **G1**: Default since JDK 9, balances throughput and latency
- **ZGC**: Official release in JDK 15, sub-millisecond pause times (<1ms)
- **Shenandoah**: Contributed by Red Hat, similar to ZGC

## How to Answer in Interviews

1. Start with the basic purpose of GC: reclaiming unused objects and freeing memory
2. Then explain the principle of generational collection
3. Next, describe which scenarios the common GCs are suited for
4. Finally, mention why the upgrade from CMS to G1 was necessary (CMS's fragmentation issues, floating garbage)

## Bonus Points

Being able to explain G1's Region design—it doesn't have fixed Eden/Survivor/Old sizes, but instead uses multiple Regions for dynamic allocation. This makes G1's pause times predictable (by setting MaxGCPauseMillis).

GC is the foundation of Java performance tuning. Only by understanding GC logs can you diagnose why your production environment is lagging.