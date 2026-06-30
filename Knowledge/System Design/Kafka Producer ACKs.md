---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kafka Producers (Partition Selection)"]
tags: [kafka, messaging, architecture]
---

# Kafka Producer ACKs

## Intuition
The `acks` configuration controls how many replicas must confirm a write before the producer considers it successful. It is a direct trade-off between latency and durability.

## Acknowledgment Levels
- **`acks=0`**: Fire-and-forget. The producer doesn't wait for any confirmation. **Fastest**, but messages can be silently lost.
- **`acks=1`**: The leader writes the message to its own log and confirms, without waiting for replicas. **Fast**, but data is lost if the leader fails before replicating.
- **`acks=all` (or `-1`)**: The leader waits for all in-sync replicas to confirm the write. **Slowest**, but provides the strongest durability (survives a leader failure). Use this for financial or critical data.
