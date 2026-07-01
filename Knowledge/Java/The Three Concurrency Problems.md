---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, problems]
---

# The Three Concurrency Problems

Every concurrency bug in Java is a manifestation of one or more of these three fundamental problems:

## 1. Visibility
Modern CPUs have local caches (L1, L2). When Thread A running on Core 0 writes to a variable, it often writes to its local L1 cache first. Thread B running on Core 1 might read a stale value from its own cache because the main memory hasn't been updated yet.
*Solution: `volatile`, `synchronized`, Atomics*

## 2. Atomicity
A single line of Java like `counter++` is actually three CPU instructions: READ, MODIFY, WRITE. The thread scheduler can preempt a thread in the middle of these operations. If two threads read the same value before either writes back, one update is lost.
*Solution: `synchronized`, Atomics*

## 3. Ordering (Instruction Reordering)
The JIT compiler and CPU can reorder instructions to optimize performance, as long as the logic remains correct from the perspective of a *single thread*. However, this can break logic if another thread is watching those variables.
*Solution: `volatile`, `synchronized` (Memory Barriers)*
