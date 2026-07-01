---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, strings, interview]
---

# String vs StringBuilder vs StringBuffer

A classic Java interview question.

## 1. String
- **Immutability:** Immutable. Operations like concatenation (`+`) create an entirely new `String` object on the Heap.
- **Performance:** Appending in a loop is $O(n^2)$ and generates massive garbage for the GC.
- **Use case:** Fixed strings, HashMap keys, multithreaded environments where immutability guarantees safety.

## 2. StringBuilder
- **Immutability:** Mutable character buffer. `append()` modifies the same underlying `char[]` array.
- **Performance:** Amortized $O(1)$ appends. Linear $O(n)$ time complexity for assembling strings in a loop.
- **Thread Safety:** NOT thread-safe.
- **Use case:** General string assembly and concatenation. The go-to choice.

## 3. StringBuffer
- **Immutability:** Mutable character buffer (same as StringBuilder).
- **Thread Safety:** All methods are `synchronized`, making it thread-safe.
- **Performance:** Slower than StringBuilder due to synchronization overhead.
- **Use case:** Almost obsolete. True multithreaded string building is extremely rare (usually you use a local StringBuilder per thread). Mostly a Java 1.0 relic.
