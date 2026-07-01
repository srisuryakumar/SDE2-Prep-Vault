---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, knapsack, unbounded-knapsack]
---

# Unbounded Knapsack Pattern (Coin Change)

## Intuition
Given coin denominations and a target amount, find the *minimum* number of coins to make that amount.

This is the **Unbounded Knapsack** problem: each item (coin) can be used an *unlimited number of times*. This single difference means the space-optimized 1D inner loop must iterate **UPWARD** (from the coin value to the capacity).

- **State:** `dp[a]` = min coins needed to make amount `a`.
- **Recurrence:** `dp[a] = min(dp[a], dp[a - coin] + 1)`.
- **Base case:** `dp[0] = 0`; all other amounts are initialized to `Integer.MAX_VALUE`.

## Template
```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;

    for (int coin : coins) {
        // UPWARD iteration - Unbounded reuse is intentional!
        for (int a = coin; a <= amount; a++) { 
            if (dp[a - coin] != Integer.MAX_VALUE) {
                dp[a] = Math.min(dp[a], dp[a - coin] + 1);
            }
        }
    }
    return dp[amount] == Integer.MAX_VALUE ? -1 : dp[amount];
}
```

## The Crucial Difference: 0/1 Knapsack vs. Unbounded Knapsack
In **0/1 Knapsack** (e.g. Partition Equal Subset Sum), iterating upward would incorrectly allow the same item to be used twice, because `dp[a - item]` might have already been updated *by this same item* earlier in the inner loop pass. Thus, 0/1 Knapsack iterates **DOWNWARD** (from $W$ to $weight[i]$).

In **Unbounded Knapsack** (Coin Change), we *want* the possibility of using the same item multiple times. Iterating **UPWARD** allows `dp[a - coin]` to carry the effect of using this coin previously. Getting this loop direction backward silently breaks the algorithm (it either incorrectly forbids legal reuse, or incorrectly allows illegal reuse).
