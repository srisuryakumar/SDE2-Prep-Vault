---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, collections, summary]
---

# Choosing the Right Collection

When answering interview questions or designing a system, selecting the correct Java collection is crucial. Use this decision matrix:

| Requirement | Preferred Collection |
| :--- | :--- |
| Indexed access by position | `ArrayList` |
| FIFO Queue | `ArrayDeque` |
| LIFO Stack | `ArrayDeque` |
| Priority ordering (Min/Max Heap) | `PriorityQueue` |
| Key $\rightarrow$ Value lookup ($O(1)$) | `HashMap` |
| Unique elements ($O(1)$) | `HashSet` |
| Sorted keys | `TreeMap` |
| Sorted unique elements | `TreeSet` |
| Insertion order preserved | `LinkedHashMap` / `LinkedHashSet` |
| LRU Cache | `LinkedHashMap` (access-order mode) |
| Thread-safe map | `ConcurrentHashMap` |
| Frequent middle insert/remove | `LinkedList` *(Rare: verify with profiling)* |
