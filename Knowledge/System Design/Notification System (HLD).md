---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 5 — Design 3 — Notification System"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["System Design Building Blocks"]
tags: [hld, case-study, notification, kafka]
---

# HLD Case Study: Notification System

## Problem Overview
Send push, email, SMS, and in-app notifications.
- **Scale:** 1M notifications/hour average (278/sec), but bursts are far higher (e.g. 1M broadcast in minutes).
- **Priority:** Must respect priority. A payment-failure alert must not wait behind a marketing blast.
- **Idempotency:** No duplicate sends.

## The Priority Queue Solution
A single FIFO queue means a marketing broadcast delays critical alerts.
**Solution:** Separate Kafka topics per priority tier.
- `notif.critical` (payment failed)
- `notif.high` (OTP code)
- `notif.medium` (mention)
- `notif.low` (marketing blast)

Assign dedicated consumer groups to each topic. `notif.critical` gets a dedicated worker pool so it's never starved.

## Deduplication (Idempotency)
Use Redis `SET NX` before sending.
```
key = "notif:sent:" + idempotency_key
SET key "1" NX EX 86400 (24h TTL)
```
If SET succeeds -> first time -> send.
If SET fails -> duplicate -> skip.

## Delivery Tracking
Maintain a state machine in a DB: `PENDING -> SENT -> DELIVERED -> FAILED`.
- `SENT` when the 3rd party provider (Twilio/SendGrid) accepts the request.
- `DELIVERED` when the provider's webhook confirms delivery.

## Scale Challenge: Broadcast Fan-Out
Sending 1M notifications from a single API call.
**Solution:** The API writes **one** "broadcast" event to Kafka. A dedicated fan-out worker expands it into per-user messages, publishing those to the priority topics in batches. This keeps the API fast and scales workers horizontally.

## Common Questions
**Q: What if a user opts out of a notification type after the broadcast fan-out has already started?**
A: Check opt-out status at the channel-worker stage (just before calling the provider), not just at fan-out time, so late opt-outs are honored.
