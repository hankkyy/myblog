---
lang: en
title: "Huawei Ascend 910C Enters Mass Production: Can Domestic AI Chips Replace NVIDIA?"
date: 2025-08-05T10:00:00+08:00
categories: ['AI', 'News']
description: "Huawei's Ascend 910C chip has entered mass production, with performance reaching about 80% of the H100, but the ecosystem gap remains significant."
---

Huawei's Ascend 910C AI chip has officially entered mass production.

## Performance

- FP16 compute: approximately 320 TFLOPS (H100 is 400 TFLOPS)
- Power consumption: 310W
- Process node: 7nm (limited by sanctions, unable to use more advanced process nodes)
- Memory: 64GB HBM2E

## Advantages

- Not subject to U.S. export controls
- Price is about 50% cheaper than NVIDIA
- Deep integration with Huawei Cloud
- Politically correct choice for domestic substitution

## Disadvantages

- Weak software ecosystem (CUDA's advantage isn't the hardware—it's the developer ecosystem built over a decade)
- Can only run Huawei's own MindSpore framework
- High migration costs for many PyTorch models
- Performance ceiling limited by process node

## Can It Replace NVIDIA?

Not in the short term. However, in specific scenarios (such as AI projects for government and state-owned enterprises), the Ascend 910C is a necessity—these customers must use domestic chips.

Huawei's strategy is also quite smart: instead of competing with NVIDIA on training performance for massive GPU clusters, it focuses on inference scenarios (which have lower dependency on ecosystem and lower hardware compatibility requirements).

There's still a long way to go for domestic AI chips, but the Ascend 910C at least proves this path is viable.

---

**References:**

- [Huawei — Ascend](https://www.huawei.com/)