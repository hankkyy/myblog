---
title: "后端实习两个月，我学到的东西比大学两年都多"
date: 2026-06-08T20:00:00+08:00
categories: ["杂谈"]
description: "从学校到企业的落差、代码 Review 的残酷、以及为什么 CRUD 没那么简单"
---

在学校的时候，我以为后端开发就是 Spring Boot 连 MySQL，写几个 CRUD 接口。

实习两个月后，我发现 **CRUD 是工作中最简单的部分**。

## 学校不会教的事

### 1. 代码 Review 是真正的学习

学校作业交了就是交了，没人告诉你哪里写得烂。

公司的代码 Review：

```
「这个循环里查了 N 次数据库，改成批量查询」
「异常吞掉了，出问题没法排查」
「变量名 data 是什么意思？要写清楚是 orderData」
```

第一次被 Review 的时候，我的 PR 被打了 47 条 comment。脸很疼，但学的东西比之前两个月加起来都多。

### 2. 环境比代码难搞

写功能花 2 小时。配 Docker、配 Nginx、配 CI/CD、配监控告警、配日志采集……

花了两天。然后发现是配置文件里少了一个空格。

### 3. 沟通成本 > 编码成本

- 需求文档写得不清楚 → 来回确认 → 半天没了
- 接口格式没对齐 → 联调失败 → 又半天没了
- 数据库表结构改了没通知 → 线上炸了 → 一天没了

**「把话说清楚」是后端最被低估的能力。**

## 写 CRUD 也有讲究

你以为的 CRUD：

```java
@PostMapping("/order")
public Result createOrder(@RequestBody OrderDTO dto) {
    orderMapper.insert(dto);
    return Result.ok();
}
```

实际生产环境的 CRUD：

```java
@PostMapping("/order")
@Transactional(rollbackFor = Exception.class)
public Result createOrder(@Valid @RequestBody OrderDTO dto) {
    // 1. 参数校验 + 业务校验
    // 2. 幂等性检查（防止重复提交）
    // 3. 库存扣减（注意并发，用乐观锁）
    // 4. 创建订单
    // 5. 发送消息队列（异步通知）
    // 6. 记录操作日志
    // 7. 异常回滚 + 补偿逻辑
    return Result.ok(orderId);
}
```

一个「简单」的创建订单，实际要考虑：

- **事务边界**：哪些操作要原子？
- **幂等性**：用户点了两次怎么办？
- **并发安全**：库存超卖怎么处理？
- **失败补偿**：消息发失败了怎么恢复？

## 给也在实习的同学

1. **主动要 Code Review**——这是成长最快的方式
2. **问为什么**——不只问「怎么做」，更要问「为什么这样做」
3. **看老代码**——了解系统演进历史，比文档有用
4. **别怕犯错**——实习就是来犯错的，只要同一个错不犯两遍

> 企业代码和 LeetCode 的区别，就是生活和大富翁的区别。
