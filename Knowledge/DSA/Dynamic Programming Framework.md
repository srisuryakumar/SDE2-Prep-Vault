---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, fundamentals]
---

# Dynamic Programming Framework

## Why DP Exists
Brute-force recursive solutions often solve the *identical* subproblem over and over, leading to exponential $O(2^n)$ time complexity.
DP's insight: if you've already computed the answer to a subproblem, **cache it** and look it up instead of recomputing. This collapses exponential time down to the number of *distinct* subproblems.

## DP vs. Recursion
- **Top-down (memoization):** Write natural recursive solution, but check a cache (`HashMap` or array) first before recursing, and store the result before returning.
- **Bottom-up (tabulation):** Build the answer iteratively from the smallest subproblems up, filling a table. Avoids recursion overhead and makes space optimization easier to see.

## The Five-Step DP Framework
1. **Define the state:** What does `dp[i]` (or `dp[i][j]`) actually represent? (e.g., "Max profit achievable using only the first $i$ days").
2. **Write the recurrence:** How does `dp[i]` relate to smaller/earlier values? This answers "what choices exist at this step, and which is best?"
3. **Identify base cases:** The smallest subproblems with known, trivial answers (e.g. `dp[0]=0`).
4. **Choose top-down or bottom-up:** Bottom-up is usually preferred for easier space optimization.
5. **Optimize space, if possible:** If `dp[i]` only depends on a constant number of previous entries (e.g. just `dp[i-1]` and `dp[i-2]`), collapse the $O(n)$ array into $O(1)$ variables.
