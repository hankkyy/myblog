---
title: "gRPC vs REST：什么时候该用 gRPC？"
date: 2026-05-18T10:00:00+08:00
categories: ["技术"]
description: "Protobuf 编码、HTTP/2 多路复用、流式传输——gRPC 的优劣势分析"
---

微服务通信选 REST 还是 gRPC？

## 核心差异

| 维度 | REST | gRPC |
|------|------|------|
| 协议 | HTTP/1.1 | HTTP/2 |
| 数据格式 | JSON (文本) | Protobuf (二进制) |
| 接口定义 | 无强制约定 | .proto 文件 |
| 代码生成 | 手动/OpenAPI | 自动 |
| 流式传输 | 不支持 | 原生支持 |

## Protobuf：体积就是优势

```protobuf
message User {
  int64 id = 1;
  string name = 2;
  string email = 3;
}
```

JSON 渲染：`{"id": 123, "name": "张三", "email": "zhang@test.com"}` → 58 bytes
Protobuf 编码：→ ~30 bytes，节省 ~50%

在高频调用场景，累计带宽差距显著。

## HTTP/2 多路复用

```
HTTP/1.1:  连接1 [req1 → res1] | 连接2 [req2 → res2]  ← Head-of-line blocking
HTTP/2:    单连接 [req1,req2,req3] → [res2,res1,res3]  ← 多路复用
```

## 什么时候用 gRPC

- ✅ 微服务间高频内部调用
- ✅ 需要流式传输（实时推送、大文件）
- ✅ 多语言环境（代码自动生成）
- ✅ 性能敏感场景

## 什么时候用 REST

- ✅ 对外 API（浏览器兼容）
- ✅ 简单 CRUD
- ✅ 需要缓存（HTTP 缓存天然支持）
- ✅ 团队不熟悉 Protobuf

> 内部用 gRPC，对外用 REST——这是目前的主流选择。
