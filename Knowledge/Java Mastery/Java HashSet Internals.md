---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, collections, hashset]
---

# Java HashSet Internals

`HashSet` is a Set implementation that uses a hash table for storage. 
Under the hood, **`HashSet` is literally backed by a `HashMap`**.

## How it works
When you create a `HashSet<E>`, it creates an internal `HashMap<E, Object>`.
```java
private transient HashMap<E,Object> map;
private static final Object PRESENT = new Object(); // dummy value
```

When you add an element to the `HashSet`, it calls `put()` on the internal `HashMap`. The element becomes the **key**, and a dummy object (`PRESENT`) becomes the **value**.
```java
public boolean add(E e) {
    return map.put(e, PRESENT) == null;
}
```

## Guarantees
Because it uses `HashMap` keys, it guarantees:
- **No duplicates:** `HashMap` keys are unique.
- **O(1) amortized performance:** For `add`, `remove`, and `contains`.
- **No ordering:** The elements are scattered based on their hash codes.

Just like `HashMap`, you **must** correctly override `equals()` and `hashCode()` for elements stored in a `HashSet`.
