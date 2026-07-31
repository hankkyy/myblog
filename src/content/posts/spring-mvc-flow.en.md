---
lang: en
title: "Spring MVC Request Handling Flow: From DispatcherServlet to View Rendering"
date: 2025-08-08T09:00:00+08:00
categories: ['Technology']
description: "Trace the complete processing path of an HTTP request in Spring MVC, and you can explain it with a diagram in interviews."
---

The request handling flow of Spring MVC is a classic interview question.

## Complete Flow

```
HTTP Request
    ↓
DispatcherServlet (Front Controller)
    ↓
HandlerMapping (Find the handler)
    ↓
HandlerAdapter (Invoke the handler)
    ↓
Handler (Controller method)
    ↓
ModelAndView (Return result)
    ↓
ViewResolver (Resolve the view)
    ↓
View (Render the view)
    ↓
HTTP Response
```

## Detailed Explanation of Each Step

**1. DispatcherServlet**: The core of Spring MVC and the entry point for all requests. It is configured in `web.xml` or via `AbstractAnnotationConfigDispatcherServletInitializer`.

**2. HandlerMapping**: Finds the corresponding Controller method based on the request URL. The information from the `@RequestMapping` annotation is stored here. A common implementation is `RequestMappingHandlerMapping`.

**3. HandlerAdapter**: An adapter that invokes the Handler method. Since a Handler may return different types of values (ModelAndView, String, ResponseEntity, etc.), the adapter handles them uniformly.

**4. ViewResolver**: Resolves a logical view name ("userList") into a physical view ("/WEB-INF/views/userList.jsp").

## Interceptor vs Filter

- **Filter**: Operates at the Servlet level and executes before the request enters DispatcherServlet
- **Interceptor**: Operates at the Spring level and executes after HandlerMapping but before HandlerAdapter

## Interview Talking Points

> An HTTP request first arrives at DispatcherServlet, which uses HandlerMapping to find the corresponding Controller method, invokes the method via HandlerAdapter and processes the return value, and finally resolves the view through ViewResolver or directly returns data.

Mastering this flow is your first step toward understanding "what happens behind the scenes in Spring Boot."