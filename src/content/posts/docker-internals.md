---
title: "Docker 底层原理：Namespace、Cgroups 与 UnionFS"
date: 2026-05-20T16:00:00+08:00
categories: ["云原生"]
description: "容器不是轻量级虚拟机，而是被 Namespace 隔离、Cgroups 限制的普通进程"
---

很多人以为容器是「轻量级虚拟机」。其实容器就是一个普通进程，只是被 Linux 内核的隔离机制限制了视野。

## 三大利器

```
┌──────────────────────────────────────┐
│  Namespace  → 隔离（看到什么）        │
│  Cgroups    → 限制（能用多少）        │
│  UnionFS    → 分层（镜像怎么存）      │
└──────────────────────────────────────┘
```

## Namespace：进程的「牢笼」

```bash
# 查看某进程的 namespace
ls -la /proc/$(pidof nginx)/ns/
# PID  Namespace → 容器内 pid 1 就是宿主机的某个 pid
# NET  Namespace → 容器有独立网卡、IP、端口
# MNT  Namespace → 容器有自己的文件系统
# UTS  Namespace → 容器可以有自己的 hostname
```

## Cgroups：资源限制

```bash
# 限制内存 256MB
echo 268435456 > /sys/fs/cgroup/memory/docker/xxx/memory.limit_in_bytes
# 限制 CPU 50%
echo 50000 > /sys/fs/cgroup/cpu/docker/xxx/cpu.cfs_quota_us
```

Docker 通过 cgroup 保证容器不会吃掉宿主机所有资源。

## UnionFS：镜像分层

```
┌──────────┐
│  Container layer (R/W) │ ← 容器运行时的修改
├──────────┤
│  Layer 3: apt install nginx │
├──────────┤
│  Layer 2: COPY app /app │
├──────────┤
│  Layer 1: FROM ubuntu:22.04 │
└──────────┘
```

每一层只存储差异（delta），镜像复用节省磁盘。

## 一个容器启动到底做了什么

```
1. 创建 Namespace（PID/NET/MNT/UTS/IPC）
2. 设置 Cgroups 限制
3. pivot_root 切换根文件系统
4. 执行 entrypoint
```

> 理解了这三者，就理解了容器的本质。
