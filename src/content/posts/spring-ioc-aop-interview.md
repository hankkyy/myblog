---
title: "Spring IoC 和 AOP 面试怎么答？不只是背概念"
date: 2025-01-25T10:00:00+08:00
categories: ['技术']
description: "从面试官的视角理解 Spring 的核心概念，用代码和场景解释 IoC 容器和 AOP 切面编程。"
---

Spring 的 IoC 和 AOP 是面试必考题。但大多数人只会背概念。

## IoC（控制反转）

面试官想听到的不仅是「控制反转就是把对象创建交给容器管理」。他要的是：

1. **为什么需要 IoC**：解耦。不用 new 依赖对象，通过配置或注解注入。
2. **DI 的三种方式**：构造器注入（推荐）、Setter 注入、字段注入（@Autowired）。
3. **Bean 的生命周期**：实例化 → 属性注入 → Aware 回调 → 初始化 → 使用 → 销毁。
4. **Bean 的作用域**：singleton（默认）、prototype、request、session。

加分项：能说清楚循环依赖怎么解决的——三级缓存。

## AOP（面向切面编程）

面试官想听的：

1. **AOP 解决什么问题**：横切关注点——日志、事务、权限校验。
2. **核心概念**：切面（Aspect）、连接点（Join Point）、通知（Advice）、切点（Pointcut）。
3. **代理模式**：JDK 动态代理（基于接口）vs CGLIB 代理（基于类继承）。
4. **实际应用**：`@Transactional` 就是通过 AOP 实现的，在方法前后开启/提交/回滚事务。

## 会动手比会背更重要

面试时如果能现场写一个简单的 AOP 切面来打印方法执行时间，印象分会高很多：

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

别只背八股文。写一遍就记住了。
