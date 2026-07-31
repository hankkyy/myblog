---
lang: en
title: "Getting Started with CDN Edge Computing: What Can Cloudflare Workers and Vercel Edge Do?"
date: 2025-05-18T16:00:00+08:00
categories: ['Technology']
description: "Edge computing runs code on global CDN nodes, significantly reducing latency. Learn where it fits and where it doesn't."
---

Edge computing is the evolution of CDN—not only caching static files but also running code on the node closest to the user.

## Why Edge Computing Matters

Traditional architecture: User → CDN (static) → Origin server (dynamic processing)

Edge computing: User → Edge node (both dynamic and static handled here)

A user in Singapore with an origin server in the US. In the traditional model, dynamic requests must travel halfway around the globe (200ms+). With edge computing, requests are handled directly at the nearest node (10ms).

## Suitable Use Cases

- A/B testing (returning different versions at the edge based on cookies)
- Image optimization (real-time resizing, format conversion)
- API gateway (authentication, rate limiting, and routing at the edge)
- Location-based logic
- Simple server-side rendering

## Unsuitable Scenarios

- Operations requiring a database (latency and consistency issues)
- Compute-intensive tasks (edge nodes have limited CPU)
- Stateful logic (no shared state between edge nodes)

## Major Platforms

- Cloudflare Workers: The world's largest edge network, supporting JS/TS/WASM
- Vercel Edge Functions: Deep integration with Next.js
- Deno Deploy: An edge platform built on Deno
- AWS Lambda@Edge: Tied to CloudFront

Edge computing is an important trend—not a replacement for traditional backends, but a way to make certain critical paths faster.