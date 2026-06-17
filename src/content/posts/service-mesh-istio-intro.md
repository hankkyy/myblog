---
title: "Service Mesh 入门：Istio 到底解决了什么问题？"
date: 2025-09-30T16:00:00+08:00
categories: ['云原生', '分布式', '技术']
description: "理解 Service Mesh 的核心概念——Sidecar、流量管理、可观测性，以及它和 API 网关的区别。"
---

Service Mesh 是微服务架构的下一阶段。Istio 是目前最流行的 Service Mesh 实现。

## 微服务通信的痛点

在微服务架构中，服务之间的通信变得复杂：
- 服务发现：A 怎么找到 B？
- 负载均衡：多个 B 实例怎么分配流量？
- 超时重试：B 挂了怎么办？
- 熔断降级：B 太慢了怎么办？
- 灰度发布：怎么把 10% 流量切到新版本？

以前这些逻辑要写在每个服务里。Service Mesh 把这部分剥离出来。

## Sidecar 模式

每个服务 Pod 旁边放一个 Sidecar 代理（Envoy）。所有进出流量都经过它：

```
Service A → Envoy Proxy → Envoy Proxy → Service B
```

应用代码不需要知道网络细节——Sidecar 帮你处理了。

## Istio 的架构

- **数据面**：Envoy（Sidecar），负责实际处理流量
- **控制面**：Istiod，配置和管理 Envoy
- **Ingress/Egress Gateway**：管理进出集群的流量

## 核心功能

**流量管理**：
- 金丝雀发布：把 5% 流量路由到新版本
- 故障注入：故意注入延迟测试容错
- 超时和重试策略

**可观测性**：
- 自动生成分布式追踪（Jaeger/Zipkin）
- 指标收集（Prometheus）
- 可视化（Kiali）

**安全**：
- 服务间的 mTLS（双向 TLS 加密）
- 基于身份的访问控制

## Istio vs API 网关

- API 网关是集群入口（南北流量）
- Service Mesh 是服务间通信（东西流量）

两者各司其职，可以同时使用。

## 学习建议

Istio 的概念很多，建议先在 Minikube 上搭一个 demo 环境，体验金丝雀发布和故障注入。动手比看书快得多。
