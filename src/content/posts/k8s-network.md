---
title: "Kubernetes 网络模型：从 Pod 到 Service 的完整数据包旅程"
date: 2026-06-14T09:00:00+08:00
categories: ["技术"]
description: "追踪一个请求从外部进入 K8s 集群到 Pod 的完整网络路径"
---

Kubernetes 的网络模型是面试高频题，但很多人只是背了「每个 Pod 一个 IP」，实际数据包怎么走的并不清楚。

## K8s 网络的三层模型

```
┌─────────────────────────────────────────────┐
│  Node                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │  Pod A  │  │  Pod B  │  │  Pod C  │    │
│  │10.244.1.2│  │10.244.1.3│  │10.244.2.2│   │
│  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │            │            │          │
│  ┌────┴────────────┴────────────┴────┐     │
│  │         cni0 bridge               │     │
│  └────────────────┬──────────────────┘     │
│                   │                        │
│              ┌────┴─────┐                  │
│              │  eth0    │                  │
│              │10.0.0.5  │                  │
└──────────────┴──────────┴──────────────────┘
```

## 场景一：同节点 Pod 通信

Pod A (10.244.1.2) → Pod B (10.244.1.3)：

1. Pod A 发出包，目标 `10.244.1.3`
2. 包经过 veth pair 到达 `cni0` 网桥
3. cni0 查 ARP 表，发现目标在同一子网
4. **直接二层转发**，不经过 iptables

## 场景二：跨节点 Pod 通信

Pod A (Node1) → Pod C (Node2)：

1. Pod A 发包，目标 `10.244.2.2`
2. 到 cni0，发现目标不在本子网
3. 查路由表：`10.244.2.0/24 via 10.0.0.6`（Node2 的 IP）
4. 包被封装（VXLAN / IP-in-IP），发到 Node2
5. Node2 解封装，交给本地 cni0
6. cni0 转发给 Pod C

**关键点：Overlay 网络用 VXLAN 隧道封装，每个包多了 50 字节的 VXLAN 头。**

## 场景三：ClusterIP Service

```yaml
apiVersion: v1
kind: Service
spec:
  clusterIP: 10.96.0.1
  selector:
    app: nginx
```

请求 `10.96.0.1:80` → Pod B：

1. 包到达 iptables/netfilter
2. 命中 kube-proxy 写入的 DNAT 规则
3. 目标改写为 `10.244.1.3:80`
4. **随机选一个后端 Pod**（默认 iptables 概率模式）
5. 后续和正常 Pod 通信一样

**iptables 模式的缺点**：规则数量 O(n)，大量 Service 时性能下降。新版本推荐 **IPVS 模式**，用哈希表查找，O(1)。

## 场景四：外部流量 → NodePort → Pod

外部用户 → `NodeIP:30080` → Pod：

```
Client → NodeIP:30080
  → iptables DNAT → ClusterIP:80
    → iptables DNAT → PodIP:80
```

> 注意：如果 Pod 不在收到请求的节点上，iptables 还会加一层 SNAT，导致 Pod 里看到的源 IP 是 Node IP。设置 `externalTrafficPolicy: Local` 可以保留源 IP。

## 总结

| 场景 | 关键技术 | 性能 |
|------|----------|------|
| 同节点 Pod | veth + bridge | 最高 |
| 跨节点 Pod | VXLAN/Calico BGP | 中等 |
| ClusterIP | iptables/IPVS DNAT | 中等 |
| NodePort | iptables SNAT+DNAT | 较低 |
