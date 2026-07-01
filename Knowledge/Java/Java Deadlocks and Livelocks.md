---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, deadlock, starvation]
---

# Java Deadlocks and Livelocks

## Deadlock
A deadlock occurs when two or more threads are waiting for locks held by each other, forming an inescapable circular dependency.

### The Four Coffman Conditions (Must all hold for deadlock)
1. **Mutual exclusion:** Resources can't be shared.
2. **Hold and wait:** Thread holds a lock while waiting for another.
3. **No preemption:** Locks can't be forcibly taken away.
4. **Circular wait:** Thread A waits for B, B waits for A.

### Prevention Strategies
1. **Consistent Lock Ordering:** If all threads always acquire `lockA` before `lockB`, a circular wait is mathematically impossible.
2. **Timeouts:** Use `tryLock(timeout)` instead of `synchronized`. If a thread can't get all needed locks, it backs off, releases its current locks, and retries.

## Livelock
Threads aren't blocked, but they keep changing states in response to each other, making no actual progress. (e.g., two people politely stepping in the same direction to let the other pass). Fix by introducing random back-off times.

## Starvation
A thread perpetually fails to acquire a resource because other (often higher priority) threads always get it first. Fix by using fair locks (`new ReentrantLock(true)`).
