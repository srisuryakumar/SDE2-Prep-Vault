---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 5 — Partitioning and Sharding"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Consistent Hashing", "Hot Spots in Distributed Systems"]
tags: [database, distributed-systems, sharding]
---

# Hash Partitioning vs Range Partitioning

## Intuition
When sharding a database, you must decide how to assign a key to a specific partition. There are two primary strategies.

## Range Partitioning
Assign contiguous ranges of keys to partitions (e.g., dates: "Jan on Node 1, Feb on Node 2").
- **Pros:** Great for range queries (e.g., "get all events from last week") because you only need to query one partition.
- **Cons:** Highly susceptible to **hot spots**. If partitioning by date, today's partition takes 100% of the write traffic while older partitions sit idle.

## Hash Partitioning
Assign keys to partitions using a hash function: `hash(key) % num_partitions`.
- **Pros:** Distributes keys evenly across partitions, mitigating data-skew hot spots.
- **Cons:** Makes range queries very expensive (must query all partitions and merge results). Furthermore, naive hashing `modulo N` breaks down when `N` changes (adding/removing a node causes a near-total data reshuffle). This is solved by [[Consistent Hashing]].
