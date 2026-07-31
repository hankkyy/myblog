---
lang: en
title: "HTTP and HTTPS Interview Guide: Status Codes, Caching, TLS Handshake"
date: 2025-04-15T11:00:00+08:00
categories: ['Technology']
description: "Evolution from HTTP 1.0 to 3.0, meanings of common status codes, and the encryption principles of HTTPS."
---

The HTTP protocol is a fundamental topic in backend interviews.

## Evolution of HTTP

**HTTP 1.0**: One TCP connection per request, closed after use. Inefficient.

**HTTP 1.1**: Persistent connections (Connection: keep-alive) + Pipelining. But head-of-line blocking remains an issue.

**HTTP 2.0**: Multiplexing (multiple concurrent requests over a single TCP connection), header compression, server push. However, TCP head-of-line blocking still persists.

**HTTP 3.0**: Based on QUIC (UDP), completely solves head-of-line blocking.

## Common Status Codes

- **200**: OK
- **301**: Permanent redirect (search engines will update the URL)
- **302**: Temporary redirect
- **304**: Not Modified (cache is valid, no need to retransmit)
- **400**: Bad request parameters
- **401**: Unauthenticated (login required)
- **403**: Forbidden (no permission)
- **404**: Resource not found
- **500**: Internal server error
- **502**: Bad gateway (upstream server is down)
- **503**: Service unavailable (overloaded or under maintenance)

## HTTPS = HTTP + TLS

TLS handshake process (simplified):

1. Client sends supported cipher suites
2. Server selects a cipher suite + sends its certificate
3. Client verifies the certificate + generates a symmetric key (encrypted with the server's public key and sent)
4. Both parties communicate using the symmetric key for encryption

## Cache Headers

- **Cache-Control: max-age=3600**: Cache for 1 hour
- **ETag**: Resource version identifier, used with If-None-Match for conditional requests
- **Last-Modified**: Last modification time, used with If-Modified-Since

## Interview Talking Points

> The core improvement from HTTP 1.1 to 2.0 is multiplexing — a single TCP connection carries multiple requests. The core improvement from 2.0 to 3.0 is the QUIC protocol — based on UDP, it completely solves TCP's head-of-line blocking. HTTPS exchanges a symmetric key through the TLS handshake, after which symmetric encryption protects the communication content.

Remember the status codes and caching strategies — you'll encounter them every day in real development.