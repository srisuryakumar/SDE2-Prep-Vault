---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kafka Architecture Overview"]
tags: [kafka, operations]
---

# Kafka Topic Configuration (Partitions and Replication)

## Intuition
When creating a Kafka topic, the two most important decisions are partition count and replication factor.

## Partitions
- **Controls maximum parallelism.** You can never have more *active* consumers in a group than you have partitions (extra consumers sit idle).
- More partitions = more parallelism, but higher resource usage per broker.
- **Rule of thumb:** Under-provision slightly and grow as needed. It's easier to add partitions than to merge them later.

## Replication Factor
- **Controls fault tolerance.** 
- A replication factor of `3` means each partition has 2 extra copies and can survive 2 broker failures without data loss. `3` is the standard production default.
- A replication factor of `1` means zero fault tolerance; losing that broker loses that data permanently.
