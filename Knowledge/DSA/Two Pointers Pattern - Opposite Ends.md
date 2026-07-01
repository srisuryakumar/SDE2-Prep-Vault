---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, two-pointers]
---

# Two Pointers Pattern - Opposite Ends

## Intuition
When searching for a pair (or triple) in a **sorted array** that satisfies a condition, a brute force check takes $O(n^2)$. 
The two-pointer approach exploits the sorted order to logically eliminate entire columns of pairs in a single step, bringing the complexity down to $O(n)$.

**The core invariant:** `left` points to the smallest remaining candidate; `right` points to the largest. When they meet, every pair has been considered (either tested or logically eliminated).

## Template
```java
public static void twoPointersOppEnds(int[] sorted) {
    int left = 0, right = sorted.length - 1;
    while (left < right) {
        // Compute something involving sorted[left] and sorted[right]
        int value = sorted[left] + sorted[right]; // example: sum

        if (value == TARGET) {
            // found! record result, advance both (or just one based on problem)
            left++;
            right--;
        } else if (value < TARGET) {
            left++;   // sum too small → need a bigger left element
        } else {
            right--;  // sum too big  → need a smaller right element
        }
    }
}
```

## Classic Problems
- **Two Sum II (Sorted):** If sum < target, advance left. If sum > target, advance right.
- **Container With Most Water:** Volume depends on width and the *shorter* line. Moving the taller line inward reduces width and cannot improve height. Always advance the pointer pointing to the shorter line.
- **3Sum:** Sort first. Fix one element `nums[i]`, then run Two Sum II on the remaining subarray to its right for a target of `-nums[i]`. Total time $O(n^2)$. Skip duplicate values to avoid duplicate triplets.
