---
lang: en
title: "How to Answer Spring IoC and AOP Interview Questions? It's Not Just About Memorizing Concepts"
date: 2025-01-25T10:00:00+08:00
categories: ['Technology']
description: "Understand Spring's core concepts from an interviewer's perspective, explaining the IoC container and AOP with code and real-world scenarios."
---

Spring's IoC and AOP are must-know topics in interviews. But most people just memorize the concepts.

## IoC (Inversion of Control)

What interviewers want to hear isn't just "Inversion of Control means handing object creation to the container." They want:

1. **Why IoC is needed**: Decoupling. No need to `new` dependency objects—inject them via configuration or annotations.
2. **Three ways of DI**: Constructor injection (recommended), Setter injection, Field injection (`@Autowired`).
3. **Bean lifecycle**: Instantiation → Property injection → Aware callbacks → Initialization → Usage → Destruction.
4. **Bean scopes**: singleton (default), prototype, request, session.

Bonus points: Being able to explain how circular dependencies are resolved—the three-level cache.

## AOP (Aspect-Oriented Programming)

What interviewers want to hear:

1. **What problem AOP solves**: Cross-cutting concerns—logging, transactions, permission checks.
2. **Core concepts**: Aspect, Join Point, Advice, Pointcut.
3. **Proxy patterns**: JDK dynamic proxy (interface-based) vs CGLIB proxy (class-inheritance-based).
4. **Practical application**: `@Transactional` is implemented via AOP, opening/committing/rolling back transactions before and after method execution.

## Hands-On Skills Matter More Than Memorization

If you can write a simple AOP aspect on the spot during an interview to print method execution time, you'll score much higher:

```java
@Aspect
@Component
public class LoggingAspect {
    @Around("execution(* com.example.service.*.*(..))")
    public Object logTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        System.out.println(joinPoint.getSignature() + " took " + (System.currentTimeMillis() - start) + "ms");
        return result;
    }
}
```

Don't just memorize textbook answers. Write it once, and you'll remember it.