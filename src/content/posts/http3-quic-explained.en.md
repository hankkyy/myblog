---
lang: en
title: "HTTP/3 and QUIC: Why Replace TCP with UDP?"
date: 2025-01-05T09:00:00+08:00
categories: ["Technology"]
description: "A simple explanation of the design principles behind HTTP/3 based on the QUIC protocol, and how it solves the problems of HTTP/2."
---

HTTP/3 is gradually gaining adoption, but many people don't understand why it uses UDP at its core instead of TCP.

## Why Not TCP?

The biggest problem with HTTP/2 is **Head-of-Line Blocking**.

TCP guarantees that data packets arrive in order. If the first packet is lost, even if the second and third packets have already arrived, the application layer can't access them—it must wait for the first packet to be retransmitted.

In HTTP/2, a single TCP connection carries multiple streams (multiplexing), so **the loss of one packet blocks all streams**. This has a significant impact in poor network conditions (such as mobile networks).

## The QUIC Approach

QUIC implements TCP-like reliable transmission on top of UDP, but each stream is independent:

- If a packet in Stream A is lost, Streams B and C are unaffected
- Retransmitted packets use new packet numbers (avoiding TCP's retransmission ambiguity problem)
- Connection migration: switching from WiFi to 4G doesn't drop the connection

## Impact on Backend Development

- nginx 1.25+ supports HTTP/3 (requires the QUIC module)
- Certificate management is the same as HTTP/2 (TLS 1.3 is mandatory)
- Firewalls need to open UDP port 443
- gRPC is also advancing a QUIC-based transport layer

HTTP/3 isn't a silver bullet (HTTP/2 is perfectly sufficient on LANs), but for APIs targeting mobile users, HTTP/3's weak-network optimizations are highly valuable.

---

**References:**

- [IETF — QUIC: RFC 9000](https://www.rfc-editor.org/rfc/rfc9000)