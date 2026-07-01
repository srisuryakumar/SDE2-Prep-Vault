---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 4 — Behavioral Patterns"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, behavioral]
---

# Iterator Pattern

## Intuition
You want to allow clients to traverse a collection of elements without exposing the underlying internal structure (whether it's an Array, a Tree, a Linked List, or a Circular Buffer).

## The Solution
1. The collection provides an `iterator()` method that returns an `Iterator` object.
2. The `Iterator` interface defines standard traversal methods: `hasNext()` and `next()`.
3. The client writes a standard `while(iterator.hasNext())` loop. The client is completely decoupled from the data structure, meaning you can swap an `ArrayList` for a `TreeSet` without breaking the client code.
