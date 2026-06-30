---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 6 — Generics and Functional Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, streams, functional, collections]
---

# Java Streams API

The Streams API allows declarative processing of collections. Unlike JavaScript's array methods (`.filter().map()`) which are eager and create intermediate arrays at each step, **Java Streams are lazy**.

## Laziness and Short-Circuiting
A stream consists of intermediate and terminal operations:
- **Intermediate operations** (`filter`, `map`, `sorted`, `limit`): These do not execute immediately. They merely build a pipeline description.
- **Terminal operations** (`collect`, `findFirst`, `count`, `forEach`): These trigger the actual execution of the pipeline.

Because they are lazy, streams can optimize processing (Short-Circuiting). For instance, if you do `.filter(condition).findFirst()`, the stream will process elements one by one through the filter and **stop entirely** the moment it finds the first match. It does not filter the rest of the million-element list.

## Parallel Streams
You can easily distribute work across CPU cores using `.parallelStream()`. However, this should only be used for very large datasets and CPU-bound operations. Using it for small collections adds overhead that makes it slower than sequential processing, and using it with I/O or shared mutable state can cause severe bugs.
