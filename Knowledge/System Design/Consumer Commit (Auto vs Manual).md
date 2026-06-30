---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kafka Consumers (Polling)"]
tags: [kafka, messaging]
---

# Consumer Commit (Auto vs Manual)

## Intuition
Once a consumer processes a message, it must "commit" the offset so Kafka knows not to send it again. How you commit determines whether you might lose messages or process them twice.

## Auto Commit (`enable.auto.commit=true`)
Kafka periodically commits the latest offset automatically on a timer, *regardless of whether processing finished*.
- **Risk:** If the app crashes *after* the auto-commit fires but *before* processing finishes, the message is skipped on restart (data loss).

## Manual Commit
You call `commitSync()` or `commitAsync()` explicitly in code **after** processing succeeds.
- **Risk if done wrong:** Committing before processing has the same data loss risk as auto-commit.
- **Benefit if done correctly:** Committing after successful processing guarantees **at-least-once delivery**. If the app crashes before the commit, the message is re-delivered on restart. (This requires your processing logic to be idempotent).
