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

# Deadlock

A deadlock occurs when two or more threads are each waiting for a lock that another thread holds, and none can proceed.

**Example:**
- Thread A holds `Lock1` and waits for `Lock2`.
- Thread B holds `Lock2` and waits for `Lock1`.
Neither can release their lock because they are waiting. The system freezes.

## Prevention
To prevent deadlock, you can break any of the Coffman conditions (mutual exclusion, hold and wait, no preemption, circular wait). Common strategies:
1. Acquire locks in the same global order across all threads.
2. Use `tryLock()` with a timeout instead of blocking indefinitely.
3. Use lock-free data structures (`ConcurrentHashMap`, `AtomicInteger`).
4. Avoid mutable shared state by using immutable objects.

In databases, Spring's `@Transactional` can cause deadlocks if two transactions update the same rows in opposite orders. Database engines resolve this by killing one transaction.
