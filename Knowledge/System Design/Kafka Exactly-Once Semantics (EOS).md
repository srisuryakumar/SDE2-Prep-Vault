---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Idempotent Producers (Kafka)"]
tags: [kafka, messaging, architecture]
---

# Kafka Exactly-Once Semantics (EOS)

## Intuition
Kafka's default delivery guarantee is **at-least-once**. To achieve **exactly-once semantics (EOS)**, Kafka layers two mechanisms to prevent both producer-side duplicates and consumer-side double-processing during crashes.

## The Two Mechanisms
1. **Idempotent Producer:** (See [[Idempotent Producers (Kafka)]]). Prevents duplicate writes from the producer to the broker caused by network retries.
2. **Transactions:** Allows a consume-process-produce cycle (read from topic A, write to topic B, AND commit the consumer offset) to happen **atomically**. Either the whole cycle is visible, or none of it is, even if the application crashes mid-cycle.

## The Boundary Limit
Exactly-once applies *only within Kafka*. The moment you call an external REST API or write to a non-transactional database inside your Kafka listener, you lose end-to-end exactly-once guarantees and must rely on idempotency at that external boundary.
