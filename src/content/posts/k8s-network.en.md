---
lang: en
title: "Kubernetes Network Model: The Complete Packet Journey from Pod to Service"
date: 2026-06-14T09:00:00+08:00
categories: ["Technology"]
description: "Tracing the full network path of a request from outside the K8s cluster to a Pod"
---

Kubernetes' network model is a frequent interview question, but many people just memorize "one IP per Pod" without understanding how the actual packets travel.

## The Three-Layer Network Model of K8s

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

## Scenario 1: Pod Communication on the Same Node

Pod A (10.244.1.2) → Pod B (10.244.1.3):

1. Pod A sends a packet targeting `10.244.1.3`
2. The packet traverses the veth pair and reaches the `cni0` bridge
3. cni0 checks the ARP table and finds the target is on the same subnet
4. **Direct Layer 2 forwarding** — no iptables involved

## Scenario 2: Pod Communication Across Nodes

Pod A (Node1) → Pod C (Node2):

1. Pod A sends a packet targeting `10.244.2.2`
2. It reaches cni0, which finds the target is not on the local subnet
3. The routing table is consulted: `10.244.2.0/24 via 10.0.0.6` (Node2's IP)
4. The packet is encapsulated (VXLAN / IP-in-IP) and sent to Node2
5. Node2 decapsulates it and hands it to the local cni0
6. cni0 forwards it to Pod C

**Key point: The overlay network uses VXLAN tunnel encapsulation, adding 50 bytes of VXLAN header to each packet.**

## Scenario 3: ClusterIP Service

```yaml
apiVersion: v1
kind: Service
spec:
  clusterIP: 10.96.0.1
  selector:
    app: nginx
```

Request to `10.96.0.1:80` → Pod B:

1. The packet reaches iptables/netfilter
2. It matches the DNAT rule written by kube-proxy
3. The destination is rewritten to `10.244.1.3:80`
4. **A backend Pod is randomly selected** (default iptables probability mode)
5. From here on, it's the same as normal Pod communication

**Drawback of iptables mode**: Rule count is O(n), so performance degrades with many Services. Newer versions recommend **IPVS mode**, which uses hash table lookups — O(1).

## Scenario 4: External Traffic → NodePort → Pod

External user → `NodeIP:30080` → Pod:

```
Client → NodeIP:30080
  → iptables DNAT → ClusterIP:80
    → iptables DNAT → PodIP:80
```

> Note: If the Pod is not on the node that received the request, iptables adds an extra layer of SNAT, so the Pod sees the Node IP as the source IP. Setting `externalTrafficPolicy: Local` preserves the original source IP.

## Summary

| Scenario | Key Technology | Performance |
|----------|----------------|-------------|
| Same-node Pod | veth + bridge | Highest |
| Cross-node Pod | VXLAN/Calico BGP | Medium |
| ClusterIP | iptables/IPVS DNAT | Medium |
| NodePort | iptables SNAT+DNAT | Lower |