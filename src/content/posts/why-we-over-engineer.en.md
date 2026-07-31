---
lang: en
title: "Why We Always Love Over-Engineering: Reflections from 'Hello World' to 'Microservices Architecture'"
date: 2025-03-08T20:00:00+08:00
categories: ['Reflections']
description: "A discussion on the phenomenon of over-engineering in the tech community, and why the simplest solution is often the best one."
---

Have you ever had this experience: you only needed a simple script, but ended up building an entire microservices architecture.

## Symptoms of Over-Engineering

1. **Premature Optimization**: With only 100 users right now, you're already thinking about handling tens of millions of concurrent requests
2. **Show-Off Tech Choices**: Using Kafka to replace a simple queue, or deploying a single-page app with Kubernetes
3. **Abstraction Hell**: Three layers of interfaces, five layers of inheritance, sacrificing readability for "extensibility"
4. **Tech Worship**: "Whatever solution the big tech companies use must be right"

## Why Simple Is Better

- Simple code is easier to understand and maintain
- Simple architectures cost less to debug
- Simple solutions iterate faster
- Simple doesn't mean crude—Antirez's Redis is extremely simple yet extremely powerful

## When Complexity Is Justified

- When you clearly know the scenarios you'll encounter within the next 6 months
- When you've already hit the bottleneck of your current solution
- When your team has the capability and willingness to maintain that complex solution

## My Principle

> Make it work, make it right, make it fast.

First get the code running, then make it correct, and finally make it fast. Most projects get stuck at the first step but are already thinking about the third.

Letting go of over-engineering is an important step toward becoming a mature programmer.