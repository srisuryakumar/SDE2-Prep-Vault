---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 4 — Replication"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Tunable Consistency (Cassandra)", "Leader-Follower (Master-Replica) Replication"]
tags: [database, distributed-systems, cassandra, replication]
---

# Leaderless Replication (Dynamo-style)

## Intuition
There is no leader at all. A client writes to **N** replicas directly and considers the write successful once **W** of them acknowledge. To read, a client queries **R** replicas and takes the most recent value among the responses.

## Tuning N, R, and W
- **N**: Total replicas.
- **W**: Write quorum (number of nodes that must ACK a write).
- **R**: Read quorum (number of nodes queried for a read).

If `W + R > N`, the read and write sets are mathematically guaranteed to overlap on at least one node, ensuring the read will always return the latest write (strong-ish consistency).
If `W = 1`, writes are extremely fast and highly available, but durability is weak. If `W = 3` (on `N=3`), writes are strongly durable but fail if even one node goes down.

This equation is the foundation of Cassandra's tunable consistency.
