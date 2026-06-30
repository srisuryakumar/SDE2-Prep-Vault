# Chapter 10: Dynamic Programming
## Part 2 — Grid DP · 0/1 Knapsack Family

## Pattern 2 — Grid DP (2D)

### Problem — Unique Paths (LeetCode 62)

**Statement.** A robot starts at the top-left of an m×n grid, moving only right or down. Count the distinct paths to the bottom-right.

- **State:** `dp[i][j]` = number of distinct paths to reach cell (i, j).
- **Recurrence:** `dp[i][j] = dp[i-1][j] + dp[i][j-1]` — arrived either from above or from the left.
- **Base case:** row 0 and column 0 are all `1` — there's exactly one way to reach any cell in the first row (keep moving right) or first column (keep moving down).

```java
public int uniquePaths(int m, int n) {
    int[][] dp = new int[m][n];
    for (int i = 0; i < m; i++) dp[i][0] = 1;
    for (int j = 0; j < n; j++) dp[0][j] = 1;

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }
    return dp[m - 1][n - 1];
}
```

**Trace** on `m=3, n=3`:

```
Base cases:        Filled in:
[1,1,1]             [1,1,1]
[1,_,_]    →         [1,2,3]
[1,_,_]              [1,3,6]

dp[1][1]=dp[0][1]+dp[1][0]=1+1=2
dp[1][2]=dp[0][2]+dp[1][1]=1+2=3
dp[2][1]=dp[1][1]+dp[2][0]=2+1=3
dp[2][2]=dp[1][2]+dp[2][1]=3+3=6

Final answer: 6   ✓   (matches the combinatorial formula C(m+n-2, m-1) = C(4,2) = 6)
```

**Complexity:** O(m·n) time, O(m·n) space — but **space-optimizable to O(n)**: since `dp[i][j]` only ever depends on the row above and the current row, a single 1D array of size n, updated left to right in place, is all that's actually needed.

---

### Problem — Minimum Path Sum (LeetCode 64)

**Statement.** Given a grid of non-negative numbers, find a top-left-to-bottom-right path (right/down moves only) minimizing the sum along the way.

- **State:** `dp[i][j]` = minimum path sum to reach cell (i, j).
- **Recurrence:** `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`.
- **Base case:** `dp[0][0]=grid[0][0]`; first row and column each have only one possible path (straight across, or straight down), so they accumulate directly.

```java
public int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[][] dp = new int[m][n];
    dp[0][0] = grid[0][0];
    for (int j = 1; j < n; j++) dp[0][j] = dp[0][j - 1] + grid[0][j];
    for (int i = 1; i < m; i++) dp[i][0] = dp[i - 1][0] + grid[i][0];

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = grid[i][j] + Math.min(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    return dp[m - 1][n - 1];
}
```

**Trace** on `grid=[[1,3,1],[1,5,1],[4,2,1]]`:

```
dp[0]=[1,4,5]   (1, 1+3, 4+1)
dp[1][0]=1+1=2
dp[2][0]=2+4=6

dp[1][1]=5+min(4,2)=5+2=7
dp[1][2]=1+min(5,7)=1+5=6
dp[2][1]=2+min(7,6)=2+6=8
dp[2][2]=1+min(6,8)=1+6=7

Final grid:
[1,4,5]
[2,7,6]
[6,8,7]

Answer: 7   ✓   (path 1→3→1→1→1, i.e. right, right, down, down: 1+3+1+1+1=7)
```

**Complexity:** O(m·n) time, O(m·n) space (also collapsible to O(n), same reasoning as Unique Paths).

---

### Problem — Unique Paths with Obstacles (LeetCode 63)

**Statement.** Same as Unique Paths, but some cells are obstacles (marked `1`) that block movement entirely.

**The twist on the recurrence:** if `grid[i][j]` is an obstacle, `dp[i][j] = 0` outright — no path can pass through it, regardless of what `dp[i-1][j] + dp[i][j-1]` would otherwise compute.

**The twist on the base case — easy to miss:** if an obstacle appears *anywhere* in row 0 or column 0, every cell from that point onward in that row/column becomes unreachable (`0`), not just the obstacle cell itself — the only way to reach a later cell in row 0 is by passing straight through every earlier cell in row 0, and an obstacle blocks that entirely.

