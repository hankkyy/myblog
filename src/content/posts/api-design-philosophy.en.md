---
lang: en
title: "The Philosophy of API Design: Reflections from REST to gRPC to GraphQL"
date: 2025-08-10T16:00:00+08:00
categories: ['Technology']
description: "Good API design isn't about following the latest protocol, but understanding the use cases and trade-offs of each paradigm."
---

REST, gRPC, and GraphQL each have their strengths, but good API design has little to do with which protocol you choose.

## REST

The core of REST is the resource:

```
GET    /users/123      # Get user
POST   /users           # Create user
PUT    /users/123       # Update user
DELETE /users/123       # Delete user
```

Pros: Simple, cacheable, uses HTTP status codes to express semantics.
Cons: Awkward for multi-resource operations (e.g., "get all unpaid orders for a user" requires nested URLs or multiple round trips).

## gRPC

The core of gRPC is RPC (Remote Procedure Call):

```protobuf
service OrderService {
  rpc CreateOrder(CreateOrderReq) returns (CreateOrderResp);
}
```

Pros: Strong typing, high performance, streaming support.
Cons: Poor browser support (requires gRPC-Web), less readable than REST.

## GraphQL

The core of GraphQL is letting the client decide what data it needs:

```graphql
query {
  user(id: 123) {
    name
    orders(status: "pending") { total }
  }
}
```

Pros: Fetch all needed data in a single request.
Cons: Uncontrollable query complexity (a single GraphQL query can bring down the backend), difficult caching.

## How to Choose

- Simple public-facing APIs → REST
- Internal microservice communication → gRPC
- Frontend requiring complex data aggregation → GraphQL
- Real-time data → WebSocket / SSE

There's no silver bullet. Good API design is about letting callers guess how to use it, not making them dig through documentation.