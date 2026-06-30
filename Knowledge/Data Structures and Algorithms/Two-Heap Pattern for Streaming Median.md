---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 7 — Heaps and Priority Queues"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, heaps, two-heaps]
---

# Two-Heap Pattern for Streaming Median

## Intuition
Maintaining a running median as numbers arrive one at a time needs more than a single heap. A single heap gives fast access to an *extreme* (min or max), but the median sits in the *middle*.

**The Solution:** Split the data into two halves using two heaps.
- **Lower Half:** A **Max-Heap**. The largest element (closest to the median) sits at the root.
- **Upper Half:** A **Min-Heap**. The smallest element (the other boundary) sits at the root.

Keep the two heaps balanced in size (never differing by more than 1).

## Implementation
```java
class MedianFinder {
    private PriorityQueue<Integer> lowerHalf = new PriorityQueue<>(Collections.reverseOrder());
    private PriorityQueue<Integer> upperHalf = new PriorityQueue<>();

    public void addNum(int num) {
        // 1. Insert into correct half
        if (lowerHalf.isEmpty() || num <= lowerHalf.peek()) {
            lowerHalf.offer(num);
        } else {
            upperHalf.offer(num);
        }

        // 2. Rebalance (sizes must not differ by > 1)
        if (lowerHalf.size() > upperHalf.size() + 1) {
            upperHalf.offer(lowerHalf.poll());
        } else if (upperHalf.size() > lowerHalf.size() + 1) {
            lowerHalf.offer(upperHalf.poll());
        }
    }

    public double findMedian() {
        if (lowerHalf.size() == upperHalf.size()) {
            return (lowerHalf.peek() + upperHalf.peek()) / 2.0;
        }
        return lowerHalf.size() > upperHalf.size() ? lowerHalf.peek() : upperHalf.peek();
    }
}
```
**Complexity:** $O(\log n)$ for `addNum`, $O(1)$ for `findMedian`. Space $O(n)$.
