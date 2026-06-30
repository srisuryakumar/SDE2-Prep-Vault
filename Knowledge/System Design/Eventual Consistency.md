---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 3 — Consistency Models"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Consistency Models Overview"]
tags: [distributed-systems, consistency]
---

# Eventual Consistency

## Intuition
**Guarantee:** If no new writes occur, all replicas will *eventually* converge to the same value. There is no bound on how long "eventually" takes, and no guarantee about what you'll see in the meantime (you may see stale data).

## The Trade-off
This is the default model for systems like DynamoDB and Cassandra. It is the cheapest model to provide because replicas don't have to coordinate before responding. This allows it to scale incredibly well horizontally.

## Use Cases
- Product catalog data
- View counters
- Recommendation data
Anywhere a brief window of staleness is an acceptable trade for speed and availability.
