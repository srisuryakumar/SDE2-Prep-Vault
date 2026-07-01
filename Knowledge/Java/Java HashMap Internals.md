---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["[[HashMap and Frequency Counting]]", ]
tags: [java, collections, hashmap]
---

# Java HashMap Internals

`HashMap` is arguably the most important data structure in Java. It powers `HashSet`, `LinkedHashMap`, and `ConcurrentHashMap`.

## The Internal Structure
It is backed by an array (table) of "buckets." Each bucket is a linked list (or a tree in Java 8+).
1. **Hash Spreading:** `key.hashCode()` is XORed with its own upper 16 bits (`hash ^ (hash >>> 16)`) to ensure good distribution, even for small arrays where only lower bits are used.
2. **Bucket Index:** Calculated via `hash & (capacity - 1)`. This is a fast bitwise modulo operation, which requires the capacity to always be a power of 2.

## Insertion (`put`)
1. Compute the hash and bucket index.
2. If the bucket is empty, place the node.
3. If a collision occurs (bucket occupied), walk the linked list. If `key.equals(existingKey)`, update the value. If not found, append/prepend the new node.

## Java 8 Treeification
To prevent Denial of Service (DoS) attacks via engineered hash collisions, Java 8 introduced Treeification. 
If a bucket's linked list grows to **8 or more nodes**, the list is automatically converted into a **Red-Black Tree**, improving worst-case lookup from $O(n)$ to $O(log n)$.

## Resizing
When the number of entries exceeds the **load factor threshold** (default `0.75 * capacity`), the HashMap resizes:
- The capacity is doubled (e.g., 16 → 32).
- Every single entry is re-hashed and moved to its new bucket.
- This is an $O(n)$ operation, but it happens infrequently, leading to amortized $O(1)$ insertions.

## Related Concepts
- See also [[HashMap and Frequency Counting]] for the algorithmic applications of frequency counting.
