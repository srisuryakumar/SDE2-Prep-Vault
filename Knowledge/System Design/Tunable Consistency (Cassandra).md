---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 2 — CAP Theorem"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["CAP Theorem", "PACELC Theorem"]
tags: [database, cassandra, distributed-systems]
---

# Tunable Consistency (Cassandra)

## Intuition
Systems like Cassandra don't force you into a single, hardcoded position on the CAP spectrum. They offer **tunable consistency** on a per-query basis.

## Consistency Levels (CL)
- **`ONE`**: Acknowledge as soon as 1 replica responds. High availability, low latency, weak consistency.
- **`QUORUM`**: Acknowledge once a majority of replicas respond. Balanced.
- **`ALL`**: Acknowledge only when every replica responds. Strong consistency, but low availability (one slow node blocks the write) and high latency.

## Strong Consistency with Quorums
You can achieve strong consistency by configuring: `Write CL + Read CL > Replication Factor`.
If Replication Factor is 3, writing at `QUORUM` (2) and reading at `QUORUM` (2) ensures that `2 + 2 > 3`. The read quorum and write quorum are mathematically guaranteed to overlap on at least one node, ensuring the read always sees the latest acknowledged write.
