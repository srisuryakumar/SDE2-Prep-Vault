---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, javascript]
---

# Concurrency - JavaScript vs Java Mental Model

Before writing concurrent Java, you must unlearn the JavaScript mental model.

## JavaScript
- **Single-threaded event loop:** Only one thing runs at a time.
- **Asynchronous != Parallel:** `async/await` and Promises are cooperative yielding, not true parallelism. They interleave on a single thread.
- **No shared state problems:** You cannot have a race condition in pure JS because two threads never read/write the same memory simultaneously.

## Java
- **True OS Threads:** Multiple threads run literally simultaneously on different CPU cores.
- **Shared Memory:** Two threads CAN and WILL read/write the same memory at the same time.
- **Race conditions are the default:** If you don't coordinate access with locks or atomics, results are unpredictable, non-reproducible, and data-corrupting. Everything in `java.util.concurrent` exists to solve this problem.
