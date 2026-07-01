---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, collections, stack, queue]
---

# ArrayDeque

`ArrayDeque` stands for Array Double-Ended Queue. It is backed by a resizable **circular array**.

## The Best Stack and Queue
In Java, **always use `ArrayDeque` for Stacks and Queues**.
- **Do not use `Stack`:** The legacy `java.util.Stack` class extends `Vector`, meaning every operation is synchronized, making it unnecessarily slow in single-threaded environments.
- **Do not use `LinkedList`:** While `LinkedList` implements `Deque`, `ArrayDeque` is significantly faster because contiguous array storage is highly cache-friendly compared to the pointer-chasing overhead of a linked list.

## Operations
Because it is double-ended, you can add or remove from either side in **$O(1)$** time:
- **Stack (LIFO):** `push(e)`, `pop()`, `peek()`
- **Queue (FIFO):** `offer(e)`, `poll()`, `peek()`
- **Deque:** `addFirst(e)`, `addLast(e)`, `pollFirst()`, `pollLast()`
