---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 7 — Java Concurrency"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, concurrency, completablefuture, async]
---

# Java CompletableFuture

`CompletableFuture` (Java 8) is Java's composable asynchronous primitive, similar to JavaScript Promises. It allows you to build complex non-blocking pipelines without callback hell.

## Key Methods
- **Creation:** `supplyAsync(() -> result)` runs a task asynchronously.
- **Transformation:** `thenApply(Function)` transforms the result synchronously; `thenApplyAsync` does it on another thread.
- **Composition (FlatMap):** `thenCompose(Function)` chains dependent futures where the next step also returns a `CompletableFuture`.
- **Parallel Execution:** `CompletableFuture.allOf(cf1, cf2, cf3)` waits for multiple futures to complete in parallel. This is incredibly useful for hitting multiple independent microservices simultaneously, reducing total latency to the `max(T1, T2, T3)`.
- **Error Handling:** `exceptionally(Function)` provides a fallback value if an exception occurs in the chain.

## Example: Parallel API Calls
```java
CompletableFuture<User> userFuture = fetchUserAsync();
CompletableFuture<Orders> ordersFuture = fetchOrdersAsync();

CompletableFuture.allOf(userFuture, ordersFuture).thenRun(() -> {
    // Both are done, retrieve values without blocking
    User user = userFuture.join(); 
    Orders orders = ordersFuture.join();
    System.out.println(user + " has " + orders);
});
```
