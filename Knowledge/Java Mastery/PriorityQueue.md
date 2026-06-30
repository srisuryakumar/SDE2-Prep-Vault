---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, collections, queue, heap]
---

# PriorityQueue

A `PriorityQueue` is an implementation of a **Heap** data structure in Java. 

## Characteristics
- **Default:** By default, it is a **MIN-heap** (the smallest element is always at the head).
- **Custom Ordering:** You can create a MAX-heap by passing `Comparator.reverseOrder()` or providing a custom comparator.
- **Internal Structure:** It is implemented as a binary heap stored in a dynamic array.

## Performance
- `peek()`: **$O(1)$** — The root of the heap (the min/max) is always at index 0 of the array.
- `offer(e)` / `poll()`: **$O(log n)$** — Adding or removing requires "bubbling up" or "bubbling down" to maintain the heap property.
- `contains(e)`: **$O(n)$** — A heap is partially ordered, not fully sorted. Finding an arbitrary element requires scanning the array.
