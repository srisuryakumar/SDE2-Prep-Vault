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

# Two Pointers Pattern - Same Direction

## Intuition
Two pointers don't have to start from opposite ends. A powerful configuration uses both pointers starting at the left:
- **Fast Pointer:** Explores ahead, seeing every element.
- **Slow Pointer:** Marks where the next valid element should go.

This is equivalent to an **in-place partition**. Everything at or below `slow-1` is "cleaned". Everything ahead of `slow` but behind `fast` has been scanned and discarded.

**Pattern Recognition:** Reach for this when asked to partition an array in-place, remove/filter elements while preserving order, or overwrite an array with a "cleaned" version without using extra memory.

## Template
```java
public static int twoPointersSameDirection(int[] arr) {
    int slow = 0;
    for (int fast = 0; fast < arr.length; fast++) {
        if (isValid(arr[fast])) {      // condition depends on the problem
            arr[slow] = arr[fast];     // write valid element to slow position
            slow++;                    // advance slow
        }
        // invalid elements: fast advances but slow does not
    }
    return slow;   // slow is the length of the valid portion
}
```

## Classic Problems
- **Remove Duplicates from Sorted Array:** `isValid` means `arr[fast] != arr[slow]`.
- **Move Zeroes:** `isValid` means `arr[fast] != 0`. Do a second pass to fill from `slow` to the end with 0s.
- **Sort Colors (Dutch National Flag):** Uses 3 pointers (`lo`, `mid`, `hi`) to partition into 0s, 1s, and 2s in a single pass.
