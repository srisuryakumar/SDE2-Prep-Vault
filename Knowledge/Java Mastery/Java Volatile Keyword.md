---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, volatile, visibility]
---

# Java Volatile Keyword

`volatile` ensures **Visibility and Ordering**, but NOT **Atomicity**.

## What it Does
It guarantees that any thread that reads a field will see the most recently written value. It bypasses CPU caches, reading from and writing to main memory directly.

## What it Does NOT Do
It does not prevent race conditions on compound operations. `volatile int count; count++;` is still unsafe because `count++` is a read-modify-write operation. Two threads can still read the same memory value simultaneously, increment it, and write back the same result, losing an update.

## Perfect Use Cases
1. **Simple boolean flags:** e.g., a `running` flag to stop a background thread.
2. **Atomic reference replacement:** `volatile Map cache = new HashMap();`
3. **Double-Checked Locking:** Used heavily in Thread-Safe Singleton implementations to prevent other threads from seeing a partially-constructed object due to instruction reordering.
