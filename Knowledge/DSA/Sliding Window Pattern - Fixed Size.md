---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["[[Rate Limiting Algorithms]]", ]
tags: [dsa, pattern, sliding-window]
---

# Sliding Window Pattern - Fixed Size

## Intuition
When computing something over every contiguous subarray of a fixed size $k$, a brute force approach takes $O(nk)$. The sliding window insight is that **consecutive windows share most of their elements**. 

The window `arr[i..i+k-1]` and the window `arr[i+1..i+k]` differ in exactly two elements: 
- The one that slid out on the left (`arr[i]`)
- The one that slid in on the right (`arr[i+k]`)

If your aggregation (sum, count, hash) supports $O(1)$ removal and addition, updating the window is $O(1)$ rather than $O(k)$, bringing total complexity down to $O(n)$.

**Pattern Recognition:** The giveaway is "subarray (or substring) of exactly size $k$." Fixed window = fixed $k$ in the problem statement.

## Template
```java
public static int slidingWindowFixed(int[] arr, int k) {
    // Build initial window
    int windowSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];

    int result = windowSum;  // or whatever you're tracking

    // Slide the window
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i];       // add the new right element
        windowSum -= arr[i - k];   // remove the element that fell off the left
        result = Math.max(result, windowSum);  // or min, or however you aggregate
    }
    return result;
}
```

## Classic Problems
- **Maximum Sum Subarray of Size K:** Direct template application.
- **Average of Subarrays of Size K:** Same as maximum sum, just divide the result by $k$.

## Related Concepts
- See also [[Rate Limiting Algorithms]] for the rate limiter implementation behind token bucket.
