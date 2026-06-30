---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 12 — Advanced Patterns"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [dsa, pattern, fenwick-tree, bit, range-queries, hard]
---

# Fenwick Tree Pattern (Binary Indexed Tree)

## Intuition
Solves the exact same problem as a Segment Tree—**prefix sum with point updates**—but with simpler code and better practical performance. 
The tradeoff is that it only works for operations with an inverse (like sum, whose inverse is subtraction). It cannot do range minimum/maximum queries easily.

**The Key Insight:** Index `i` in the array stores the sum of a specific range of elements, determined by its **lowest set bit**. 
We can isolate the lowest set bit using `i & (-i)`.
Note: The Fenwick Tree is always **1-indexed**.

## Template
```java
class FenwickTree {
    private int[] tree;
    private int n;

    FenwickTree(int n) {
        this.n = n;
        tree = new int[n + 1]; // 1-indexed
    }

    // Add delta to position i (1-indexed)
    public void update(int i, int delta) {
        for (; i <= n; i += i & (-i)) { // Jump to next range that covers this one
            tree[i] += delta;
        }
    }

    // Query prefix sum [1..i]
    public int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & (-i)) { // Jump back to previous covering range
            sum += tree[i];
        }
        return sum;
    }

    // Query range sum [l..r]
    public int queryRange(int l, int r) {
        return query(r) - query(l - 1);
    }
}
```

**Common Mistake:** Forgetting the 1-indexed convention. `0 & (-0)` is 0, which breaks the `update` loop (infinite loop). Always shift array indices to 1-indexing when passing them into `update` or `query`.
