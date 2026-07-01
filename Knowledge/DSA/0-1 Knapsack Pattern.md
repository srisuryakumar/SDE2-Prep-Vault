---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, knapsack]
---

# 0/1 Knapsack Pattern

## Intuition
Given $n$ items with weights and values, maximize value within a capacity $W$. Each item can be used **at most once** ("0/1": take it or don't).

- **State:** `dp[i][w]` = max value using first $i$ items with capacity $w$.
- **Recurrence:** `dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight[i]] + value[i])`.

## Space Optimization (1D Rolling Array)
We can compress the $O(n \cdot W)$ 2D table into a 1D array of size $W$.
**CRITICAL REQUIREMENT:** To ensure each item is used at most once, the inner capacity loop MUST run **downward** (from $W$ down to $weight[i]$). If you ran it upward, `dp[s - weight]` might read a value that was already updated *earlier in the same pass*, meaning the item was used twice.

## Template (Partition Equal Subset Sum)
Can you partition an array into two subsets with equal sums?
This is a 0/1 Knapsack where capacity = $Sum / 2$, and weight = value = `nums[i]`. We want to see if we can reach EXACTLY the capacity.

```java
public boolean canPartition(int[] nums) {
    int sum = 0;
    for (int num : nums) sum += num;
    if (sum % 2 != 0) return false;

    int target = sum / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true; // Sum of 0 is always achievable

    for (int num : nums) {
        // Iterate DOWNWARD to prevent item reuse!
        for (int s = target; s >= num; s--) {
            if (dp[s - num]) {
                dp[s] = true;
            }
        }
    }
    return dp[target];
}
```

## Variations
- **Target Sum:** Count ways to assign `+` or `-` to numbers to hit a target. Reduces to finding a subset sum equal to `P = (totalSum + target) / 2`. Accumulate counts instead of booleans: `dp[s] += dp[s - num]`.
- **Unbounded Knapsack (Coin Change):** When an item can be reused infinitely, the inner loop MUST run **upward** (from $0$ to $W$) to allow previous updates from the same item to propagate.
