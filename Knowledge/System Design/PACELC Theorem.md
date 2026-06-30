---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 2 — CAP Theorem"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["CAP Theorem"]
tags: [distributed-systems, architecture]
---

# PACELC Theorem

## Intuition
CAP Theorem only describes a system's behavior *during* a network partition. But partitions are rare. PACELC extends CAP to describe the trade-off during *normal* operation.

## The Theorem
**If Partition (P), choose Availability (A) or Consistency (C); Else (E), choose Latency (L) or Consistency (C).**

## Why it matters
Even with a perfectly healthy network, requiring a write to be confirmed by replicas adds latency. You must trade off **Latency vs Consistency** every single day.
- A system like Cassandra is PA/EL (Available during partition, Low Latency normally).
- A traditional synchronous RDBMS is PC/EC (Consistent by refusing during partition, Consistent normally by paying the Latency cost of synchronous replication).
