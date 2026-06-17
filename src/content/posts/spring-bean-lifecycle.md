---
title: "Spring Bean 生命周期：从实例化到销毁经历了什么？"
date: 2025-07-12T11:00:00+08:00
categories: ['技术']
description: "梳理 Spring Bean 从创建到销毁的完整生命周期，面试时可以画图回答。"
---

Spring Bean 的生命周期是面试的经典题。完整流程如下：

## 生命周期全流程

```
1. 实例化（Instantiation）
   → 调用构造方法创建对象
   
2. 属性赋值（Populate Properties）
   → 依赖注入（@Autowired 的字段被赋值）
   
3. BeanNameAware / BeanFactoryAware
   → 如果 Bean 实现了这些 Aware 接口，调用 setBeanName()、setBeanFactory()
   
4. BeanPostProcessor.postProcessBeforeInitialization
   → 初始化前的拦截点
   
5. InitializingBean.afterPropertiesSet()
   → 如果实现了 InitializingBean 接口

6. @PostConstruct 方法
   → 通常在这做初始化工作（推荐）

7. BeanPostProcessor.postProcessAfterInitialization
   → 初始化后的拦截点（AOP 代理在这里生成！）
   
8. 就绪（Bean is ready to use）

9. @PreDestroy / DisposableBean.destroy()
   → 销毁时的回调
```

## 面试时怎么答

不要一开始就背全部步骤。先说三个关键词：

> Bean 的生命周期分为三阶段：创建（实例化 + 属性注入）、初始化（@PostConstruct 等回调）、销毁（@PreDestroy）。其中最关键的是 BeanPostProcessor——AOP 就是通过它在初始化后生成代理对象的。

然后被追问再说详细步骤。

## 几个重要的点

- **BeanPostProcessor** 是最强大的扩展点——它可以修改任何 Bean（AOP、@Autowired 都是靠它实现的）
- **@PostConstruct > InitializingBean**：推荐用 @PostConstruct，代码侵入性更小
- 如果你自定义了一个 BeanPostProcessor，注意不要在里面执行耗时操作——每个 Bean 都会经过它

理解了 Bean 生命周期，Spring 的大部分「魔法」都能解释通了。
