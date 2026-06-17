---
title: "API 设计的哲学：从 REST 到 gRPC 再到 GraphQL 的反思"
date: 2025-08-10T16:00:00+08:00
categories: ['技术']
description: "好的 API 设计不是跟风用最新的协议，而是理解每种范式的适用场景和取舍。"
---

REST、gRPC、GraphQL 各有各的好，但好的 API 设计跟选择什么协议关系不大。

## REST

REST 的核心是资源（Resource）：

```
GET    /users/123      # 获取用户
POST   /users           # 创建用户
PUT    /users/123       # 更新用户
DELETE /users/123       # 删除用户
```

优点：简单、可缓存、用 HTTP 状态码表达语义。
缺点：多资源操作时比较麻烦（「获取用户的所有订单中未支付的」需要嵌套 URL 或多轮请求）。

## gRPC

gRPC 的核心是 RPC（远程过程调用）：

```protobuf
service OrderService {
  rpc CreateOrder(CreateOrderReq) returns (CreateOrderResp);
}
```

优点：强类型、高性能、流式传输。
缺点：浏览器支持差（需要 gRPC-Web）、可读性不如 REST。

## GraphQL

GraphQL 的核心是让客户端决定要什么数据：

```graphql
query {
  user(id: 123) {
    name
    orders(status: "pending") { total }
  }
}
```

优点：一次请求获取所有需要的数据。
缺点：查询复杂度不可控（一个 GraphQL 查询可能拖垮后端）、缓存困难。

## 怎么选

- 对外开放的简单 API → REST
- 内部微服务通信 → gRPC
- 前端需要复杂数据聚合 → GraphQL
- 实时数据 → WebSocket / SSE

没有银弹。好的 API 设计是让调用者能猜到该怎么用，而不是让调用者去翻文档。
