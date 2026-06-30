---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 4 — Replication"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Leader-Follower (Master-Replica) Replication"]
tags: [database, distributed-systems, architecture]
---

# Database Replication (Why replicate)

## Intuition
Replication is keeping a copy of the same data on multiple machines connected via a network.

## Why replicate at all?
1. **Fault tolerance:** If data lives on only one node and it dies (or disk fails), the data is gone. Multiple copies ensure durability and availability.
2. **Read scaling:** One node can only serve a finite number of reads per second. Spreading reads across multiple copies multiplies read capacity.
3. **Geographic distribution:** Putting a replica physically close to users in Tokyo means they don't pay the latency penalty of round-tripping to a primary database in Virginia.
