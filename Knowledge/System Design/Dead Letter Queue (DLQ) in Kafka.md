---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Consumer Commit (Auto vs Manual)"]
tags: [kafka, messaging, error-handling]
---

# Dead Letter Queue (DLQ) in Kafka

## Intuition
When a consumer fails to process a message, it cannot simply skip it (that's data loss) and it shouldn't retry infinitely (that blocks the partition). 
A Dead Letter Queue (DLQ) is a separate topic where messages are sent after they exhaust all retry attempts, allowing the main partition to continue processing while failed messages are parked for later review.

## Spring Kafka's `@RetryableTopic`
Spring Kafka provides `@RetryableTopic` to automatically create retry topics (`retry-0`, `retry-1`) with backoff delays, and eventually route to a DLQ (`-dlt`) upon exhaustion.

## What NOT to retry
Only retry **transient** failures (network blips, brief downstream unavailability). 
**Do not retry** on deserialization errors or business logic validation failures (e.g., "order amount is negative"). Retrying these just wastes CPU producing the exact same guaranteed failure before landing on the DLQ anyway. Route them to the DLQ immediately.

## What to do with the DLQ
Never just delete messages on the DLQ. Options:
1. **Log and alert:** Someone gets paged, reviews, and manually fixes it.
2. **Persist to a dashboard:** Operations can triage a backlog async.
3. **Automated reprocessing:** A tool replays DLQ messages back onto the original topic once the root cause is fixed.
