---
title: "作为 Java 开发者，我是怎么开始学 Rust 的"
date: 2025-02-05T14:00:00+08:00
categories: ['技术']
description: "从 Java 程序员的视角出发，理解 Rust 的所有权、借用的核心概念，对比两种语言的思维方式差异。"
---

最近开始学 Rust，作为写了几年 Java 的人，思维方式确实需要转换。

## 最大的不同：所有权

Java 的垃圾回收让我们习惯了「随便创建对象，GC 会处理」。Rust 让你自己管理内存，但编译器会帮你检查是否正确。

```rust
let s1 = String::from("hello");
let s2 = s1;  // s1 的所有权转移给了 s2
println!("{}", s1);  // 编译错误！s1 已经无效了
```

这跟 Java 完全不同——Java 里 `s1` 和 `s2` 可以指向同一个对象。

## 借用（Borrowing）

如果不想转移所有权，可以用引用（借用）：

```rust
let s1 = String::from("hello");
let s2 = &s1;  // s2 借用 s1，s1 依然有效
println!("{}", s1);  // 没问题
```

## Rust 对 Java 开发者的启发

即使不写 Rust，理解所有权和借用的概念能让你写出更好的 Java 代码：
- 更清楚对象的生命周期
- 更谨慎地处理可变状态
- 减少不必要的对象拷贝

## 学习建议

不要一上来就看《The Rust Book》，先看 Rustlings（互动式练习），跟着敲一遍。然后写一个小项目（命令行工具、简单的 HTTP 服务）。

Rust 的学习曲线比 Java 陡，但收获也比想象中大。
