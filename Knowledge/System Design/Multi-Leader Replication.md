---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 4 — Replication"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Leader-Follower (Master-Replica) Replication"]
tags: [database, distributed-systems, replication]
---

# Multi-Leader Replication

## Intuition
Instead of one leader, **multiple nodes can accept writes**. Typically, there is one leader per data center/region. Each region writes locally (low latency), then replicates to the other leaders asynchronously.

## Why use it?
It solves the latency problem of a geographically distributed user base where every write would otherwise have to cross an ocean to a single leader.

## The Cost: Write Conflicts
Because multiple leaders can accept writes concurrently, two users (one in the US, one in the EU) might update the *same record* simultaneously. The two leaders now disagree. The system needs a conflict resolution strategy (e.g., last-write-wins by timestamp, custom merge functions, or application-level resolution) to reconcile them.
