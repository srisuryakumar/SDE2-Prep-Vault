---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kafka Architecture Overview"]
tags: [kafka, operations, metrics]
---

# Consumer Lag

## Intuition
Consumer lag is the single most important Kafka operational metric. It is the difference between the latest offset produced to a partition and the offset the consumer group has currently committed.

`Lag = (Latest partition offset) - (Committed offset)`

## Why it matters
Rising lag means your consumer cannot keep up with the producer. It might be too slow, or it might be crashed. 
**Alerting rule:** Alert on lag growing unboundedly, not on lag existing at all. A small, stable lag is completely normal. The danger signal is the upward trend, not the absolute number.
