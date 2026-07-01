---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, collections, trees, sorting]
---

# TreeMap and TreeSet

`TreeMap` (and its wrapper `TreeSet`) are sorted collections in Java. 
They store their elements in a **Red-Black Tree** (a self-balancing binary search tree).

## Performance
Because they use a tree structure, every operation (`add`, `remove`, `contains`) runs in **$O(log n)$** time, which is slower than the $O(1)$ average of `HashMap`/`HashSet`.

## Ordering
Elements are iterated in **Sorted Order**.
- By default, they use the elements' *natural ordering* (the elements must implement `Comparable`).
- Alternatively, you can provide a custom `Comparator` via the constructor:
  ```java
  TreeMap<String, Integer> byLength = new TreeMap<>(Comparator.comparingInt(String::length));
  ```

## Navigable Methods
Because the structure is inherently sorted, they implement `NavigableMap`/`NavigableSet`, exposing powerful methods for range queries:
- `firstKey()` / `lastKey()`
- `floorKey(K key)` (largest key $\le$ given key)
- `ceilingKey(K key)` (smallest key $\ge$ given key)
- `subMap(K fromKey, K toKey)` (a view of a specific range)
