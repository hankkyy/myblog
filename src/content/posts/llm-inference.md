---
title: "LLM 推理优化：从 Flash Attention 到 vLLM PagedAttention"
date: 2026-06-13T15:00:00+08:00
categories: ["AI"]
description: "深入理解大模型推理加速的核心技术：KV Cache、Flash Attention、Continuous Batching 和 PagedAttention"
---

大模型推理慢、显存占用大，是实际部署最大的痛点。这篇文章梳理四个关键优化技术。

## 1. KV Cache

Transformer 在生成每个 token 时都要重新计算所有历史 token 的 Key 和 Value。KV Cache 的核心思想：**算过的 K、V 存起来，下次直接用**。

```python
# 没有 KV Cache：每步 O(n²)
for i in range(max_len):
    Q, K, V = linear(x[:i+1])  # 重复计算！
    output = attention(Q, K, V)

# 有 KV Cache：每步 O(n)
K_cache, V_cache = [], []
for i in range(max_len):
    Q_new, K_new, V_new = linear(x[i:i+1])
    K_cache.append(K_new)
    V_cache.append(V_new)
    output = attention(Q_new, K_cache, V_cache)
```

显存占用：`2 × num_layers × hidden_size × seq_len × dtype_size`。对于 LLaMA-70B，单请求 2048 token 约需 1.1GB。

## 2. Flash Attention

经典 Attention 的问题：中间矩阵 (QK^T) 大小是 O(n²)，必须写到 HBM（显存），然后再读回来做 softmax。

Flash Attention 的做法：**分块计算，不写中间结果**。

```
传统: QK^T → HBM → softmax → HBM → ×V → HBM  (3次HBM读写)
Flash: QK^T → SRAM → softmax → ×V → HBM       (1次HBM读写)
```

利用 GPU 的 SRAM（比 HBM 快 10x+），将 Q、K、V 分成小块，在 SRAM 内完成全部计算。结果是 2-4x 加速 + 显存占用降低到 O(n)。

## 3. vLLM PagedAttention

传统推理引擎为每个请求预分配连续显存（max_seq_len），产生大量碎片。PagedAttention 借鉴操作系统虚拟内存思想：**KV Cache 分成固定大小的 block，不要求连续**。

```
传统: [Req1 KV: ████████________] [Req2 KV: ████____________]
PagedAttention: [Block0:Req1] [Block1:Req2] [Block2:Req1] [Block3:空闲]
```

结果：显存利用率从 20-40% 提升到 **96%+**。

## 4. Continuous Batching

传统静态 batching：等所有请求完成才开始下一批。一个长请求拖慢全家。

Continuous Batching：**每个 step 动态组 batch**。有请求完成就踢出去，新请求随时加入。吞吐提升 2-10x。

## 总结

| 技术 | 解决的问题 | 加速比 |
|------|-----------|--------|
| KV Cache | 避免重复计算 | 基础 |
| Flash Attention | I/O 瓶颈 | 2-4x |
| PagedAttention | 显存碎片 | 吞吐 2-4x |
| Continuous Batching | 批效率 | 吞吐 2-10x |

> 优化推理的核心思路：别让 GPU 闲着等数据。
