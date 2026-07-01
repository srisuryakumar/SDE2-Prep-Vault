---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 3 — Redis"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [redis, cluster, consistent-hashing]
---

# Redis Cluster and Consistent Hashing

## Intuition
Redis Cluster allows horizontal scaling of Redis across multiple nodes.

## Consistent Hashing (16,384 Slots)
Every key is assigned to one of exactly 16,384 hash slots.
`HASH_SLOT = CRC16(key) mod 16384`

These slots are distributed across nodes (e.g. 3 nodes each take 1/3 of the slots). Each node has N replicas for fault tolerance.
If a client sends a command to the wrong node, the node responds with a `MOVED` redirection, pointing the client to the correct node. The client transparently redirects and caches the new mapping.

## Hash Tags
Sometimes you need multiple keys to live on the SAME node (e.g., for multi-key transactions). You can force this using **Hash Tags** `{}`.
- `{user:1}:session`
- `{user:1}:cart`
Both keys hash based on just `"user:1"`, ensuring they map to the exact same slot and node.

## Online Resizing
Adding a new node happens with zero downtime:
1. New node joins cluster.
2. Admin reassigns a portion of slots to the new node.
3. Keys in those slots migrate atomically (one slot at a time).
4. Clients are redirected via `MOVED` responses.
