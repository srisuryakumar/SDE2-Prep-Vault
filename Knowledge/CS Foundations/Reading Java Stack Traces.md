---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 6 — Developer Environment, Git, and Tooling"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, tooling, debugging]
---

# Reading Java Stack Traces

When a Java exception goes uncaught, the JVM prints a stack trace to stderr. Reading it correctly is a critical daily skill.

## How to Read a Stack Trace
1. **Read the last "Caused by:" first:** This is the root cause. Everything above it is the propagation chain.
2. **Find your code:** Ignore framework lines (org.springframework, org.apache.catalina, java.lang). Look for your package name (e.g., `com.surya`). The root cause is in *your* code at the line indicated.
3. **Understand the order:** The stack reads from innermost (top) to outermost (bottom). The method at the top threw the exception, and it propagated down the list.

## Common Exceptions
- **NullPointerException:** Method called on a null reference. (Java 17+ indicates exactly what was null).
- **ClassCastException:** Casting a value to an incompatible type.
- **ArrayIndexOutOfBoundsException:** Index ≥ length or < 0.
- **StackOverflowError:** Stack exhausted, usually infinite recursion.
- **OutOfMemoryError (Heap):** Heap is full, often a memory leak (objects accumulating in long-lived collections).
- **LazyInitializationException:** Hibernate-specific; accessing a lazy-loaded relationship outside of a `@Transactional` context after the session closed.
