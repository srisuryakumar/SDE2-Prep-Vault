---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, executor, thread-pool]
---

# Java ExecutorService

Creating a new OS-level `Thread` for every task is expensive (takes ~1ms and consumes ~1MB stack memory). `ExecutorService` manages a pool of reusable threads to execute asynchronous tasks efficiently.

## Core Pool Types (`Executors` factory)
1. **Fixed Thread Pool (`newFixedThreadPool(N)`):** Exactly N threads. Tasks queue up if all threads are busy. Good for CPU-bound tasks (N = CPU cores).
2. **Cached Thread Pool (`newCachedThreadPool()`):** Creates new threads as needed, reuses idle ones. DANGEROUS under load because it is unbounded (can create thousands of threads and cause OutOfMemory).
3. **Single Thread Executor (`newSingleThreadExecutor()`):** One thread, processes tasks sequentially.
4. **Scheduled Executor (`newScheduledThreadPool()`):** For periodic or delayed tasks.

## Submitting Tasks
- `submit(Runnable)`: Returns a `Future<?>` (get() returns null).
- `submit(Callable<T>)`: Returns a `Future<T>` holding the computed result.
Calling `future.get()` blocks the current thread until the task completes.

## Shutdown
Always shut down an ExecutorService when done, otherwise the application won't exit (the threads stay alive).
- `shutdown()`: Stops accepting new tasks, lets current/queued tasks finish.
- `shutdownNow()`: Attempts to interrupt running tasks and returns queued tasks.
