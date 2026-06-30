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

# Kafka Log Compaction vs Retention

## Intuition
Kafka does not delete messages when they are consumed; it deletes them based on retention policies. 

## Time/Size-based Retention
- `retention.ms` or `retention.bytes` will delete *old* messages once the threshold is crossed, regardless of whether a consumer has read them. This allows new consumers to replay history.

## Log Compaction
- `cleanup.policy=compact` keeps only the **most recent value for each key**, deleting older values for that same key.
- This is useful when a topic represents *current state* rather than a history of events (e.g., a topic feeding a `KTable` of "current account balances"). It prevents the topic from growing unboundedly while still allowing a new consumer to rebuild the full current-state table from the start.
