---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, concurrency, loom, virtual-threads]
---

# Java Virtual Threads (Project Loom)

Virtual Threads (introduced in Java 21) revolutionize concurrency in Java by decoupling threads from OS threads.

## The Problem with Traditional Threads
Traditional Java threads are mapped 1:1 to OS threads. OS threads are heavy (require ~1MB stack space each). If you have 10,000 concurrent HTTP requests that are mostly waiting on a database (I/O bound), creating 10,000 OS threads will crash the JVM/OS (OutOfMemory).

## How Virtual Threads Work
The JVM maintains a small pool of OS "carrier" threads (usually one per CPU core). It can multiplex millions of lightweight **Virtual Threads** onto these few carrier threads.
When a Virtual Thread performs a blocking I/O operation (e.g., HTTP call, DB query, `Thread.sleep`), it **yields** — it unmounts from its carrier thread. The carrier thread is now free to run another virtual thread. When the I/O finishes, the virtual thread is remounted and resumes.

## When to Use
- **YES:** High-concurrency, I/O-bound workloads (web servers, microservice communication, database access).
- **NO:** CPU-bound workloads. A virtual thread doing heavy math still occupies a CPU core just like a regular thread.
- **NO:** Avoid using `synchronized` blocks around I/O operations inside a virtual thread, as this "pins" the virtual thread to the carrier thread, defeating the purpose. Use `ReentrantLock` instead.
