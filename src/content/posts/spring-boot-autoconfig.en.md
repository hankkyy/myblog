---
lang: en
title: "Spring Boot Auto-Configuration: What Does @SpringBootApplication Really Do?"
date: 2025-04-25T14:00:00+08:00
categories: ['Technology']
description: "Trace from the @SpringBootApplication annotation to the AutoConfiguration loading mechanism — a must-know for interviews."
---

Spring Boot's auto-configuration is a frequent interview topic. Many people can only say "convention over configuration," but freeze when asked about the underlying principles.

## The Three-in-One @SpringBootApplication

```java
@SpringBootConfiguration  // Equivalent to @Configuration
@EnableAutoConfiguration  // Entry point for auto-configuration
@ComponentScan            // Scans components
```

The key is `@EnableAutoConfiguration`.

## The Auto-Configuration Flow

1. `@EnableAutoConfiguration` imports `AutoConfigurationImportSelector`
2. It reads `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (the Spring Boot 3 approach)
3. This file lists all candidate auto-configuration classes (about 200 of them)
4. They are filtered through `@Conditional` annotations — loaded only if conditions are met

## The Magic of @Conditional

Spring Boot provides many conditional annotations:

- `@ConditionalOnClass`: Loads only if a certain class exists on the classpath. For example, `DataSourceAutoConfiguration` requires the DataSource class to be present
- `@ConditionalOnMissingBean`: Auto-creates a bean only if the user hasn't defined it themselves
- `@ConditionalOnProperty`: Loads only if a certain property exists in the configuration file

## How to Answer in an Interview

> Spring Boot triggers auto-configuration through `@EnableAutoConfiguration`. At startup, it scans the `AutoConfiguration.imports` file and decides whether to load a given auto-configuration class based on `@Conditional` condition annotations. The end result: you add `spring-boot-starter-web`, and it automatically configures DispatcherServlet, Tomcat, and Jackson for you.

## How to Verify Your Understanding

Create an empty Spring Boot project, open the `spring-boot-autoconfigure` jar, and take a look at what the `AutoConfiguration.imports` file looks like. Pick an auto-configuration class, click into it, and examine the @Conditional annotations on it.

Hands-on practice beats rote memorization every time.