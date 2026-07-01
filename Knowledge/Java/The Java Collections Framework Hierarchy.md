---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, collections, structures]
---

# The Java Collections Framework Hierarchy

Unlike JavaScript, where `Array` and `Map` cover most use cases, Java has a rich type-safe hierarchy of collections.

## The Core Interfaces
- **`Iterable<T>`**: The root interface. Anything Iterable can be used in a `for-each` loop.
- **`Collection<T>`**: Extends Iterable. Adds methods like `add()`, `remove()`, `size()`.

### Sub-Interfaces of Collection
1. **`List<T>`**: Ordered, allows duplicates, accessed by index.
   - `ArrayList` (Dynamic array, O(1) access)
   - `LinkedList` (Doubly-linked list, rarely the best choice)
2. **`Set<T>`**: Unordered, no duplicates.
   - `HashSet` (Backed by HashMap, O(1) average access)
   - `LinkedHashSet` (Maintains insertion order)
   - `TreeSet` (Sorted set, O(log n) access via Red-Black Tree)
3. **`Queue<T>` / `Deque<T>`**: Processing elements in order (FIFO/LIFO).
   - `PriorityQueue` (Min-heap)
   - `ArrayDeque` (Fast double-ended queue, use for Stacks and Queues)

### The Map Interface
**`Map<K, V>`** does NOT extend `Collection` because it holds key-value pairs, not single elements.
- `HashMap` (Unordered, O(1) average lookup)
- `LinkedHashMap` (Maintains insertion/access order)
- `TreeMap` (Sorted keys, O(log n) lookup)
