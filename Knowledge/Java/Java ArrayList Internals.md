---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, collections, arrays]
---

# Java ArrayList Internals

`ArrayList` is the most commonly used collection in Java. It is a dynamic array backed by a standard `Object[]`.

## Growth Strategy
When you instantiate an `ArrayList()`, it starts with an empty array. On the first `add()`, it allocates an array of capacity 10.
When the array is full, the `ArrayList` resizes by allocating a new array that is **1.5x larger** (`oldCapacity + (oldCapacity >> 1)`) and uses `System.arraycopy()` to copy all existing elements to the new array.

## Time Complexity
- `get(index)`: **O(1)**. Direct pointer arithmetic to the memory address.
- `add(end)`: **Amortized O(1)**. Most adds are O(1); occasionally O(n) during a resize.
- `add(middle)` / `remove(index)`: **O(n)**. Elements must be shifted right or left to make/close space.

## Best Practices
If you know the expected size of your list, use the pre-sizing constructor `new ArrayList<>(100_000)` to avoid costly intermediate resizes.
