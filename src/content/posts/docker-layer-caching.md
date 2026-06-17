---
title: "Docker 镜像层缓存原理：为什么 COPY 顺序影响构建速度"
date: 2025-01-18T10:00:00+08:00
categories: ['技术']
description: "通过一个简单的 Spring Boot 项目，理解 Docker 层缓存的工作机制和最佳实践。"
---

Docker 的镜像层缓存是一个非常重要但容易被忽视的概念。

## 层是什么

Docker 镜像由多个只读层叠加而成。Dockerfile 中的每一行指令（FROM、RUN、COPY 等）都会创建一个新的层。这些层会被缓存——如果某一层没有变化，Docker 直接复用缓存，跳过重建。

## 一个典型案例

```dockerfile
# 不好的写法
COPY . /app
RUN mvn package

# 好的写法
COPY pom.xml /app
RUN mvn dependency:resolve
COPY src /app/src
RUN mvn package
```

为什么第二种写法更快？因为 `pom.xml` 变化频率远低于源码。先把依赖下载好并缓存住，每次改代码只需要重新编译，不用重新下载依赖。

## 关键原则

- 把变化频率低的操作放在前面（安装系统依赖、下载 Maven/npm 依赖）
- 把变化频率高的操作放在后面（COPY 源码、编译）
- 合理利用多阶段构建减小镜像体积

理解了层缓存，Docker 构建速度能提升数倍。
