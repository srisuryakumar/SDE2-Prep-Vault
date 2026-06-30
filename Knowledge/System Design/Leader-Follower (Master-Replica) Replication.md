---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 4 — Replication"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Multi-Leader Replication", "Leaderless Replication (Dynamo-style)"]
tags: [database, distributed-systems, replication]
---

# Leader-Follower (Master-Replica) Replication

## Intuition
The most common replication topology. One node (the **leader**) accepts all writes. The rest (the **followers**) replicate the leader's changes and serve reads.
This avoids write conflicts (as writes happen in one place) but makes the leader a bottleneck for writes and a single point of failure.

## Synchronous vs Asynchronous
- **Synchronous:** The leader waits for followers to acknowledge the write before responding to the client. Highly durable, but latency is tied to the slowest follower, and if a follower is down, the write fails.
- **Asynchronous:** The leader responds to the client immediately and replicates in the background. Fast writes, but risks data loss if the leader crashes before the write replicates to followers.
*(Most production systems use a hybrid: one synchronous follower for durability, the rest asynchronous).*

## Replication Lag
Because followers apply changes after the leader, there is a window (milliseconds to seconds) where the follower's data is stale. A client might write data, read it from a follower, and not see their write. (See [[Read-Your-Writes Consistency]]).
