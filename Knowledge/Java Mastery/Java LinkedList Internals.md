---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, collections, lists]
---

# Java LinkedList Internals

`LinkedList` in Java is a doubly-linked list. Each node holds the element, a pointer to the previous node, and a pointer to the next node.

## Time Complexity
- `addFirst()` / `addLast()`: **O(1)**
- `removeFirst()` / `removeLast()`: **O(1)**
- `get(index)`: **O(n)** — It must traverse from the head (or tail) to find the element.

## Why LinkedList Usually Loses to ArrayList
In theory, `LinkedList` has O(1) insertion in the middle (if you already have the node reference). In practice, `LinkedList` almost always performs worse than `ArrayList` because of **CPU Cache Performance**.

- `ArrayList` stores data in contiguous memory (`Object[]`). The CPU prefetcher loads adjacent elements into the L1 cache, making iteration extremely fast.
- `LinkedList` stores nodes at random locations across the Heap. Traversing it causes constant **cache misses** (fetching from main RAM), making it drastically slower for iteration.
- `LinkedList` also consumes significantly more memory overhead per element (pointers + object headers).

*Verdict:* Use `ArrayList` for lists, and `ArrayDeque` for queues and stacks. Avoid `LinkedList`.