```java
public int uniquePathsWithObstacles(int[][] obstacleGrid) {
    int m = obstacleGrid.length, n = obstacleGrid[0].length;
    int[][] dp = new int[m][n];

    dp[0][0] = (obstacleGrid[0][0] == 1) ? 0 : 1;
    for (int j = 1; j < n; j++) {
        dp[0][j] = (obstacleGrid[0][j] == 1) ? 0 : dp[0][j - 1];
    }
    for (int i = 1; i < m; i++) {
        dp[i][0] = (obstacleGrid[i][0] == 1) ? 0 : dp[i - 1][0];
    }

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = (obstacleGrid[i][j] == 1) ? 0 : dp[i - 1][j] + dp[i][j - 1];
        }
    }
    return dp[m - 1][n - 1];
}
```

**Trace** on `[[0,0,0],[0,1,0],[0,0,0]]` (obstacle dead center):

```
Base cases: row0=[1,1,1], col0=[1,1,1] (no obstacles on the border)

dp[1][1]: obstacle → 0
dp[1][2]: dp[0][2]+dp[1][1] = 1+0 = 1
dp[2][1]: dp[1][1]+dp[2][0] = 0+1 = 1
dp[2][2]: dp[1][2]+dp[2][1] = 1+1 = 2

Final grid:
[1,1,1]
[1,0,1]
[1,1,2]

Answer: 2   ✓   (the only two routes around the center obstacle —
                  via the top-right corner, or via the bottom-left corner)
```

**Complexity:** O(m·n) time, O(m·n) space.

**Common mistake — Grid DP:** propagating the obstacle's blocking effect to *only* the obstacle cell itself, while leaving the rest of row 0 / column 0 incorrectly stuck at `1`. An obstacle anywhere on the border kills every cell past it in that row or column.

---

## Pattern 3 — 0/1 Knapsack Family

### Classic 0/1 Knapsack

