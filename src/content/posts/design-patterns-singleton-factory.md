---
title: "设计模式面试：单例的 5 种写法和工厂模式在 Spring 中的应用"
date: 2025-10-25T11:00:00+08:00
categories: ['技术']
description: "单例模式从饿汉到枚举的演进，以及 FactoryBean 和 BeanFactory 的关系。"
---

设计模式在面试中的作用：证明你不是只会 CRUD 的码农。

## 单例模式的 5 种写法

**1. 饿汉式（最简单）**
```java
public class Singleton {
    private static final Singleton INSTANCE = new Singleton();
    private Singleton() {}
    public static Singleton getInstance() { return INSTANCE; }
}
```
缺点：类加载时就创建了，如果一直不用就浪费内存。

**2. 懒汉式（有线程安全问题）**
两个线程同时判断 `instance == null`，会创建两个实例。

**3. 双重检查锁（DCL，最常见）**
```java
public class Singleton {
    private static volatile Singleton instance;  // volatile 很重要！
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```
`volatile` 防止指令重排序——否则可能拿到一个未初始化完成的对象。

**4. 静态内部类（推荐）**
利用类加载机制保证线程安全和懒加载。

**5. 枚举（最安全）**
```java
public enum Singleton {
    INSTANCE;
}
```
防止反射攻击和序列化破坏单例。Joshua Bloch（《Effective Java》作者）推荐的方式。

## 工厂模式在 Spring 中

- **BeanFactory**：Spring IoC 容器的根接口，最纯粹的工厂模式
- **FactoryBean**：当你需要复杂的 Bean 创建逻辑时实现这个接口（比如 MyBatis 的 SqlSessionFactoryBean）
- 区别：BeanFactory 负责管理所有的 Bean，FactoryBean 是生产特定 Bean 的工厂

## 面试怎么答

先写代码，再解释为什么这样写。设计模式脱离代码就是空洞的理论。
