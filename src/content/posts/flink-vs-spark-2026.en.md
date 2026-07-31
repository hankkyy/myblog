---
lang: en
title: "Getting Started with Real-Time Computing: How to Choose Between Flink and Spark Structured Streaming?"
date: 2026-02-10T13:00:00+08:00
categories: ["Technology", "Distributed Systems"]
description: "Learn the differences between Flink and Spark Structured Streaming, and understand their respective use cases."
---

I've been looking into real-time computing resources lately, comparing Flink and Spark Structured Streaming.

## Flink

- True stream processing, with each piece of data processed independently
- Very powerful state management
- A technology validated by Alibaba's Double 11 (Singles' Day)
- Steeper learning curve (many concepts like Watermark, Window)

## Spark Structured Streaming

- Underlying micro-batch processing, with slightly higher latency
- Strong SQL expression capabilities
- Good integration with the Spark ecosystem (MLlib, GraphX)
- Unified batch and stream processing with the same codebase

## Selection Considerations

- Pure real-time scenarios with millisecond-level latency requirements → Flink
- Mixed batch and stream processing, with a team experienced in Spark → Spark
- Want to deeply learn stream processing principles → Start with Flink
- Company has a Hadoop/Hive ecosystem → Spark is more natural

For learning purposes, it's recommended to understand both, as grasping the differences in their design philosophies is more important.

---

**References:**

- [Apache Flink](https://flink.apache.org/)
- [Apache Spark](https://spark.apache.org/)