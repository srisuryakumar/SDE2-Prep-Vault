---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 3 — Consistency Models"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: ["Strong Consistency (Linearizability)"]
tags: [distributed-systems, consistency]
---

# Sequential Consistency

## Intuition
**Guarantee:** Weaker than linearizability. All operations appear to happen in *some* single, agreed-upon sequential order — and each client's own operations appear in the order that client issued them. 

However, that agreed-upon order doesn't have to match real-world (wall-clock) time. Two concurrent operations could be ordered either way, as long as every node in the system agrees on the exact same order.

## Use Cases
Systems where global ordering matters more than matching real time, such as a replicated log where all replicas must process events in the same order.
