---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, concurrency, threads, lifecycle]
---

# Java Thread Creation and Lifecycle

## Creation
There are three ways to define a thread's task:
1. **Runnable (Preferred):** Provide a lambda or class implementing `Runnable`. Returns no value.
2. **Callable:** Like Runnable but can return a value and throw checked exceptions. Requires an Executor to run.
3. **Extend Thread:** Subclass `Thread` and override `run()`. Rarely done in modern Java.

To start a thread, you must call `start()`. Do NOT call `run()` directly, as it will simply execute synchronously on the current thread.

## Lifecycle States
- **NEW:** Thread object created, `start()` not yet called.
- **RUNNABLE:** `start()` called. It is either running on the CPU or scheduled and waiting for CPU time.
- **BLOCKED:** Waiting to acquire a monitor lock (e.g., trying to enter a `synchronized` block held by another thread).
- **WAITING:** Waiting indefinitely for another thread to wake it up (`Object.wait()`, `Thread.join()` with no timeout).
- **TIMED_WAITING:** Waiting for a specific amount of time (`Thread.sleep(ms)`, `Object.wait(timeout)`).
- **TERMINATED:** The `run()` method completed (normally or via exception).
