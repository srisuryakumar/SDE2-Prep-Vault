---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 1 — The Computer at Its Core"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations]
---

# CPU Caches and Cache Misses

The CPU is enormously faster than RAM. A register operation takes under 1 nanosecond, while fetching data from RAM takes ~100 nanoseconds. To bridge this gap, CPUs use **caches**.

## Memory Latency Hierarchy
- **Register**: <1 ns (always hit)
- **L1 Cache**: 1-4 ns (~32 KB per core)
- **L2 Cache**: 4-12 ns (~256 KB per core)
- **L3 Cache**: 30-40 ns (~8-32 MB shared)
- **RAM**: ~100 ns

## Cache Misses
When the CPU needs data, it checks L1. If found (**cache hit**), access is fast. If not (**cache miss**), it checks L2, L3, and finally fetches from RAM. A cache miss to RAM takes 25-100x longer than a cache hit.

### Why this matters (ArrayList vs LinkedList)
- **ArrayList**: Stores elements contiguously. The CPU prefetches adjacent elements into the L1 cache. Near-zero cache misses.
- **LinkedList**: Scatters nodes across the heap. Every `node.next` traversal is a potential cache miss (~100ns penalty).

This is why an O(n) ArrayList traversal is 10-100x faster in practice than an O(n) LinkedList traversal.

### HashMaps
A Java HashMap stores entries in a bucket array. When there are many hash collisions, entries form a linked list or TreeMap in that bucket, reintroducing cache misses and degrading performance.
