---
lang: en
title: "Rust Officially Enters the Linux Kernel Mainline — Is the Twilight of C Here?"
date: 2026-05-25T09:00:00+08:00
categories: ["Technology", "News"]
description: "Linux 6.15 kernel merges the Rust-implemented Ext4 filesystem driver, with Rust's share in the kernel exceeding 5% for the first time."
---

Linux 6.15 has officially merged the Rust-implemented Ext4 driver. This is the first production-grade filesystem driver written in Rust in the kernel.

## Why Rewrite Ext4 in Rust?

Ext4 is one of the most commonly used filesystems on Linux. Its C implementation has been maintained for over 20 years and the code is extremely complex. Over the past 5 years, more than 200 memory-safety-related vulnerabilities have been discovered.

Advantages of the Rust version:
- Eliminates use-after-free and buffer overflow at compile time
- The type system automatically handles concurrency safety
- Code size is 30% smaller than the C version (because extensive safety checks are no longer needed)

## How's the Performance?

Official benchmarks show the Rust version performs on par with the C version, and in certain scenarios (heavy small-file read/write workloads), Rust is actually 8% faster.

## Significance

This is more than just a technical issue. Linus previously said he "allows Rust into the kernel" but asked to "not force existing C developers to learn Rust." Now the Rust ecosystem has matured enough that many kernel subsystems are exploring Rust rewrites.

For Java backend developers like me, Rust may not directly replace Java, but understanding Rust's concepts (ownership, zero-cost abstractions) is also very helpful for writing high-performance Java code.

---

**References:**

- [Linux Kernel Mailing List — Rust for Linux](https://lore.kernel.org/rust-for-linux/)