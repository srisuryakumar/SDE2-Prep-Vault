---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 5 — Hash Maps and Hash Sets"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, hash-map, hash-set, fundamentals]
---

# Hash Map and Hash Set Fundamentals

## The Trade
A HashMap trades **$O(n)$ extra space** for **$O(1)$ average time per lookup/insert**. 
Always mention the $O(n)$ space cost in interviews. A HashMap solution that doesn't mention its space cost is incomplete.

## Internals Quick Review
- Array of buckets.
- Hash function maps each key to a bucket index.
- Collisions handled by chaining (linked lists, which upgrade to red-black trees in Java when a bucket exceeds 8 entries).
- Worst case is $O(n)$ (or $O(\log n)$ with trees) per operation if collisions are adversarial.
- `HashSet` is just a `HashMap` under the hood, storing a dummy value against every key.

## When to Reach for a HashMap
Three signals:
1. You need $O(1)$ average lookup/insert instead of an $O(n)$ linear scan or $O(\log n)$ sorted search.
2. You're counting something — frequencies, occurrences, duplicates.
3. You're asking "have I seen this value/state before?" — deduplication, complement-checking, visited-tracking.
