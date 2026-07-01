---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, atomic, cas]
---

# Java Atomic Classes and CAS

The `java.util.concurrent.atomic` package provides lock-free thread safety using hardware-level **CAS (Compare-And-Swap)** instructions.

## Compare-And-Swap (CAS)
CAS is a single, uninterruptible CPU instruction. It says: "If the value at this memory address is still X (what I expect), change it to Y. Otherwise, fail and let me retry." Because it doesn't block OS threads, it is much faster than `synchronized` under moderate contention.

## Key Classes
- `AtomicInteger` / `AtomicLong`: Use for thread-safe counters (`incrementAndGet()`).
- `AtomicReference<T>`: Atomically update an object reference.
- `AtomicStampedReference<T>`: Solves the ABA problem by attaching a version stamp to the reference.
- `LongAdder`: Better than `AtomicLong` under extremely high contention. It distributes updates across multiple internal cells to reduce CAS failures, then sums them up on read. Perfect for high-throughput metrics counters.
