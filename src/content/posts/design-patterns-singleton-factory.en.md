---
lang: en
title: "Design Patterns Interview: 5 Ways to Write Singleton and Factory Pattern in Spring"
date: 2025-10-25T11:00:00+08:00
categories: ['Technology']
description: "The evolution of the Singleton pattern from eager initialization to enum, and the relationship between FactoryBean and BeanFactory."
---

The role of design patterns in interviews: proving you're not just a coder who only knows CRUD.

## 5 Ways to Write the Singleton Pattern

**1. Eager Initialization (Simplest)**
```java
public class Singleton {
    private static final Singleton INSTANCE = new Singleton();
    private Singleton() {}
    public static Singleton getInstance() { return INSTANCE; }
}
```
Disadvantage: It's created when the class is loaded. If it's never used, memory is wasted.

**2. Lazy Initialization (Has Thread Safety Issues)**
If two threads check `instance == null` simultaneously, two instances will be created.

**3. Double-Checked Locking (DCL, Most Common)**
```java
public class Singleton {
    private static volatile Singleton instance;  // volatile is very important!
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
`volatile` prevents instruction reordering — otherwise, you might get an object that hasn't been fully initialized.

**4. Static Inner Class (Recommended)**
Leverages the class-loading mechanism to ensure thread safety and lazy loading.

**5. Enum (Safest)**
```java
public enum Singleton {
    INSTANCE;
}
```
Prevents reflection attacks and serialization from breaking the singleton. This is the approach recommended by Joshua Bloch (author of *Effective Java*).

## Factory Pattern in Spring

- **BeanFactory**: The root interface of the Spring IoC container, the purest form of the factory pattern
- **FactoryBean**: Implement this interface when you need complex Bean creation logic (e.g., MyBatis's SqlSessionFactoryBean)
- Difference: BeanFactory manages all Beans, while FactoryBean is a factory that produces a specific Bean

## How to Answer in an Interview

Write the code first, then explain why it's written that way. Design patterns detached from code are just hollow theory.