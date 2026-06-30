---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kafka Architecture Overview"]
tags: [kafka, stream-processing]
---

# Kafka Streams

## Intuition
Kafka Streams is a library (runs inside your application, not as a separate cluster) for transforming, aggregating, and joining streams of events in real time.

## Core Abstractions
- **`KStream`**: A stream of independent events (e.g., every individual order placed).
- **`KTable`**: A stream interpreted as a continuously-updated **table** keyed by record key. Each new message *replaces* the previous value for that key, like a changelog.
- **Windowed Aggregation**: Grouping events into time buckets (e.g., "orders per 5-minute tumbling window") to compute rolling metrics without needing to query an external database.
