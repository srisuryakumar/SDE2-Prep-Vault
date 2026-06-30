---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, grid-dp]
---

# Grid DP Pattern

## Intuition
Grid DP problems typically involve navigating an $m \times n$ grid from the top-left to the bottom-right, restricted to moving only Right or Down.

- **State:** `dp[i][j]` represents the answer (ways, min sum, etc.) to reach cell `(i, j)`.
- **Recurrence:** `dp[i][j]` depends entirely on the cell above it `dp[i-1][j]` and the cell to its left `dp[i][j-1]`.
- **Base cases:** Row $0$ and Column $0$ are initialized based on a straight-line traversal (since there is only one way to move along the edges).

## Template (Unique Paths)
Count distinct paths from top-left to bottom-right.
```java
public int uniquePaths(int m, int n) {
    int[][] dp = new int[m][n];
    for (int i = 0; i < m; i++) dp[i][0] = 1;
    for (int j = 0; j < n; j++) dp[0][j] = 1;

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]; // Arrived from above or left
        }
    }
    return dp[m - 1][n - 1];
}
```

## Variations
- **Minimum Path Sum:** Minimize the sum of grid values along the path.
  `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`
- **Unique Paths with Obstacles:** If a cell has an obstacle, set its `dp[i][j] = 0`. **CRITICAL:** If an obstacle is on the border (row 0 or col 0), *all* subsequent cells in that border also become unreachable (`0`).

## Space Optimization
Since `dp[i][j]` only ever depends on the current row (cells to the left) and the row immediately above it, you can collapse the $O(m \cdot n)$ 2D array into a single 1D array of size $n$, updated left to right in place. This drops space to $O(n)$.
