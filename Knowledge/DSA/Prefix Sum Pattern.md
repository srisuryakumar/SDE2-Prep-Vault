---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, prefix-sum]
---

# Prefix Sum Pattern

## Intuition
When asked for the sum of elements from index $i$ to $j$, a naive scan takes $O(j-i+1)$ time. 
The prefix sum insight is to **precompute** the cumulative sum at every index once in $O(n)$, then answer any range query in $O(1)$ with a subtraction.

Define `prefix[i]` = sum of `arr[0..i-1]`.
Then: `sum(i, j) = prefix[j+1] - prefix[i]`

## Template
```java
// Build prefix sum array (size n+1 to avoid off-by-one handling)
public int[] buildPrefix(int[] arr) {
    int[] prefix = new int[arr.length + 1];
    for (int i = 0; i < arr.length; i++) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
    return prefix;
}
// sum of arr[i..j] inclusive = prefix[j + 1] - prefix[i]
```

## Classic Problems
- **Range Sum Query:** Direct application of the template.
- **Subarray Sum Equals K (with negatives):** If `sum(i,j) = k`, then `prefix[j+1] - prefix[i] = k`, which means `prefix[i] = prefix[j+1] - k`. Keep a HashMap of prefix sums seen so far. For each new prefix sum `curr`, check how many times `curr - k` has been seen. **CRITICAL:** Initialize the map with `{0: 1}` to account for subarrays starting at index 0.
- **Product of Array Except Self:** Compute left products in one pass, then maintain a running right product and multiply it in a reverse pass.
