---
title: "Kubernetes HPA 自动伸缩深入理解：从 CPU 到自定义指标"
date: 2025-05-28T10:00:00+08:00
categories: ['云原生', '技术']
description: "理解 K8s Horizontal Pod Autoscaler 的工作原理和配置方法，实现真正的弹性伸缩。"
---

HPA（Horizontal Pod Autoscaler）是 K8s 中实现自动伸缩的核心组件。

## HPA 工作原理

```
Metrics Server → 采集 CPU/内存指标
       ↓
HPA Controller → 计算期望副本数
       ↓
Deployment → 调整 Pod 数量
```

## 基本配置

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 计算公式

期望副本数 = ceil(当前副本数 × (当前指标值 / 目标指标值))

如果 CPU 使用率是 140%，目标 70%，则期望副本数 = 2 × (140/70) = 4。

## 自定义指标

除了 CPU 和内存，还可以基于自定义指标伸缩：

```yaml
metrics:
- type: Pods
  pods:
    metric:
      name: http_requests_per_second
    target:
      type: AverageValue
      averageValue: "100"
```

## HPA 的局限性

1. **扩容延迟**：默认 15 秒检查一次，可能不够快
2. **缩容过快**：可能导致 Pod 被反复创建删除（抖动）
3. **只靠 CPU**：有些应用 CPU 不直接反映负载（比如 IO 密集型）

配合 KEDA（Kubernetes Event-driven Autoscaling）可以基于 Kafka 消息积压、Redis 队列长度等事件驱动伸缩。

## 实际建议

- 先观察应用的真实负载曲线，再设定 HPA 阈值
- 生产环境至少 minReplicas=3，避免单点
- 配合 PodDisruptionBudget 确保优雅缩容
