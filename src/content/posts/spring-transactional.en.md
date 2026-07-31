---
lang: en
title: "5 Scenarios Where @Transactional Fails: Why Your Transaction Didn't Roll Back?"
date: 2025-06-30T10:00:00+08:00
categories: ['Technology']
description: "A summary of the most common scenarios and reasons why Spring transaction annotations silently fail — knowledge useful for both interviews and real-world development."
---

@Transactional looks great, but there are several situations where it silently fails.

## 1. Self-Invocation Within the Same Class

```java
@Service
public class UserService {
    @Transactional
    public void createUser(User user) {
        // The transaction here will NOT take effect!
        this.saveUser(user);
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void saveUser(User user) {
        // ...
    }
}
```

Reason: Spring transactions are implemented through AOP proxies. Self-invocation within the same class bypasses the proxy.

Solution: Extract the method into a different Service, or use `AopContext.currentProxy()`.

## 2. Non-Public Methods

```java
@Transactional
private void saveUser() { }  // Transaction does NOT take effect!
```

AOP proxies can only intercept public methods.

## 3. Swallowed Exceptions

```java
@Transactional
public void createUser() {
    try {
        // Code that throws an exception
    } catch (Exception e) {
        log.error("Something went wrong", e);  // Transaction will NOT roll back!
    }
}
```

Transactions only roll back when an uncaught RuntimeException is thrown. If you catch the exception and don't rethrow it, it's pointless. You need to manually roll back inside the catch block:

```java
TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
```

## 4. Unsupported Database Engine

MyISAM does not support transactions. Adding @Transactional won't help.

## 5. Multithreading

```java
@Transactional
public void batchProcess() {
    new Thread(() -> {
        userMapper.insert(user);  // Not in the current transaction!
    }).start();
}
```

Transactions are bound to ThreadLocal, so a new thread cannot access the current transaction.

## Summary

Remember the two root causes: the limitations of AOP proxies + transactions being bound to ThreadLocal. All failure scenarios can be attributed to these two categories.