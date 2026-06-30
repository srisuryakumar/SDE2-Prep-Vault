---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 6 — Design 4 — WhatsApp"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Building Blocks", "Distributed Systems and Messaging"]
tags: [hld, case-study, whatsapp, chat, websockets, cassandra]
---

# HLD Case Study: WhatsApp (Chat System)

## Problem Overview
Design a 1-to-1 and group chat system.
- **Scale:** 50M DAU, 100B messages/day (1.16M messages/sec avg, ~5M peak).
- **Connections:** 50M concurrent WebSocket connections.
- **Latency:** Delivery < 500ms when both are online. Offline messages must not be lost.

## Maintaining 50M Concurrent Connections
A single modern server can hold 50K-100K concurrent idle WebSocket connections. So, we need 500-1,000 **Chat Servers**.
**The Routing Problem:** If User A is on Server 7, and User B is on Server 203, how does Server 7 know where to route the message?
**Solution:** A **Connection Registry** (sharded Redis).
1. On connect: Chat Server sets `user_id -> server_id` in Redis.
2. On send: Sender's Chat Server queries Redis for recipient's `server_id`.
3. Message is routed to the recipient's Chat Server via Kafka.

## Message Flow & Storage
```
Sender -> Chat Server A -> Kafka -> Chat Server B -> Recipient
             |
             v
         Cassandra (durable write in parallel)
```
Writes to Cassandra happen *in parallel* with live delivery so the user doesn't wait for disk I/O.

## Database: Cassandra
Why Cassandra over Postgres? Because it handles massive write volume and time-ordered data efficiently.
- **Partition Key:** `conversation_id` (hash of the two user IDs sorted, or group ID).
- **Clustering Key:** `message_timestamp (descending)`.
This makes fetching the last N messages of a conversation a fast, single-partition range scan.

## Group Messaging Fan-Out
When a user sends a message to a 256-member group, the sender's device makes **one** network call. The server-side fan-out worker expands it into 256 individual routings.

## Common Questions
**Q: How do read receipts work?**
A: A read receipt is just a small control message routed through the exact same chat-server-to-chat-server path as a normal message. It's cheap to process.

**Q: What if a chat server crashes?**
A: Connections drop, clients reconnect to a different server via the load balancer. Any messages sent during the brief gap are sitting safely in Kafka waiting for the new server to consume them.
