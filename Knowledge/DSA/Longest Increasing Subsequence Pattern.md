---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, lis, binary-search, hard]
---

# Longest Increasing Subsequence Pattern

## Intuition
Find the length of the longest *strictly increasing* subsequence of an integer array.

## The $O(n^2)$ DP Approach
- **State:** `dp[i]` = length of the longest increasing subsequence *ending exactly at* index `i`.
- **Recurrence:** `dp[i] = 1 + max(dp[j])` over every `j < i` where `nums[j] < nums[i]`.
- **Base case:** `dp[i] = 1` initially.

```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    int maxLen = 1;

    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }
    return maxLen;
}
```

## The $O(n \log n)$ Refinement — Patience Sort
Maintain an array `tails`, where `tails[k]` is the *smallest possible* tail value among all increasing subsequences of length `k+1` found so far.
Keeping each tail as small as possible maximizes the chance that *future* numbers can extend that subsequence further.

Since `tails` is strictly increasing by definition, we can use **binary search** to find where the current number belongs.
1. If the number is larger than every current tail, it extends the longest sequence. Add it to `tails`.
2. Otherwise, find the *first* tail that is $\ge$ the number, and replace it. This improves the potential for future numbers to extend this length.

```java
public int lengthOfLIS(int[] nums) {
    List<Integer> tails = new ArrayList<>();
    for (int num : nums) {
        int pos = Collections.binarySearch(tails, num);
        if (pos < 0) {
            pos = -(pos + 1); // binarySearch's convention for "insertion point"
        }
        if (pos == tails.size()) {
            tails.add(num);      // Extend LIS
        } else {
            tails.set(pos, num); // Improve existing tail
        }
    }
    return tails.size();
}
```
**Caveat:** The `tails` array does *not* necessarily represent a valid subsequence from the input array. Only its *length* is guaranteed to be correct.
