---
title: "Rust 写给 Java 程序员：所有权机制深度解析"
date: 2026-06-16T10:00:00+08:00
categories: ["技术"]
description: "从 Java GC 视角理解 Rust 的所有权、借用和生命周期"
---

Rust 的所有权（Ownership）是让 Java 程序员最头疼的概念。Java 里我们只管 `new`，GC 会处理一切。Rust 完全不同——**没有 GC，编译器在编译时就知道每块内存何时释放**。

## Java 的视角

```java
String s1 = new String("hello");
String s2 = s1;  // s1 和 s2 指向同一个对象
// GC 会在没有任何引用时回收内存
```

Java 的做法：**引用计数 + GC 追踪**。程序员不用想内存，运行时帮你管。

## Rust 的做法

```rust
let s1 = String::from("hello");
let s2 = s1;       // s1 所有权转移给 s2
// println!("{}", s1);  // 编译错误！s1 已失效
```

Rust 的核心规则：

1. **每个值有且只有一个所有者**
2. **所有者离开作用域，值被 drop**
3. **赋值/传参会转移所有权（move）**

## 为什么 Rust 要这样设计？

三个字：**零成本抽象**。

Java GC 的问题：
- Stop-the-world 停顿
- 内存占用比实际需要多 30-50%
- 不可预测的性能抖动

Rust 的答案：**编译期确定内存生命周期，运行时零开销**。

## 借用（Borrowing）：不转移所有权的访问

```rust
fn print_len(s: &String) {  // 不可变借用
    println!("len: {}", s.len());
}

let s = String::from("hello");
print_len(&s);    // 借出，不转移所有权
println!("{}", s); // s 仍然可用
```

## 对 Java 程序员的建议

如果你从 Java 转 Rust，按这个顺序学：

1. 先忘掉继承，拥抱组合 + trait
2. 接受「编译器是你朋友」——每次编译错误都在教你内存安全
3. `clone()` 是你的逃生舱——先让代码跑起来，再优化
4. 理解 `String` vs `&str`、`Vec` vs `&[T]` 的区别

> Rust 的学习曲线陡峭，但翻过去之后，你会开始质疑 Java 的每一行代码为什么慢。
