---
lang: en
title: "Two Months of Backend Internship Taught Me More Than Two Years of University"
date: 2026-06-08T20:00:00+08:00
categories: ["Musings"]
description: "The gap between school and the workplace, the brutality of code review, and why CRUD isn't as simple as it seems"
---

Back in school, I thought backend development meant connecting Spring Boot to MySQL and writing a few CRUD endpoints.

After two months of internship, I realized that **CRUD is the easiest part of the job**.

## What School Doesn't Teach You

### 1. Code Review Is Where the Real Learning Happens

School assignments are submitted and forgotten—nobody tells you where your code is bad.

Code review at a company:

```
"This loop hits the database N times—change it to a batch query."
"The exception is swallowed; you can't debug issues when something goes wrong."
"What does the variable name 'data' mean? Be specific—call it 'orderData'."
```

The first time I got reviewed, my PR received 47 comments. It stung, but I learned more from that than from the previous two months combined.

### 2. The Environment Is Harder Than the Code

Writing a feature took 2 hours. Setting up Docker, Nginx, CI/CD, monitoring alerts, and log collection...

Took two days. Then I found out there was a missing space in a config file.

### 3. Communication Costs > Coding Costs

- Unclear requirements doc → back-and-forth clarification → half a day gone
- Misaligned API formats → integration testing fails → another half day gone
- Database schema changed without notice → production breaks → a full day gone

**"Communicating clearly" is the most underrated skill in backend development.**

## There's More to CRUD Than Meets the Eye

What you think CRUD is:

```java
@PostMapping("/order")
public Result createOrder(@RequestBody OrderDTO dto) {
    orderMapper.insert(dto);
    return Result.ok();
}
```

What CRUD actually looks like in production:

```java
@PostMapping("/order")
@Transactional(rollbackFor = Exception.class)
public Result createOrder(@Valid @RequestBody OrderDTO dto) {
    // 1. Parameter validation + business validation
    // 2. Idempotency check (prevent duplicate submissions)
    // 3. Inventory deduction (watch for concurrency, use optimistic locking)
    // 4. Create the order
    // 5. Send to message queue (async notification)
    // 6. Log the operation
    // 7. Rollback on exception + compensation logic
    return Result.ok(orderId);
}
```

A "simple" create-order endpoint actually requires considering:

- **Transaction boundaries**: Which operations need to be atomic?
- **Idempotency**: What if the user clicks twice?
- **Concurrency safety**: How do you handle overselling inventory?
- **Failure compensation**: How do you recover if the message fails to send?

## For Fellow Interns

1. **Ask for code reviews proactively**—it's the fastest way to grow
2. **Ask why**—don't just ask "how," ask "why this approach"
3. **Read the legacy code**—understanding the system's evolution is more useful than documentation
4. **Don't be afraid to make mistakes**—internships exist for that, as long as you don't make the same mistake twice

> The difference between enterprise code and LeetCode is the difference between real life and Monopoly.