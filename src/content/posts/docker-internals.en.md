---
lang: en
title: "Docker Under the Hood: Namespace, Cgroups, and UnionFS"
date: 2026-05-20T16:00:00+08:00
categories: ["Cloud Native"]
description: "Containers are not lightweight VMs, but ordinary processes isolated by Namespaces and constrained by Cgroups"
---

Many people think containers are "lightweight virtual machines." In reality, a container is just an ordinary process, only its view is restricted by the Linux kernel's isolation mechanisms.

## The Three Pillars

```
┌──────────────────────────────────────┐
│  Namespace  → Isolate (what you see)  │
│  Cgroups    → Limit (how much you use)│
│  UnionFS    → Layer (how images are stored)│
└──────────────────────────────────────┘
```

## Namespace: The Process's "Cage"

```bash
# View a process's namespaces
ls -la /proc/$(pidof nginx)/ns/
# PID  Namespace → PID 1 inside the container is just some PID on the host
# NET  Namespace → The container has its own network interface, IP, and ports
# MNT  Namespace → The container has its own filesystem
# UTS  Namespace → The container can have its own hostname
```

## Cgroups: Resource Limits

```bash
# Limit memory to 256MB
echo 268435456 > /sys/fs/cgroup/memory/docker/xxx/memory.limit_in_bytes
# Limit CPU to 50%
echo 50000 > /sys/fs/cgroup/cpu/docker/xxx/cpu.cfs_quota_us
```

Docker uses cgroups to ensure a container cannot consume all of the host's resources.

## UnionFS: Layered Images

```
┌──────────┐
│  Container layer (R/W) │ ← Modifications made during container runtime
├──────────┤
│  Layer 3: apt install nginx │
├──────────┤
│  Layer 2: COPY app /app │
├──────────┤
│  Layer 1: FROM ubuntu:22.04 │
└──────────┘
```

Each layer only stores the delta (differences). Image reuse saves disk space.

## What Happens When a Container Starts

```
1. Create Namespaces (PID/NET/MNT/UTS/IPC)
2. Set Cgroups limits
3. pivot_root to switch the root filesystem
4. Execute the entrypoint
```

> Understanding these three concepts is understanding the essence of containers.