**Statement (foundational, not tied to one specific problem).** Given n items, each with a weight and a value, and a knapsack of capacity W, choose a subset — each item used *at most once* ("0/1": take it or don't) — maximizing total value without exceeding W.

- **State:** `dp[i][w]` = max value achievable using only the first i items, with capacity w.
- **Recurrence:** `dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight[i]] + value[i])` — don't take item i, or take it (only valid if it fits).
- **Base case:** `dp[0][w] = 0` for every w — no items, no value, regardless of capacity.

```java
public int knapsack(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    int[][] dp = new int[n + 1][capacity + 1];

    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            dp[i][w] = dp[i - 1][w];   // don't take item i
            if (weights[i - 1] <= w) {
                dp[i][w] = Math.max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1]);
            }
        }
    }
    return dp[n][capacity];
}
```

**Trace** on `weights=[1,3,4,5]`, `values=[1,4,5,7]`, `capacity=7`:

```
Row 0 (no items): all zeros.
Row 1 (w=1,v=1):  [0,1,1,1,1,1,1,1]
Row 2 (w=3,v=4):  [0,1,1,4,5,5,5,5]
Row 3 (w=4,v=5):  [0,1,1,4,5,6,6,9]
Row 4 (w=5,v=7):  [0,1,1,4,5,7,8,9]

Final dp[4][7] = 9
```

**Verify:** items 2 and 3 (weight 3 + weight 4 = exactly 7, value 4 + 5 = 9) fit the capacity perfectly and are jointly optimal. ✓

**Complexity:** O(n·W) time, O(n·W) space — optimizable to **O(W)**, shown concretely below.

---

### Problem — Partition Equal Subset Sum (LeetCode 416)

**Statement.** Given positive integers, determine whether they can be split into two subsets with equal sum.

**Why this is a knapsack variant.** If the total sum is S, the question becomes "does some subset sum to exactly S/2?" (the remaining elements then automatically also sum to S/2) — exactly the 0/1 knapsack question "can value V be achieved using a subset of these items," reframed as existence instead of maximization, where each item's "weight" and "value" are the same number. An odd total sum makes this immediately impossible.

```java
public boolean canPartition(int[] nums) {
    int sum = 0;
    for (int num : nums) sum += num;
    if (sum % 2 != 0) return false;

    int target = sum / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;   // sum of 0 is always achievable — take nothing

    for (int num : nums) {
        for (int s = target; s >= num; s--) {   // DOWNWARD — see why, below
            if (dp[s - num]) {
                dp[s] = true;
            }
        }
    }
    return dp[target];
}
```

**Why the capacity loop runs downward, not upward — the entire trick of this space optimization.** This is the 1D rolling-array compression of 0/1 knapsack's 2D table, and getting the direction backward silently breaks correctness. If `s` ran *upward*, updating `dp[s]` from `dp[s-num]` could read a value of `dp[s-num]` that was *already updated earlier in this same pass, for this same item* — which means the same item just got used twice, turning 0/1 knapsack into unbounded knapsack by accident. Running downward guarantees `dp[s-num]` still holds its value from *before* the current item was considered, correctly enforcing "each item used at most once."

**Trace** on `nums=[1,5,11,5]` (target = 22/2 = 11):

```
dp=[T,F,F,F,F,F,F,F,F,F,F,F]   (index 0..11)

num=1: s=1: dp[0]=T → dp[1]=T.  (all other s: dp[s-1] still F)
       dp=[T,T,F,F,F,F,F,F,F,F,F,F]

num=5: s=6: dp[1]=T → dp[6]=T.   s=5: dp[0]=T → dp[5]=T.
       dp=[T,T,F,F,F,T,T,F,F,F,F,F]

num=11: s=11: dp[0]=T → dp[11]=T.
       dp=[T,T,F,F,F,T,T,F,F,F,F,T]

num=5 (second): s=10: dp[5]=T → dp[10]=T.  (others unchanged or already true)
       dp=[T,T,F,F,F,T,T,F,F,F,T,T]

Final dp[11] = TRUE   ✓   ({1,5,5} sums to 11; the remaining {11} also sums to 11)
```

**Complexity:** O(n·target) time, O(target) space — already the space-optimized version.

---

### Problem — Target Sum (LeetCode 494)

**Statement.** Assign `+` or `-` to each number so the result equals `target`. Count the number of ways.

**Why this is also a knapsack variant — counting, not maximizing.** Let P = sum of numbers assigned `+`, N = sum assigned `-`. Then `P + N = totalSum` (of absolute values) and `P − N = target`. Solving: `P = (totalSum + target) / 2`. The problem reduces to "count the subsets summing to exactly P" — the identical mechanism as Partition Equal Subset Sum, just counting ways instead of checking existence, and P need not be half the total.

```java
public int findTargetSumWays(int[] nums, int target) {
    int totalSum = 0;
    for (int num : nums) totalSum += num;

    if ((totalSum + target) % 2 != 0 || totalSum + target < 0) return 0;
    int P = (totalSum + target) / 2;

    int[] dp = new int[P + 1];
    dp[0] = 1;   // exactly one way to make sum 0: choose nothing

    for (int num : nums) {
        for (int s = P; s >= num; s--) {
            dp[s] += dp[s - num];   // accumulate a COUNT, not a boolean
        }
    }
    return dp[P];
}
```

**Trace** on `nums=[1,1,1,1,1]`, `target=3` → `P = (5+3)/2 = 4`:

```
dp=[1,0,0,0,0]

after num=1 (1st): dp=[1,1,0,0,0]
after num=1 (2nd): dp=[1,2,1,0,0]
after num=1 (3rd): dp=[1,3,3,1,0]
after num=1 (4th): dp=[1,4,6,4,1]
after num=1 (5th): dp=[1,5,10,10,5]

Final dp[4] = 5
```

**Verify:** P=4 means exactly 4 of the five 1's get `+` (and 1 gets `-`). The number of ways to choose *which* 4 of 5 is `C(5,4) = 5`. Matches exactly. ✓

**Complexity:** O(n·P) time, O(P) space.

---

### Coin Change — A Preview of Unbounded Knapsack

**Statement (briefly).** Given coin denominations and a target amount, find the minimum number of coins to make that amount, or −1 if impossible.

**Why this is a different knapsack variant.** Unlike the three problems above — where each number could be used at most once — a coin denomination can be used **any number of times**. This single difference flips the inner loop's required direction: Partition Equal Subset Sum and Target Sum iterated their capacity dimension *downward*, specifically to stop an item from being reused within the same pass. Coin Change's unbounded reuse means iterating *upward* isn't just safe — it's **required**: you *want* `dp[s-coin]` to potentially already reflect this same coin's use, because reuse is exactly what's allowed.

This problem gets the full bottom-up trace in this chapter's Hard DP section, specifically because the upward-vs-downward direction is worth seeing fully worked through rather than asserted. The takeaway to carry forward for now: **0/1 knapsack (each item once) iterates downward; unbounded knapsack (each item unlimited) iterates upward** — same recurrence shape, opposite direction, completely different allowed behavior.

### Space Optimization: The 1D Rolling Array

Every problem in this Pattern was shown directly in its space-optimized O(capacity) form rather than the naive O(items × capacity) 2D table, because each table row only ever depends on the *immediately preceding* row — never anything earlier. Collapsing two full rows into one array, updated in place, is always safe for 0/1 knapsack **as long as the capacity dimension is traversed downward** — exactly the detail Partition Equal Subset Sum's trace walked through concretely above.

---

*Part 3 covers String DP (Longest Common Subsequence, Edit Distance, Longest Palindromic Substring) and State Machine DP (the four Buy/Sell Stock problems, shown as the same state machine with a different k).*
