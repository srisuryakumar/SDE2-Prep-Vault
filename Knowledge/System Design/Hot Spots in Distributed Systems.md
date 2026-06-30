---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 5 — Partitioning and Sharding"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Hash Partitioning vs Range Partitioning"]
tags: [database, distributed-systems, architecture]
---

# Hot Spots in Distributed Systems

## Intuition
Even if you use perfectly even hash partitioning to distribute your data, you can still experience a **hot spot** due to an uneven *access pattern*.
For example, if a celebrity on a social network goes viral, their specific user record might get 10,000x the read/write traffic of an average user. That single partition will be overwhelmed, even while other partitions sit idle.

## Strategies to Fix Hot Spots
- **Key Salting:** For heavy writes, append a random suffix to the hot key (e.g., `user_123_01`, `user_123_02`, up to `100`). This splits the data and writes across multiple partitions. On read, the application must query all 100 partitions and merge the results.
- **Caching:** For heavy reads, place a caching layer (e.g., Redis) in front of the database so most reads never hit the partition.
- **Dedicated Capacity:** Detect known-hot keys and dynamically route them to dedicated, over-provisioned capacity rather than standard partitions.
