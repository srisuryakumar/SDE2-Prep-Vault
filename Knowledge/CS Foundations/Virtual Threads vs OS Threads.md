---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, os, concurrency]
---

# Virtual Threads vs OS Threads

## OS Threads (Kernel Threads)
Managed by the OS kernel. 
- Creating one requires a syscall (e.g. `clone()`).
- High overhead: Default stack size is ~1 MB on Linux. 10,000 threads = 10 GB RAM just for stacks.
- Expensive context switches (~1-10 microseconds).
- Java's standard `Thread` (before Java 21) mapped 1-to-1 with OS threads.

## Green Threads
Managed entirely by the language runtime (like old Java or Go's goroutines), invisible to the OS. The OS sees a few OS threads, and the runtime multiplexes many lightweight threads on top.

## Virtual Threads (Java 21)
Managed by the JVM, mounted on a small pool of OS "carrier threads" (usually equal to CPU cores). 
- When a virtual thread blocks on I/O, the JVM unmounts it and runs another virtual thread on the same OS carrier thread.
- Very lightweight (a few KB of heap, not a 1MB stack).
- Allows applications to handle millions of concurrent connections without hitting OS thread limits or requiring reactive programming.

This is why Spring Boot 3.2+ with virtual threads (`spring.threads.virtual.enabled=true`) can handle vastly more concurrent connections.
