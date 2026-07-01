---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, synchronized, locks]
---

# Java Synchronized Keyword

`synchronized` is the heaviest but most complete concurrency primitive in Java. It solves all three concurrency problems at once.

## What it Does
1. **Atomicity:** It provides mutual exclusion (a monitor lock). Only one thread can execute inside the synchronized block at a time.
2. **Visibility:** On lock release, it flushes all writes to main memory. On lock acquire, it forces reads from main memory.
3. **Ordering:** It prevents the JVM from reordering instructions across the lock boundaries.

## Usage Forms
1. **Synchronized Method:** `public synchronized void doWork()` locks on `this` (the instance).
2. **Static Synchronized Method:** `public static synchronized void doWork()` locks on the Class object (shared across all instances).
3. **Synchronized Block:** `synchronized(lockObject) { ... }` allows fine-grained locking on a specific object, improving throughput by only locking the critical section.

## Re-entrancy
Java monitors are **reentrant**. If a thread already holds a lock on an object, it can enter another synchronized block/method that requires the same lock without deadlocking itself. The JVM just increments a hold-count.
