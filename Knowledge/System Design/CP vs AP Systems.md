---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 2 — CAP Theorem"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["CAP Theorem"]
tags: [distributed-systems, cap]
---

# CP vs AP Systems

## Intuition
When a network partition happens, a distributed system must choose to be either CP or AP.

## CP Systems (Consistency + Partition Tolerance)
- **Behavior:** They refuse requests on the minority side of the partition rather than risk serving stale or conflicting data. They become *unavailable*.
- **When to use:** When being wrong is worse than being down. Used for leader election, distributed locks, and critical configuration.
- **Examples:** ZooKeeper, etcd, HBase.

## AP Systems (Availability + Partition Tolerance)
- **Behavior:** They continue to serve requests on both sides of the partition. The data will diverge (conflict), and must be reconciled later when the partition heals (e.g., via last-write-wins or vector clocks).
- **When to use:** When availability matters more than perfect consistency. Used for shopping carts, social media likes, analytics.
- **Examples:** Cassandra, DynamoDB, CouchDB.
