---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 5 — Partitioning and Sharding"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Consistent Hashing"]
tags: [database, distributed-systems, sharding]
---

# Virtual Nodes (Consistent Hashing)

## Intuition
In standard consistent hashing, if each physical node is assigned just one position on the hash ring, the distribution can be very uneven. One node might randomly own a massive arc of the ring (and thus most of the data), while another owns a tiny arc. Additionally, if a node fails, its entire load shifts to a single counter-clockwise neighbor, overwhelming it.

## The Solution
Instead of one position, assign each physical node **many positions on the ring** (e.g., 100+ "virtual nodes").
- Node A maps to `A-v1`, `A-v2`, ... `A-v100`.
- Node B maps to `B-v1`, `B-v2`, ... `B-v100`.

## Benefits
1. **Even Distribution:** The node's "share" of the ring is the sum of many small, randomly distributed arcs, averaging out to a very even data distribution.
2. **Safe Failovers:** If Node A fails, its load doesn't hit a single neighbor. It hits the neighbors of its 100 virtual nodes, spreading the load of the failed node evenly across the rest of the cluster.
