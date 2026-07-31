---
lang: en
title: "The Technical Decisions I Screwed Up Over the Years"
date: 2025-09-12T18:00:00+08:00
categories: ["Reflections"]
description: "Sharing some technical mistakes and lessons learned during my studies—falling into pitfalls is also part of growing."
---

Everyone makes mistakes. Here are a few of mine.

## 1. Blindly Chasing New Tech

In my sophomore year, I insisted on deploying a simple course project with K8s. I ended up spending two weeks configuring the environment and only half a day writing the code. When it came time to submit, the K8s setup broke, and I nearly failed the course.

Lesson: Choose the simplest solution that gets the job done. If a single JAR file plus one server can handle it, don't bring in K8s.

## 2. Dependency Injection Addiction

After learning Spring, I wanted to use dependency injection for everything. A CLI tool under 500 lines ended up with 3 interfaces and 5 implementation classes.

Lesson: If a simple `new` can solve it, don't over-engineer with DI. Not all code needs to be "enterprise-grade."

## 3. Comments That Say Nothing

```java
// Get user
public User getUser(Long id) { ... }
```

Comments like this are worthless.

Lesson: Good code doesn't need comments to explain "what" it does. Comments should explain "why"—why this algorithm? Why not consider caching?

## 4. Trying to Learn Too Much Too Soon

There was a period when I wanted to learn Rust, K8s, and machine learning all at once. I pursued three directions simultaneously and ended up mastering none of them.

Lesson: Focus on one thing at a time. Depth is far more valuable than breadth.

Making mistakes isn't scary. What's scary is repeating the same mistakes over and over.