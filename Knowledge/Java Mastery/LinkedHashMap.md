---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, collections, hashmap, cache]
---

# LinkedHashMap

`LinkedHashMap` extends `HashMap` to add predictability to iteration order.

## How it works
It maintains a **doubly-linked list** running through all its entries. This structure requires slightly more memory per entry than a standard `HashMap`.

## Ordering Modes
1. **Insertion Order (Default):** Iterating through the map will return entries in the exact order they were inserted. A standard `HashMap` returns entries in an unpredictable, seemingly random order based on bucket locations.
2. **Access Order (LRU Cache):** If instantiated with `new LinkedHashMap<>(16, 0.75f, true)`, the map updates the linked list whenever an element is accessed (`get` or `put`). The most recently accessed element is moved to the end of the list.

## Implementing an LRU Cache
You can implement an LRU (Least Recently Used) cache trivially by overriding `removeEldestEntry()`:
```java
Map<Integer, String> lruCache = new LinkedHashMap<>(16, 0.75f, true) {
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, String> eldest) {
        return size() > 100;  // Evict oldest when size exceeds 100
    }
};
```
