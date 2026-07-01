---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, memory-model, happens-before]
---

# Java Memory Model and Happens-Before

The Java Memory Model (JMM) defines when a write by one thread is guaranteed to be visible to a read by another thread. This is governed by the **happens-before (HB)** relationship. If Action A happens-before Action B, B is guaranteed to see the results of A.

## Key Happens-Before Rules
1. **Program Order:** Within a single thread, each action HB the next.
2. **Monitor Lock:** An unlock of a monitor HB every subsequent lock of that SAME monitor. (This is why `synchronized` guarantees visibility).
3. **Volatile Variable:** A write to a `volatile` variable HB subsequent reads of that same variable.
4. **Thread Start:** `Thread.start()` HB all actions performed inside the started thread.
5. **Thread Join:** All actions in a thread HB the return of `Thread.join()` for that thread.

If there is no happens-before relationship between two operations, the JVM and CPU are free to reorder them, and you have a race condition or visibility bug.
