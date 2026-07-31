---
lang: en
title: "TCP Three-Way Handshake and Four-Way Wave: What Do Interviewers Really Want to Hear?"
date: 2025-03-10T14:00:00+08:00
categories: ['Technology']
description: "Not just memorizing the process, but understanding why three times instead of two or four, and why the wave takes four steps."
---

TCP connection establishment and teardown is a core topic in computer networking interviews.

## Three-Way Handshake

```
Client                           Server
  |                               |
  |----SYN(seq=x)---------------->|  ① Client: I want to connect
  |                               |
  |<---SYN+ACK(seq=y,ack=x+1)----|  ② Server: Got it, I'm ready
  |                               |
  |----ACK(seq=x+1,ack=y+1)----->|  ③ Client: Received, start sending data
```

## Why Three Times Instead of Two?

The problem with two handshakes: if the client's first SYN is delayed in the network and then arrives again, the server would incorrectly establish a connection.

The third ACK in the three-way handshake lets the server confirm that the client actually received its SYN+ACK, preventing stale connections from being incorrectly established.

## Why Not Four Times?

The server can combine SYN and ACK into a single packet (SYN+ACK) without needing to send them separately. So three times is sufficient.

## Four-Way Wave

```
Client                           Server
  |                               |
  |----FIN(seq=u)---------------->|  ① Client: I have no more data
  |                               |
  |<---ACK(seq=v,ack=u+1)--------|  ② Server: Understood
  |                               |
  |<---FIN(seq=w,ack=u+1)--------|  ③ Server: I have no more data either
  |                               |
  |----ACK(seq=u+1,ack=w+1)----->|  ④ Client: Understood
```

## Why Does the Wave Take Four Steps?

Because TCP is full-duplex — both sides can independently send and receive data. When one side says "I have no more data" (FIN), the other side may still have data to send. So FIN and ACK cannot be combined.

After the client sends its final ACK, it enters TIME_WAIT (2MSL, about 60 seconds), which serves two purposes:
1. Ensuring the final ACK reaches the server
2. Allowing all packets from the old connection to disappear from the network

## Interview Talking Points

> The three-way handshake is essentially establishing a reliable connection over an unreliable network. Two times is not enough (stale connection issues), four times is wasteful. The four-way wave exists because TCP is full-duplex, and each side needs to confirm its own closure independently.

People who can explain "why three and why four" are far rarer than those who just recite the process.