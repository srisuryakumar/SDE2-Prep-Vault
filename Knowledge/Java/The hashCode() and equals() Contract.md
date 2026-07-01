---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, collections, hashmap, equality]
---

# The hashCode() and equals() Contract

Violating this contract will severely corrupt `HashMap` and `HashSet` operations, leading to silent bugs where objects exist in the collection but cannot be retrieved.

## The Contract Rules
1. If `a.equals(b)` is true, then `a.hashCode()` **MUST** equal `b.hashCode()`.
2. If `a.hashCode() != b.hashCode()`, then `a.equals(b)` **MUST** be false.
3. If `a.hashCode() == b.hashCode()`, `a.equals(b)` is *not required* to be true (this is a hash collision).

## The Danger
If you override `equals()` without overriding `hashCode()`, two objects with identical data will have different memory addresses (the default `Object.hashCode()` behavior). 
When you try to `map.get(key)`, the `HashMap` will compute the default hash for the key, look in the wrong bucket, and return `null`, even though a conceptually identical key exists in the map!

**Rule:** Always override BOTH `equals()` and `hashCode()` together. IDEs or Records (`record`) can generate these safely.
