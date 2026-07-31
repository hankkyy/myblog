---
lang: en
title: "gRPC vs REST: When Should You Use gRPC?"
date: 2026-05-18T10:00:00+08:00
categories: ["Technology"]
description: "Protobuf encoding, HTTP/2 multiplexing, streaming—an analysis of gRPC's pros and cons"
---

Should microservices communicate via REST or gRPC?

## Core Differences

| Dimension | REST | gRPC |
|-----------|------|------|
| Protocol | HTTP/1.1 | HTTP/2 |
| Data Format | JSON (text) | Protobuf (binary) |
| Interface Definition | No enforced contract | .proto files |
| Code Generation | Manual/OpenAPI | Automatic |
| Streaming | Not supported | Natively supported |

## Protobuf: Size Is the Advantage

```protobuf
message User {
  int64 id = 1;
  string name = 2;
  string email = 3;
}
```

JSON rendering: `{"id": 123, "name": "Zhang San", "email": "zhang@test.com"}` → 58 bytes
Protobuf encoding: → ~30 bytes, saving ~50%

In high-frequency call scenarios, the cumulative bandwidth difference is significant.

## HTTP/2 Multiplexing

```
HTTP/1.1:  Connection 1 [req1 → res1] | Connection 2 [req2 → res2]  ← Head-of-line blocking
HTTP/2:    Single connection [req1,req2,req3] → [res2,res1,res3]  ← Multiplexing
```

## When to Use gRPC

- ✅ High-frequency internal calls between microservices
- ✅ When streaming is needed (real-time push, large files)
- ✅ Polyglot environments (automatic code generation)
- ✅ Performance-sensitive scenarios

## When to Use REST

- ✅ External APIs (browser compatibility)
- ✅ Simple CRUD
- ✅ When caching is needed (native HTTP cache support)
- ✅ Team unfamiliar with Protobuf

> Use gRPC internally, REST externally—this is the current mainstream choice.

---

**References:**

- [gRPC Official Documentation](https://grpc.io/)