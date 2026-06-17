---
title: "Spring Boot 自动配置原理：@SpringBootApplication 到底做了什么？"
date: 2025-04-25T14:00:00+08:00
categories: ['技术']
description: "从 @SpringBootApplication 注解一路追踪到 AutoConfiguration 的加载机制，面试必考。"
---

Spring Boot 的自动配置是面试高频题。很多人只会说「约定大于配置」，但被追问原理就卡壳了。

## @SpringBootApplication 的三合一

```java
@SpringBootConfiguration  // 等价于 @Configuration
@EnableAutoConfiguration  // 自动配置的入口
@ComponentScan            // 扫描组件
```

关键是 `@EnableAutoConfiguration`。

## 自动配置的流程

1. `@EnableAutoConfiguration` 引入了 `AutoConfigurationImportSelector`
2. 它会读取 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`（Spring Boot 3 的写法）
3. 这个文件列出了所有候选的自动配置类（约 200 个）
4. 通过 `@Conditional` 注解过滤——满足条件才加载

## @Conditional 的魔法

Spring Boot 提供了很多条件注解：

- `@ConditionalOnClass`：类路径存在某个类才加载。比如 `DataSourceAutoConfiguration` 需要 DataSource 类存在
- `@ConditionalOnMissingBean`：用户没自己定义这个 Bean 才自动创建
- `@ConditionalOnProperty`：配置文件有某个属性才加载

## 面试怎么答

> Spring Boot 通过 `@EnableAutoConfiguration` 触发自动配置。启动时扫描 `AutoConfiguration.imports` 文件，根据 `@Conditional` 条件注解决定是否加载某个自动配置类。最终达到的效果是：你引入了 `spring-boot-starter-web`，它自动给你配好了 DispatcherServlet、Tomcat、Jackson。

## 怎么验证你的理解

创建一个空的 Spring Boot 项目，打开 `spring-boot-autoconfigure` jar 包，看看 `AutoConfiguration.imports` 文件长什么样。遇到一个自动配置类，点进去看看它上面的 @Conditional 注解。

动手远比背书有效。
