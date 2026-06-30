---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 4 — Networking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, networking, http]
---

# HTTP Evolution (HTTP/1.1 vs HTTP/2 vs HTTP/3)

## HTTP/1.1
- **Sequential:** Processes one request at a time per TCP connection (even with Keep-Alive).
- **Head-of-Line (HOL) Blocking:** A delayed response blocks all subsequent requests on that connection.
- **Text-based:** Headers are sent as plain text and repeated verbatim for every request.

## HTTP/2
- **Multiplexing:** Multiple requests and responses can be interleaved on a single TCP connection simultaneously. Eliminates HOL blocking at the HTTP layer.
- **Header compression (HPACK):** Compresses headers to reduce redundant byte overhead.
- **Binary framing:** Uses a more efficient binary format instead of plain text.
- Used heavily in high-performance frameworks like **gRPC**.

## HTTP/3
- **QUIC over UDP:** Replaces TCP with a new transport protocol (QUIC) running over UDP.
- **Eliminates TCP HOL blocking:** In HTTP/2, if a TCP packet is lost, all multiplexed streams stall waiting for the retransmit. QUIC solves this because streams are independent.
- **Faster Handshake:** Combines TLS and transport handshakes to reduce connection establishment latency.
- **Connection Migration:** Survives network changes (like switching from WiFi to 4G).
