---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, concurrency, locks, reentrant]
---

# Java ReentrantLock and Condition

`ReentrantLock` is an explicit locking mechanism providing more flexibility than `synchronized`.

## Key Features
- **tryLock():** Non-blocking lock attempt. Returns `true` if acquired, `false` if held by another thread. Allows you to back off instead of waiting forever.
- **tryLock(timeout):** Wait up to N units of time to acquire the lock.
- **lockInterruptibly():** Wait for the lock, but can be interrupted by another thread while waiting.
- **Fairness:** `new ReentrantLock(true)` grants the lock to the longest-waiting thread, preventing starvation (at the cost of some throughput).

## Best Practice
ALWAYS release explicit locks in a `finally` block to prevent deadlocks if an exception is thrown.
```java
lock.lock();
try {
    // critical section
} finally {
    lock.unlock(); // ALWAYS do this
}
```

## Condition
`Condition` provides per-lock wait queues. It replaces `wait()`/`notify()` with `.await()` and `.signal()`. This is useful for bounded blocking queues, where you can have separate `notEmpty` and `notFull` conditions on the same lock.
