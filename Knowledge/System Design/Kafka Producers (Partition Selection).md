---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kafka Architecture Overview"]
tags: [kafka, messaging]
---

# Kafka Producers (Partition Selection)

## Intuition
A Kafka producer sends a message consisting of a **key**, a **value**, a **topic**, and optionally a specific **partition**.

## Partition Selection by Key
If you don't specify a partition explicitly, Kafka computes it from the key: `partition = hash(key) % numPartitions`.
This means **messages with the same key always land on the same partition**. 

Because Kafka guarantees strict ordering within a partition, sending all updates for a specific entity (e.g., `orderId=555`) with the same key guarantees that a consumer will process those updates in the exact order they were sent.
