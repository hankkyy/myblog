---
title: "@Transactional 失效的 5 种场景：为什么你的事务没回滚？"
date: 2025-06-30T10:00:00+08:00
categories: ['技术']
description: "总结 Spring 事务注解最常见的失效场景和原因，面试和实际开发都会用到的知识。"
---

@Transactional 看起来很美好，但它有好几种情况会静默失效。

## 1. 同类方法调用

```java
@Service
public class UserService {
    @Transactional
    public void createUser(User user) {
        // 这里的事务不会生效！
        this.saveUser(user);
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void saveUser(User user) {
        // ...
    }
}
```

原因：Spring 事务是通过 AOP 代理实现的。同类方法调用绕过了代理。

解决：把方法拆到不同的 Service 里，或者用 `AopContext.currentProxy()`。

## 2. 非 public 方法

```java
@Transactional
private void saveUser() { }  // 事务不生效！
```

AOP 代理只能拦截 public 方法。

## 3. 异常被吞了

```java
@Transactional
public void createUser() {
    try {
        // 抛异常的代码
    } catch (Exception e) {
        log.error("出错了", e);  // 事务不会回滚！
    }
}
```

事务只在抛出未被捕获的 RuntimeException 时才回滚。你 catch 了又没抛出去，等于白搭。要在 catch 里手动回滚：

```java
TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
```

## 4. 数据库引擎不支持

MyISAM 不支持事务。你加了 @Transactional 也没用。

## 5. 多线程

```java
@Transactional
public void batchProcess() {
    new Thread(() -> {
        userMapper.insert(user);  // 不在当前事务中！
    }).start();
}
```

事务绑定在 ThreadLocal 上，新线程拿不到当前事务。

## 总结

记住两个根本原因：AOP 代理的局限 + 事务绑定在 ThreadLocal 上。所有失效场景都可以归到这两类。
