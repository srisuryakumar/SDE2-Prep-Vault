---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 12 — Advanced Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, binary-search, advanced]
---

# Binary Search on Answer Pattern

## Intuition
Normally we use Binary Search to find an element in a sorted array. However, it can also be used to find an optimal "answer" parameter if there is a **monotonic feasibility function**.

If a problem asks for the minimum or maximum value of some parameter (e.g., minimum ship capacity, minimum eating speed), and a `canDo(value)` check is monotonic (false below a threshold, true above it, or vice versa), you can binary search the answer range.

## Template (Capacity to Ship Packages)
Find minimum ship capacity to ship all weights in `D` days.
1. Determine `lo` and `hi`. `lo` is the max single weight (must be able to carry the heaviest package). `hi` is the sum of all weights (can carry everything in 1 day).
2. Binary search between `lo` and `hi`.
3. If `canShip(mid)` is true, try to find a tighter (smaller) capacity: `hi = mid - 1`. If false, `lo = mid + 1`.

```java
public int shipWithinDays(int[] weights, int days) {
    int lo = 0, hi = 0;
    for (int w : weights) { 
        lo = Math.max(lo, w); 
        hi += w; 
    }

    int result = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (canShip(weights, mid, days)) {
            result = mid; // Found a valid answer, try for a smaller one
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }
    return result;
}

private boolean canShip(int[] weights, int capacity, int days) {
    int daysNeeded = 1, currentLoad = 0;
    for (int w : weights) {
        if (currentLoad + w > capacity) {
            daysNeeded++;
            currentLoad = 0;
        }
        currentLoad += w;
    }
    return daysNeeded <= days;
}
```
