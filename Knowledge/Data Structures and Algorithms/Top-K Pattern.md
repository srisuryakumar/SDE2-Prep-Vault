---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 7 — Heaps and Priority Queues"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, heaps, top-k]
---

# Top-K Pattern

## Intuition
Finding the $k$ largest elements doesn't require sorting everything ($O(n \log n)$). You only need to track the best $k$ candidates seen so far.
Maintain a **heap of size $k$**. While the heap has fewer than $k$ elements, add. Once it reaches size $k$, compare each new element against the heap's root (the *weakest* of your current top-$k$). If it beats it, evict the root and insert the new one.

- **To find the $k$ largest:** Use a **Min-Heap**. The smallest of the current top candidates sits at the root, ready to be evicted if a larger element appears.
- **To find the $k$ smallest:** Use a **Max-Heap**. The largest of the current bottom candidates sits at the root.

## Template (Kth Largest Element)
```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) {
            minHeap.poll(); // Evict the current weakest (smallest)
        }
    }
    return minHeap.peek(); // The k-th largest is the root!
}
```
**Complexity:** Time $O(n \log k)$. Space $O(k)$.

## Common Variations
- **K Closest Points to Origin:** Find the $k$ *smallest* distances $\rightarrow$ Use a **Max-Heap** (farthest of the closest candidates at the root). Compare squared Euclidean distances ($x^2 + y^2$) to avoid floating point math.
- **Top K Frequent Elements:** If frequencies are bounded, bucket sort is $O(n)$. If unbounded or generic, this pattern handles it in $O(n \log k)$ by using frequency as the comparator.
