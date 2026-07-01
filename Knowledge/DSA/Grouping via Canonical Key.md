---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 5 — Hash Maps and Hash Sets"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, hash-map, canonical-key]
---

# Grouping via Canonical Key

## Intuition
When grouping items by equivalence (like anagrams), we need a **canonical key**: a uniform representation where every equivalent item maps to the exact same key, and nothing else does. Use this canonical key as the HashMap key, and every item falls into the correct bucket in one pass.

## Problem: Group Anagrams
Two strings are anagrams exactly when sorting their characters produces the identical string. The sorted string is the canonical key.

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);   // Canonical form
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```
**Complexity:** $O(n \cdot m \log m)$, where $n$ is strings and $m$ is max length.

## Optimization: Frequency Signature
If asked to avoid sorting, use a frequency signature (e.g., an array of 26 ints converted to a string like `"3#0#1#..._"`). This brings the cost down to $O(n \cdot m)$.

**Common Mistake:** Never use a raw `char[]` or `int[]` as a HashMap key in Java. Arrays use identity comparison by default, not value comparison. Always convert to a `String` (or another type that overrides `equals`/`hashCode`).
