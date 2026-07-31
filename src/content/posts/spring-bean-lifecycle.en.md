---
lang: en
title: "Spring Bean Lifecycle: What Happens from Instantiation to Destruction?"
date: 2025-07-12T11:00:00+08:00
categories: ['Technology']
description: "A clear walkthrough of the complete Spring Bean lifecycle from creation to destruction — perfect for answering interview questions with a diagram."
---

The Spring Bean lifecycle is a classic interview question. Here's the complete flow:

## Full Lifecycle Flow

```
1. Instantiation
   → Constructor is called to create the object
   
2. Populate Properties
   → Dependency injection (fields annotated with @Autowired are assigned)
   
3. BeanNameAware / BeanFactoryAware
   → If the Bean implements these Aware interfaces, setBeanName() and setBeanFactory() are invoked
   
4. BeanPostProcessor.postProcessBeforeInitialization
   → Interception point before initialization
   
5. InitializingBean.afterPropertiesSet()
   → If the InitializingBean interface is implemented

6. @PostConstruct method
   → Typically used for initialization work here (recommended)

7. BeanPostProcessor.postProcessAfterInitialization
   → Interception point after initialization (AOP proxies are generated here!)
   
8. Ready (Bean is ready to use)

9. @PreDestroy / DisposableBean.destroy()
   → Callback during destruction
```

## How to Answer in an Interview

Don't recite all the steps at once. Start with three key phrases:

> The Bean lifecycle is divided into three phases: creation (instantiation + property injection), initialization (@PostConstruct and other callbacks), and destruction (@PreDestroy). The most critical part is BeanPostProcessor — AOP uses it to generate proxy objects after initialization.

Then go into the detailed steps if asked to elaborate.

## Key Points to Remember

- **BeanPostProcessor** is the most powerful extension point — it can modify any Bean (AOP and @Autowired are both implemented through it)
- **@PostConstruct > InitializingBean**: @PostConstruct is recommended because it's less invasive to your code
- If you define a custom BeanPostProcessor, avoid performing time-consuming operations inside it — every Bean passes through it

Once you understand the Bean lifecycle, most of Spring's "magic" becomes clear.