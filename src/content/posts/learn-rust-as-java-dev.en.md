---
lang: en
title: "How I Started Learning Rust as a Java Developer"
date: 2025-02-05T14:00:00+08:00
categories: ['Technology']
description: "Understanding Rust's core concepts of ownership and borrowing from a Java programmer's perspective, comparing the differences in thinking between the two languages."
---

I recently started learning Rust, and as someone who has written Java for years, the shift in mindset is definitely necessary.

## The Biggest Difference: Ownership

Java's garbage collection makes us accustomed to "creating objects freely, GC will handle it." Rust requires you to manage memory yourself, but the compiler helps you check if it's correct.

```rust
let s1 = String::from("hello");
let s2 = s1;  // ownership of s1 is moved to s2
println!("{}", s1);  // compile error! s1 is no longer valid
```

This is completely different from Java—in Java, `s1` and `s2` can point to the same object.

## Borrowing

If you don't want to transfer ownership, you can use references (borrowing):

```rust
let s1 = String::from("hello");
let s2 = &s1;  // s2 borrows s1, s1 is still valid
println!("{}", s1);  // no problem
```

## What Rust Teaches Java Developers

Even if you don't write Rust, understanding the concepts of ownership and borrowing can help you write better Java code:
- Be clearer about object lifecycles
- Handle mutable state more carefully
- Reduce unnecessary object copying

## Learning Advice

Don't jump straight into *The Rust Book*. Start with Rustlings (interactive exercises) and work through them. Then write a small project (a command-line tool, a simple HTTP service).

Rust's learning curve is steeper than Java's, but the payoff is bigger than you'd expect.