---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 4 — Networking"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, networking, websocket]
---

# WebSocket Protocol

HTTP is inherently a request-response protocol; the client must initiate all communication. For real-time applications (e.g., chat, live dashboards, multiplayer games), the server needs to push data to the client proactively.

## How WebSocket Works
WebSocket starts as a standard HTTP request, but includes an `Upgrade: websocket` header.
- The server responds with an `HTTP 101 Switching Protocols` status code.
- The connection is "upgraded" from HTTP to a persistent, bidirectional channel over the same TCP connection.

Once upgraded, the connection is no longer HTTP. It operates as a raw bidirectional frame stream. Either the client or the server can send messages to the other at any time, with very low overhead, until the connection is explicitly closed.
