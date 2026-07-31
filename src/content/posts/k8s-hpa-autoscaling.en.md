---
lang: en
title: "Deep Dive into Kubernetes HPA Autoscaling: From CPU to Custom Metrics"
date: 2025-05-28T10:00:00+08:00
categories: ['Cloud Native', 'Technology']
description: "Understand how the K8s Horizontal Pod Autoscaler works and how to configure it for true elastic scaling."
---

HPA (Horizontal Pod Autoscaler) is the core component for implementing autoscaling in K8s.

## How HPA Works

```
Metrics Server → Collects CPU/memory metrics
       ↓
HPA Controller → Calculates desired replica count
       ↓
Deployment → Adjusts the number of Pods
```

## Basic Configuration

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

## Calculation Formula

Desired replicas = ceil(current replicas × (current metric value / target metric value))

If CPU utilization is 140% and the target is 70%, then desired replicas = 2 × (140/70) = 4.

## Custom Metrics

In addition to CPU and memory, you can also scale based on custom metrics:

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

## Limitations of HPA

1. **Scaling latency**: It checks every 15 seconds by default, which may not be fast enough
2. **Rapid downscaling**: Can cause Pods to be repeatedly created and deleted (flapping)
3. **CPU-only focus**: For some applications, CPU doesn't directly reflect load (e.g., I/O-intensive workloads)

Combining HPA with KEDA (Kubernetes Event-driven Autoscaling) enables event-driven scaling based on Kafka message backlog, Redis queue length, and more.

## Practical Recommendations

- Observe the application's real load curve before setting HPA thresholds
- In production, set at least minReplicas=3 to avoid single points of failure
- Use PodDisruptionBudget together to ensure graceful downscaling

---

**References:**

- [Kubernetes Documentation — Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)