---
lang: en
title: "WebAssembly on the Backend: Year Three, the Turning Point Approaches"
date: 2026-07-22T14:00:00+08:00
categories: ["Technology", "Cloud Native"]
description: "With the WASI 0.3 preview release, the server-side Wasm ecosystem is accelerating. It won't replace Docker, but it will replace the scenarios where Docker is too heavy."
---

This week, Kimi and Fable 5 grabbed all the headlines. But one thing flew under the radar: the WASI 0.3 preview was released last month, bringing async I/O support. This could be a turning point for the future of WebAssembly on the backend.

## Why Wasm Matters

The most disruptive feature of Wasm is **cold start speed**.

Docker containers take at least a few hundred milliseconds to cold start (pull image → unpack → launch process), and Java applications take seconds. Wasm cold starts are **microsecond-level** — because a Wasm module is just a compiled bytecode file that doesn't require booting an OS process.

This is revolutionary in serverless scenarios: user request arrives → cold start Wasm module → process request → destroy. The entire lifecycle takes less than 1 millisecond. This is the ultimate form of serverless — an independent, secure, ephemeral execution environment for every request.

## The Key Breakthrough in WASI 0.3

Previously, WASI only had synchronous I/O, which meant you couldn't efficiently handle network requests in Wasm. The `wasi:io/poll` interface in WASI 0.3 finally makes async I/O possible.

In simple terms: **Before WASI 0.3, Wasm could only run functions. After it, Wasm can run services.**

Additionally, Wasm's sandbox isolation happens at the language VM level and doesn't share the OS kernel. Compared to Docker, the security boundary is stronger. This makes it naturally suited for multi-tenant platforms — one Wasm sandbox per tenant is both more secure and cheaper than containers.

## The Reality Gap

To be fair, here's what the reality of Wasm on the backend looks like:

- **Rust** has the best support — the wasm32-wasip2 target is already available, and the Tokio async runtime can compile to Wasm
- **Go** is catching up — Go 1.24 improved Wasm support, but goroutine scheduling still has limitations
- **Java** is still early — GraalVM can compile to Wasm, but the ecosystem (database drivers, HTTP clients) is far from mature
- **Observability** is a blind spot — how do you do logging, metrics, and tracing in Wasm? There's no standard solution yet

## Who's Using It?

- **Cloudflare Workers**: The most successful server-side Wasm application, handling trillions of requests daily
- **Fermyon Spin**: A Wasm-based serverless framework with some enterprise use cases already
- **Docker** officially announced support for Wasm as an alternative container runtime

## My Take

Wasm's position on the backend isn't to "replace Docker," but to "replace the scenarios where Docker is too heavy":

- **Edge computing**: CDN edge nodes, IoT gateways — where you need extremely fast startup and minimal footprint
- **Event-driven short tasks**: Webhook processing, data transformation, image resizing — born and gone within milliseconds
- **Multi-tenant platforms**: One Wasm sandbox per tenant, more secure and cheaper than containers

Before 2027, there should be a serious backend framework written in Wasm that gains widespread attention.

In a week where Kimi K3 and Fable 5 stole all the spotlight, Wasm's progress has been quiet. But history shows that quietly advancing technologies often end up having the biggest impact.

---

**References:**

- [WASI 0.3 Preview — WASI Preview 3](https://github.com/WebAssembly/WASI)
- [Cloudflare Workers — WebAssembly on the edge](https://developers.cloudflare.com/workers/)
- [Fermyon — Spin: Serverless WebAssembly](https://www.fermyon.com/spin)