---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 5 — Partitioning and Sharding"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Virtual Nodes (Consistent Hashing)", "Hash Partitioning vs Range Partitioning"]
tags: [database, distributed-systems, sharding, algorithms]
---

# Consistent Hashing

## Intuition
Naive hash partitioning (`hash(key) % N`) forces almost every key to be reassigned when a node is added or removed (because `N` changes). Consistent hashing solves this rebalancing problem so that adding or removing a node only moves `1/N` of the keys.

## The Hash Ring
Imagine the hash output space (e.g., `0` to `2^32 - 1`) arranged in a circle. 
1. Both the **nodes** and the **keys** are hashed onto this same ring.
2. A key is assigned to the **first node found by moving clockwise** from the key's position on the ring.

## Adding or Removing a Node
If you add Node E between Node C and Node D on the ring:
- The keys between C and E now map to Node E.
- The keys between E and D *still* map to Node D.
- **Result:** Only the keys in Node E's immediate "neighborhood" are affected. All other keys on the ring stay exactly where they are.
