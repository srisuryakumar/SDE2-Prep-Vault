---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 1 — Algorithmic Thinking and Complexity Analysis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, complexity, hierarchy]
---

# The Complexity Hierarchy

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
```

## Concrete Examples
- **$O(1)$**: Array index access, HashMap get/put (average case).
- **$O(\log n)$**: Binary search, balanced BST search.
- **$O(n)$**: Linear scan, single pass with a HashMap.
- **$O(n \log n)$**: Merge sort, heap sort, "sort then scan".
- **$O(n^2)$**: Bubble sort, nested pair comparison.
- **$O(2^n)$**: Generating every subset, naive recursive Fibonacci.
- **$O(n!)$**: Generating every permutation.

## The Reality Check
- $O(n^2)$ is fine up to $n = 10,000$, but **dead** by $n = 1,000,000$ (takes hours).
- $O(2^n)$ is **dead** by $n \approx 30$, regardless of hardware.

If you are asked to handle $10^5$ elements, an $O(n^2)$ approach will time out. You must look for an $O(n \log n)$ or $O(n)$ solution.
