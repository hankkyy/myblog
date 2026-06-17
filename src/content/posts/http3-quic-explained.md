---
title: "HTTP/3 和 QUIC：为什么用 UDP 替代 TCP？"
date: 2025-01-05T09:00:00+08:00
categories: ["技术"]
description: "用简单的方式解释 HTTP/3 基于 QUIC 协议的设计原理，以及它解决了 HTTP/2 的哪些问题。"
---

HTTP/3 已经逐渐普及，但它底层用 UDP 而不是 TCP，很多人不理解。

## 为什么不用 TCP？

HTTP/2 最大的问题是**队头阻塞**（Head-of-Line Blocking）。

TCP 保证数据包按序到达。如果第 1 个包丢了，即使第 2、3 个包已经到了，应用层也拿不到，必须等第 1 个包重传。

HTTP/2 中一个 TCP 连接承载多个 Stream（多路复用），所以**一个包的丢失会导致所有 Stream 都阻塞**。这在弱网环境下（比如移动网络）影响很大。

## QUIC 的方案

QUIC 在 UDP 之上实现了类似 TCP 的可靠传输，但每个 Stream 是独立的：

- Stream A 的包丢了，Stream B、C 不受影响
- 重传的包使用新的包序号（避免了 TCP 的重传歧义问题）
- 连接迁移：WiFi 切 4G，连接不断

## 对后端开发的影响

- nginx 1.25+ 支持 HTTP/3（需要 QUIC 模块）
- 证书管理跟 HTTP/2 一样（TLS 1.3 是强制要求）
- 防火墙需要开 UDP 443 端口
- gRPC 也在推进基于 QUIC 的传输层

HTTP/3 不是银弹（局域网里 HTTP/2 完全够用），但对于面向移动用户的 API 来说，HTTP/3 的弱网优化很有价值。