---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, binary-search]
---

# Binary Search Pattern

Binary search halves the search space at each step, running in $O(\log n)$.

**CRITICAL RULE:** Always use `int mid = lo + (hi - lo) / 2;` to avoid integer overflow, never `(lo + hi) / 2`.

## Variant 1: Standard Search
Find target in a sorted array, return index or -1.
```java
public int binarySearch(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

## Variant 2: Find First Occurrence (Left-Biased)
When `nums[mid] == target`, record the result but keep searching **left** (`hi = mid - 1`).
```java
public int findFirst(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1, result = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) {
            result = mid; hi = mid - 1; // Keep searching left
        }
        else if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return result;
}
```

## Variant 3: Find Last Occurrence (Right-Biased)
When `nums[mid] == target`, record the result but keep searching **right** (`lo = mid + 1`).

## Variant 4: Search in Rotated Sorted Array
A sorted array rotated at an unknown pivot (e.g., `[4,5,6,7,0,1,2]`).
**Key insight:** Splitting at `mid` always produces at least one perfectly sorted half. Check which half is sorted, then check if the target is in that range.
```java
public int searchRotated(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;

        if (nums[lo] <= nums[mid]) { // Left half is sorted
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else { // Right half is sorted
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}
```
