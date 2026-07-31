---
lang: en
title: "Rust for Java Programmers: A Deep Dive into Ownership"
date: 2026-06-16T10:00:00+08:00
categories: ["Technology"]
description: "Understanding Rust's ownership, borrowing, and lifetimes from a Java GC perspective"
---

Rust's ownership is the concept that gives Java programmers the most headaches. In Java, we just `new` things up, and the GC handles everything. Rust is completely different—**there's no GC; the compiler knows exactly when each piece of memory is freed at compile time**.

## The Java Perspective

```java
String s1 = new String("hello");
String s2 = s1;  // s1 and s2 point to the same object
// The GC reclaims memory when there are no more references
```

Java's approach: **reference counting + GC tracing**. Programmers don't think about memory; the runtime manages it for you.

## Rust's Approach

```rust
let s1 = String::from("hello");
let s2 = s1;       // Ownership of s1 moves to s2
// println!("{}", s1);  // Compile error! s1 is no longer valid
```

Rust's core rules:

1. **Every value has exactly one owner**
2. **When the owner goes out of scope, the value is dropped**
3. **Assignment/passing transfers ownership (move)**

## Why Did Rust Design It This Way?

Three words: **zero-cost abstraction**.

Java GC problems:
- Stop-the-world pauses
- Memory usage 30-50% higher than actually needed
- Unpredictable performance jitter

Rust's answer: **determine memory lifetimes at compile time, zero runtime overhead**.

## Borrowing: Access Without Transferring Ownership

```rust
fn print_len(s: &String) {  // Immutable borrow
    println!("len: {}", s.len());
}

let s = String::from("hello");
print_len(&s);    // Borrow, don't transfer ownership
println!("{}", s); // s is still usable
```

## Advice for Java Programmers

If you're coming from Java to Rust, learn in this order:

1. Forget inheritance first; embrace composition + traits
2. Accept that "the compiler is your friend"—every compile error is teaching you memory safety
3. `clone()` is your escape hatch—get the code running first, then optimize
4. Understand the difference between `String` vs `&str`, `Vec` vs `&[T]`

> Rust's learning curve is steep, but once you get over it, you'll start questioning why every line of Java code is slow.