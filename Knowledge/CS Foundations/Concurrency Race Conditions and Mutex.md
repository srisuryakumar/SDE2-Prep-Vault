---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, concurrency]
---

# Concurrency Race Conditions and Mutex

## Race Conditions
A race condition occurs when two or more threads access shared mutable state without synchronization, and the outcome depends on their execution order. 

At the hardware level, a "read-modify-write" sequence (like `counter++`) is not atomic—it's three operations. If two threads read the counter at 5 and both add 1, they may both write back 6 instead of 7.

To prevent race conditions, use synchronization (`synchronized`, `ReentrantLock`), atomic variables (`AtomicInteger`), or design immutable shared state.

## Mutex (Mutual Exclusion Lock)
A mutex is an OS primitive that allows only one thread to hold it at a time. Any other thread trying to acquire a held mutex will **block** (enter the WAITING state) until the holder releases it.

Java's `synchronized` keyword is built on mutex-like primitives (OS mutexes or hardware Compare-And-Swap instructions).
