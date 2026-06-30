---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, linear-dp]
---

# Linear DP Pattern

Many 1D DP problems are structurally identical, relying only on the last 1 or 2 computed states. They can be space-optimized to $O(1)$ by keeping track of only `prev1` and `prev2`.

## 1. Climbing Stairs
Climb 1 or 2 steps at a time.
- **State:** `dp[i]` = ways to reach step $i$.
- **Recurrence:** `dp[i] = dp[i-1] + dp[i-2]`. (Identical to Fibonacci).
- **Space-optimized:** 
  ```java
  int prev2 = 1, prev1 = 1;
  for (int i = 2; i <= n; i++) {
      int curr = prev1 + prev2;
      prev2 = prev1; prev1 = curr;
  }
  ```

## 2. House Robber
Can't rob two adjacent houses. Maximize money.
- **State:** `dp[i]` = max money robbable considering houses $0..i$.
- **Recurrence:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. (Either skip current, or rob current + best from two houses back).
- **Space-optimized:**
  ```java
  int prev2 = nums[0], prev1 = Math.max(nums[0], nums[1]);
  for (int i = 2; i < nums.length; i++) {
      int curr = Math.max(prev1, prev2 + nums[i]);
      prev2 = prev1; prev1 = curr;
  }
  ```

## 3. House Robber II
Houses form a circle (house 0 and $n-1$ are adjacent).
- **Insight:** You can never rob *both* house 0 and house $n-1$.
- **Solution:** Run the linear House Robber algorithm twice: once over `[0, n-2]` (excluding last) and once over `[1, n-1]` (excluding first). Return the max of the two runs.
