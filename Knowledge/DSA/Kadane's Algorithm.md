---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, kadane, dp]
---

# Kadane's Algorithm

## Intuition
Used to find the contiguous subarray with the **largest sum** in $O(n)$ time.
At each index $i$, you ask one question: *"Is it worth continuing the current subarray, or better to start fresh here?"*

The maximum subarray ending exactly at $i$ is the maximum of:
1. `nums[i]` alone (starting fresh, meaning the previous prefix was negative and dragging us down).
2. `maxEndingHere + nums[i]` (extending the previous best).

The global maximum is the highest `maxEndingHere` seen across all positions.

## Template
```java
public int maxSubArray(int[] nums) {
    int maxEndingHere = nums[0];
    int maxSoFar = nums[0];   // Do NOT initialize to 0!
    for (int i = 1; i < nums.length; i++) {
        maxEndingHere = Math.max(nums[i], maxEndingHere + nums[i]);
        maxSoFar = Math.max(maxSoFar, maxEndingHere);
    }
    return maxSoFar;
}
```

## Common Mistakes
- **Initializing `maxSoFar = 0`:** This is wrong when all elements in the array are negative. Initialize both to `nums[0]`.

## Pattern Recognition
- "Maximum subarray sum"
- "Maximum product subarray" (Track both min and max because multiplying by a negative flips them).
