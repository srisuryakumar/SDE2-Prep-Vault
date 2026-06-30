---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 3 — How Programs Run"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, memory, call-stack]
---

# The Call Stack and StackOverflow

When a function is called, the CPU must track the return address, local variables, and function arguments. These are stored in a **stack frame**, allocated on the **call stack**. Each function call pushes a frame; each return pops one.

## Stack Allocation vs Heap Allocation
- **Stack:** Fast and virtually free. Controlled by moving the Stack Pointer register. No GC involvement.
- **Heap:** Slower. Used for objects created with `new`. Requires the memory allocator to find free space, initialize it, and eventually rely on Garbage Collection (GC) to clean it up.

### Escape Analysis
The JVM can perform **escape analysis**. If it detects that a new object never "escapes" the method it was created in (not returned or passed to another thread), it may allocate it on the stack instead of the heap, skipping GC overhead entirely.

## StackOverflowError
Each thread has a fixed-size stack (default 512KB-1MB in Java). When unbounded recursion or excessively deep call chains push too many frames, the stack runs out of space, and the JVM throws a `java.lang.StackOverflowError`.

To fix this, find the unbounded recursion (e.g., circular object references during JSON serialization) rather than just increasing the stack size (`-Xss`).
