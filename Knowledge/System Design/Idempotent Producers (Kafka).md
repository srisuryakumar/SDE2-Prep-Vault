---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kafka Producer ACKs"]
tags: [kafka, idempotency]
---

# Idempotent Producers (Kafka)

## Intuition
When a producer writes to a broker and a network glitch drops the acknowledgment (ACK), the producer doesn't know if the write succeeded. It must retry. Naive retries can result in duplicate messages being written to the partition.

## The Solution
By setting `enable.idempotence=true`, the producer tags each message with a sequence number. The broker detects sequence numbers it has already seen and silently drops the duplicate from the retry. 

This gives you exactly-once delivery for the *producer-to-broker hop* without writing any custom deduplication code. (Note: this does not give you end-to-end exactly-once delivery for consumers).
