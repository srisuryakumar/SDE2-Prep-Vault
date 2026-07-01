---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, binary-search, answer-search]
---

# Binary Search on the Answer

This advanced pattern expands binary search beyond finding a value in an array, to finding the optimal value of a parameter.

## When to use it
1. You are asked to find the **minimum/maximum value** of some parameter (e.g., eating speed, shipping capacity).
2. The parameter is **monotonic**: if speed `k` works, then `k+1` also works. If speed `k` fails, `k-1` also fails.
3. The parameter's range is bounded (e.g., $1$ to $\max(\text{piles})$).
4. You can write a `canFinish(k)` function to check feasibility in polynomial time (usually $O(n)$).

## Template (e.g., Koko Eating Bananas)
```java
public int minSpeed(int[] piles, int h) {
    int lo = 1, hi = maxOf(piles);
    int result = hi;
    
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (canFinish(piles, mid, h)) {
            result = mid;      // Valid! Record it and try to find a slower speed
            hi = mid - 1;      // Search left
        } else {
            lo = mid + 1;      // Too slow! Must search right
        }
    }
    return result;
}

private boolean canFinish(int[] piles, int k, int h) {
    int hours = 0;
    for (int pile : piles) {
        hours += (pile + k - 1) / k; // Ceiling division!
    }
    return hours <= h;
}
```

## Ceiling Division
In Java, integer division truncates down (floor). To get the ceiling of $a / b$, use `(a + b - 1) / b`. This avoids floating point edge cases from `Math.ceil()`.
