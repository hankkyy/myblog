---
title: "苹果发布 M4 Ultra：桌面级 AI 推理的转折点？"
date: 2025-11-20T14:00:00+08:00
categories: ["AI", "新闻"]
description: "M4 Ultra 搭载 256GB 统一内存，可本地运行 400B 参数模型，本地 AI 推理进入新纪元。"
---

苹果在 MacBook Pro 和 Mac Studio 上发布了 M4 Ultra 芯片。

## 关键参数

- CPU：32 核（20 性能核 + 12 能效核）
- GPU：80 核，67 TFLOPS（FP16）
- 统一内存：最高 256GB LPDDR5X，带宽 1.2TB/s
- NPU：64 核，120 TOPS

## 对 AI 开发的意义

256GB 统一内存意味着什么？你可以在 MacBook Pro 上本地跑 405B 参数的 Llama 4 模型。

用传统的消费级 GPU（4080 16GB / 4090 24GB）跑大模型必须做量化，但 M4 Ultra 的 256GB 统一内存可以跑全精度。

而且是统一内存架构——CPU 和 GPU 共享同一块内存，不需要 PCIe 传输数据。这对推理延迟非常友好。

## 代价

最顶配 Mac Studio M4 Ultra 256GB 售价 $12,999。对于个人开发者来说不便宜，但对比 A100/H100 的采购和运维成本，其实还算合理。

以后本地 AI 开发的门槛会越来越低，这对整个行业是好消息。