---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 6 — Generics and Functional Programming"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, generics, pecs, wildcards]
---

# Java Wildcards and PECS

Wildcards (`?`) are used when you write methods that accept generic collections but want to allow flexibility in the exact type argument.

## The PECS Mnemonic
**P**roducer **E**xtends, **C**onsumer **S**uper.

### 1. `? extends T` (Upper Bounded Wildcard)
- **Use when:** The collection acts as a **Producer** (you are reading from it).
- **Rule:** You can read elements as type `T`, but you **cannot write** to the collection (except `null`).
- Example: `void sum(List<? extends Number> list)`. You can pass `List<Integer>` or `List<Double>`. The method can safely read them as `Number`, but it can't add a `Double` to it because the actual list might be `List<Integer>`.

### 2. `? super T` (Lower Bounded Wildcard)
- **Use when:** The collection acts as a **Consumer** (you are writing to it).
- **Rule:** You can write elements of type `T` to it, but you can only read them back as `Object`.
- Example: `void addNumbers(List<? super Integer> list)`. You can pass `List<Integer>`, `List<Number>`, or `List<Object>`. The method can safely add an `Integer` to all of them.
