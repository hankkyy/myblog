---
title: "Spring MVC 请求处理流程：从 DispatcherServlet 到视图渲染"
date: 2025-08-08T09:00:00+08:00
categories: ['技术']
description: "跟踪一个 HTTP 请求在 Spring MVC 中的完整处理路径，面试时可以画图解释。"
---

Spring MVC 的请求处理流程是经典面试题。

## 完整流程

```
HTTP 请求
    ↓
DispatcherServlet（前端控制器）
    ↓
HandlerMapping（找到处理器）
    ↓
HandlerAdapter（调用处理器）
    ↓
Handler（Controller 方法）
    ↓
ModelAndView（返回结果）
    ↓
ViewResolver（解析视图）
    ↓
View（渲染视图）
    ↓
HTTP 响应
```

## 每一步详解

**1. DispatcherServlet**：Spring MVC 的核心，所有请求的入口。它在 `web.xml` 或通过 `AbstractAnnotationConfigDispatcherServletInitializer` 配置。

**2. HandlerMapping**：根据请求 URL 找到对应的 Controller 方法。`@RequestMapping` 注解的信息就存在这里。常见的实现：`RequestMappingHandlerMapping`。

**3. HandlerAdapter**：调用 Handler 方法的适配器。因为 Handler 可能返回不同类型的值（ModelAndView、String、ResponseEntity 等），需要适配器做统一处理。

**4. ViewResolver**：把逻辑视图名（"userList"）解析为物理视图（"/WEB-INF/views/userList.jsp"）。

## 拦截器 vs 过滤器

- **过滤器（Filter）**：Servlet 层面的，在请求进入 DispatcherServlet 之前执行
- **拦截器（Interceptor）**：Spring 层面的，在 HandlerMapping 之后、HandlerAdapter 之前执行

## 面试话术

> 一个 HTTP 请求先到达 DispatcherServlet，它通过 HandlerMapping 找到对应的 Controller 方法，通过 HandlerAdapter 调用方法并处理返回值，最后通过 ViewResolver 解析视图或直接返回数据。

掌握这个流程是你理解「Spring Boot 背后发生了什么」的第一步。
