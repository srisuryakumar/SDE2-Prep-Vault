---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, collections, hashmap]
---

# ConcurrentHashMap Internals

`ConcurrentHashMap` is a highly optimized, thread-safe hash map that performs much better under load than a `Collections.synchronizedMap()`.

## How it achieves concurrency
Instead of locking the entire data structure on every read/write, it uses:
- **CAS (Compare-And-Swap) for reads:** Reads are lock-free and extremely fast.
- **Lock Striping / Per-Bucket Locks for writes:** When inserting or updating an element, it only synchronizes on the specific bucket (or node) being modified. Multiple threads can write to the map simultaneously as long as they are writing to different buckets.

## Useful Atomic Operations
It provides powerful atomic methods for concurrent programming:
- `computeIfAbsent(key, function)`: Atomically checks if a key exists, and if not, computes the value and inserts it. The computation lambda is guaranteed to run at most once per key. Excellent for building caches.
- `merge(key, value, remappingFunction)`: Atomically updates a value, perfect for concurrent counters.
- `compute(key, remappingFunction)`: Atomically updates an existing value.
