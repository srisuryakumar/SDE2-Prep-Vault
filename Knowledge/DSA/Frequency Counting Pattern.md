---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 5 — Hash Maps and Hash Sets"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, hash-map, frequency-counting]
---

# Frequency Counting Pattern

## Intuition
Many problems reduce to "how many times does each distinct value appear?" Build a frequency map once in $O(n)$, and subsequent questions become $O(1)$ or $O(k)$ lookups.

## Java Template
```java
Map<Character, Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) {
    freq.merge(c, 1, Integer::sum);   // insert 1 if absent, else add 1 to existing
}
```

## Classic Problems
- **Valid Anagram:** Build frequency map for $s$. Walk $t$, decrementing counts. If any count goes negative, or lengths differ, return false. (Checking lengths up front is critical).
- **Top K Frequent Elements:** Build frequency map ($O(n)$). Because frequency is bounded between $1$ and $n$, use **bucket sort by frequency**: an array of lists indexed by frequency. Drop values into buckets, then scan buckets from highest frequency down to collect $k$ elements. This is $O(n)$ flat, beating the generic $O(n \log k)$ heap approach.
