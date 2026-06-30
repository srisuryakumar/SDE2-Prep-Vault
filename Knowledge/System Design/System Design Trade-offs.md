---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 14 — System Design Trade-offs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Framework"]
tags: [hld, trade-offs, cap-theorem]
---

# System Design Trade-offs

The core of an SDE-2 system design interview is explicitly stating and justifying trade-offs.

## 1. SQL vs NoSQL
- **SQL (PostgreSQL/MySQL):** Strong consistency, ACID, joins. Vertical scaling has a ceiling. Best for Payments, Booking Confirmations.
- **NoSQL (Cassandra/DynamoDB/Redis):** Eventual consistency (usually), no joins. Built for horizontal scaling. Best for Chat messages, Location Data, Feed lists.
- *The Decisive Question:* "Does this data need transactional joins and strong consistency, or does it need to scale writes/reads horizontally with a known access pattern?"

## 2. Sync vs Async
- **Sync:** Caller waits for the result. Slower, tighter coupling. Used when the caller *needs the result* to make the next decision (e.g., payment charge confirmation).
- **Async (Queue-mediated):** Caller enqueues and moves on. Isolates the caller from downstream latency and failures. Used when the caller just needs a side effect to eventually happen (e.g., send an email).

## 3. Push vs Pull
- **Push:** Source proactively sends updates. Lower latency, fresher data. Wastes resources on uninterested consumers. (e.g. Chat messages).
- **Pull:** Consumer requests data. Simpler, but data can be stale between pulls. (e.g. Search autocomplete hourly refresh).

## 4. Consistency vs Availability (CAP Theorem)
Under a network partition, you must choose:
- **Consistency (CP):** Every read sees the latest write (e.g., Payment system, Seat booking `SELECT FOR UPDATE`).
- **Availability (AP):** Every request gets a response, even if stale (e.g., Social media feed, Uber driver location).
*Note:* You pick a side for *each piece of data*, not once for the whole system.

## How to Present Trade-offs in Interviews
A strong SDE-2 answer follows this exact 4-part formula:
1. **The Decision:** "I'm choosing [Option A] because [Specific Reason tied to requirements]."
2. **The Downside:** "The trade-off is [Specific Downside - not vague]."
3. **The Mitigation:** "I'd mitigate that by [Mitigation strategy]."
4. **The Alternative:** "[Option B] would be the right choice if [Different Requirement] was the priority."

*Example:* "I'm making the email async via a Kafka event because SMTP latency is 500ms, which would slow down checkout. The trade-off is eventual consistency (the email arrives a few seconds late), which is perfectly acceptable here. I mitigate the risk of lost events by using a Dead Letter Queue. Synchronous would be the right choice if the email contained a one-time payment link needed immediately."
