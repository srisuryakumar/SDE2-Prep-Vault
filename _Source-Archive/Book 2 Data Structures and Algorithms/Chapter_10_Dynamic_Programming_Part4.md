# Chapter 10: Dynamic Programming
## Part 4 — Hard DP Problems · Chapter Wrap-Up

## Problem — Longest Increasing Subsequence (LeetCode 300)

**Statement.** Return the length of the longest *strictly increasing* subsequence of an integer array.

### The O(n²) DP Approach

- **State:** `dp[i]` = length of the longest increasing subsequence *ending exactly at* index i (not "using the first i elements" — specifically ending there).
- **Recurrence:** `dp[i] = 1 + max(dp[j])` over every `j < i` where `nums[j] < nums[i]`; or just `1` if no such j exists.
- **Base case:** every `dp[i] = 1` initially — any single element is, alone, an increasing subsequence of length 1.

The final answer is `max(dp)` over *every* index, since the LIS might end anywhere, not necessarily at the last position.

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

**Trace** on `nums=[10,9,2,5,3,7,101,18]`:

```
dp starts at [1,1,1,1,1,1,1,1]

i=3 (val=5): j=2 (val=2 < 5) → dp[3]=max(1, dp[2]+1=2)=2
i=4 (val=3): j=2 (val=2 < 3) → dp[4]=2
i=5 (val=7): j=3 (val=5 < 7) → dp[5]=max(2, dp[3]+1=3)=3.  j=4 also qualifies but gives the same 3.
i=6 (val=101): every earlier value qualifies; best is dp[5]+1 = 3+1 = 4 → dp[6]=4
i=7 (val=18): best qualifying is dp[5]+1 = 3+1 = 4 (j=6 doesn't qualify, 101 is not < 18) → dp[7]=4

Final dp = [1,1,1,2,2,3,4,4].  maxLen = 4
```

**Verify:** `[2,3,7,101]` (or `[2,5,7,101]`, or `[2,3,7,18]`) is a valid increasing subsequence of length 4. ✓

**Complexity:** O(n²) time, O(n) space.

### The O(n log n) Refinement — Patience Sort

**Intuition.** Maintain an array `tails`, where `tails[k]` is the *smallest possible* tail value among all increasing subsequences of length `k+1` found so far. Keeping each tail as small as possible maximizes the chance that *future* numbers can extend that subsequence further — and critically, this greedy choice keeps `tails` itself sorted at all times, which is exactly what makes binary search valid here at all. For each new number, binary search finds where it belongs: it either replaces the first tail that's `≥` itself (improving an existing length), or — if it's bigger than every current tail — extends the array, representing a new longest length found.

```java
public int lengthOfLIS(int[] nums) {
    List<Integer> tails = new ArrayList<>();
    for (int num : nums) {
        int pos = Collections.binarySearch(tails, num);
        if (pos < 0) {
            pos = -(pos + 1);   // binarySearch's convention for "not found": insertion point
        }
        if (pos == tails.size()) {
            tails.add(num);          // bigger than every current tail — extends the LIS length
        } else {
            tails.set(pos, num);     // found a smaller tail for this length — improve it
        }
    }
    return tails.size();
}
```

**Trace** on the same input, `nums=[10,9,2,5,3,7,101,18]`:

```
num=10: tails=[] → append.            tails=[10]
num=9:  9<10, replaces index0.        tails=[9]
num=2:  2<9, replaces index0.         tails=[2]
num=5:  5>2, appends.                 tails=[2,5]
num=3:  3 is between 2 and 5, replaces index1.   tails=[2,3]
num=7:  7>3, appends.                 tails=[2,3,7]
num=101: 101>7, appends.              tails=[2,3,7,101]
num=18: 18 is between 7 and 101, replaces index3.  tails=[2,3,7,18]

Final tails.size() = 4   ✓   matches the O(n²) result exactly.
```

**An important caveat.** `tails` does *not* necessarily represent an actual subsequence that appears in the original array — it tracks the best *tail value* for each length, and that value can get overwritten by elements belonging to entirely different candidate subsequences over time. (In this particular trace, `[2,3,7,18]` happens to also be a genuinely valid subsequence of the input — but that's a coincidence of this example, not a guarantee. The *length* of `tails` is always correct; recovering the actual subsequence would need additional parent-pointer bookkeeping not shown here, since the problem only asks for the length.)

**Complexity:** O(n log n) time — n numbers, each costing one O(log n) binary search. Space O(n).

**Common mistake:** using the wrong flavor of binary search (lower-bound vs. upper-bound) for *strictly* increasing vs. non-decreasing variants of this problem — the choice determines whether equal elements extend or replace, and using the wrong one silently breaks the non-strict variant.

---

## Problem — Word Break (LeetCode 139)

**Statement.** Given a string `s` and a dictionary `wordDict`, return true if `s` can be segmented into a sequence of one or more dictionary words.

**Approach — top-down with memoization.** Define `canBreak(start)` = true if `s[start..]` can be fully segmented. Try every possible end position for the *first* word beginning at `start`; if that prefix is a dictionary word *and* the rest (`canBreak(end)`) can also be broken, succeed. Memoize on `start` — different recursive paths can reach the *same* starting position multiple times, and without caching, the identical question gets re-solved from scratch every time. This is Chapter 1's "overlapping subproblems" justification for DP, made completely concrete.

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> wordSet = new HashSet<>(wordDict);
    Map<Integer, Boolean> memo = new HashMap<>();
    return canBreak(s, 0, wordSet, memo);
}

private boolean canBreak(String s, int start, Set<String> wordSet, Map<Integer, Boolean> memo) {
    if (start == s.length()) return true;
    if (memo.containsKey(start)) return memo.get(start);

    for (int end = start + 1; end <= s.length(); end++) {
        String prefix = s.substring(start, end);
        if (wordSet.contains(prefix) && canBreak(s, end, wordSet, memo)) {
            memo.put(start, true);
            return true;
        }
    }
    memo.put(start, false);
    return false;
}
```

**Trace** on `s="leetcode"`, `wordDict=["leet","code"]`:

```
canBreak(0): try "l","le","lee" — none in dict.
             "leet" IS in dict → recurse canBreak(4):
                try "c","co","cod" — none in dict.
                "code" IS in dict → recurse canBreak(8):
                    start == s.length() (8) → return true immediately.
                canBreak(4) found a working split → memo[4]=true, return true.
             canBreak(0) found a working split → memo[0]=true, return true.

Final result: true   ✓   ("leet" + "code" = "leetcode")
```

**Complexity:** O(n³) worst case without memoization-aware analysis — O(n) start positions × O(n) end positions × O(n) substring cost — but memoization guarantees each *distinct* `start` value's work happens exactly once, regardless of how many different recursive paths arrive at it. Without that memo, the naive recursion is exponential. Space O(n) for the memo plus O(n) recursion stack.

**Common mistake:** omitting the memo (or memoizing on the wrong key), which silently turns a polynomial algorithm back into an exponential one on adversarial inputs — a string like `"aaaaaaaaaaaaaaaaab"` against a dictionary full of short `'a'`-prefixes will re-explore the same failing suffixes exponentially many times without it.

---

## Problem — Coin Change (LeetCode 322) — Bottom-Up, Full Trace

**Statement.** Given coin denominations and a target amount, find the *minimum* number of coins to make that amount exactly, or −1 if impossible.

This is the unbounded-knapsack problem previewed in Part 2 — each coin denomination usable an unlimited number of times, which is exactly why the loop direction here is the *opposite* of Partition Equal Subset Sum's.

- **State:** `dp[a]` = minimum coins needed to make amount a.
- **Recurrence:** `dp[a] = min over every coin c (c ≤ a) of (dp[a-c] + 1)` — try using one more of coin c, on top of however many coins made the remaining amount.
- **Base case:** `dp[0] = 0`; every other `dp[a]` starts at infinity (unreached, until proven otherwise).

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;

    for (int coin : coins) {
        for (int a = coin; a <= amount; a++) {   // UPWARD — unbounded reuse is intentional
            if (dp[a - coin] != Integer.MAX_VALUE) {
                dp[a] = Math.min(dp[a], dp[a - coin] + 1);
            }
        }
    }
    return dp[amount] == Integer.MAX_VALUE ? -1 : dp[amount];
}
```

**Why upward here — the exact mirror image of Partition Equal Subset Sum, and worth seeing why both are correct.** There, iterating upward would have let the same item count twice in one pass — a bug, since each item was meant to be used at most once. **Here, that's not a bug, it's the entire point**: a coin denomination is allowed unlimited uses, so `dp[a-coin]` is *supposed* to potentially already reflect this same coin's use (making amount 11 with coin 5 might lean on `dp[6]`, which itself may have already used a 5). Iterating downward here would *incorrectly forbid* that reuse, undercounting and potentially missing the true minimum.

**Full trace** on `coins=[1,2,5]`, `amount=11`:

```
dp = [0,∞,∞,∞,∞,∞,∞,∞,∞,∞,∞,∞]   (indices 0..11)

After coin=1 (every dp[a] = dp[a-1]+1, building up by ones):
dp = [0,1,2,3,4,5,6,7,8,9,10,11]

After coin=2 (a=2..11, each checking dp[a-2]+1 against the current value):
a=2: dp[0]+1=1 < 2  → dp[2]=1
a=4: dp[2]+1=2 < 4  → dp[4]=2
a=6: dp[4]+1=3 < 6  → dp[6]=3
a=8: dp[6]+1=4 < 8  → dp[8]=4
a=10: dp[8]+1=5 < 10 → dp[10]=5
(odd positions also improve via the chain, e.g. a=3: dp[1]+1=2<3→dp[3]=2; a=5: dp[3]+1=3<5→dp[5]=3, etc.)
dp = [0,1,1,2,2,3,3,4,4,5,5,6]

After coin=5 (a=5..11, each checking dp[a-5]+1):
a=5:  dp[0]+1=1 < 3  → dp[5]=1
a=6:  dp[1]+1=2 < 3  → dp[6]=2
a=7:  dp[2]+1=2 < 4  → dp[7]=2
a=8:  dp[3]+1=3 < 4  → dp[8]=3
a=9:  dp[4]+1=3 < 5  → dp[9]=3
a=10: dp[5]+1=2 < 5  → dp[10]=2
a=11: dp[6]+1=3 < 6  → dp[11]=3

Final dp = [0,1,1,2,2,1,2,2,3,3,2,3]
```

**Final answer:** `dp[11] = 3` ✓ — matching `5 + 5 + 1 = 11`, three coins, the known minimum for this classic example.

**Complexity:** O(amount × coins.length) time, O(amount) space.

**Common mistake:** treating the loop nesting and direction as arbitrary stylistic choices. They encode real semantic differences — getting the *direction* wrong here (downward instead of upward) would forbid legitimate coin reuse; a *different* but related problem (counting the *number of ways* to make change, not the minimum coin count) is sensitive to which loop is outer vs. inner in a way that changes whether permutations of the same coins get counted as distinct. The loop structure is part of the algorithm's correctness, not a formatting preference.

---

## Common Mistakes — Chapter-Wide

- **Writing code before stating the state definition out loud.** "What does `dp[i]` mean" is the one sentence that, if wrong, invalidates everything built on top of it.
- **Getting knapsack loop direction backward.** 0/1 knapsack (each item once), space-optimized to 1D, needs the capacity dimension iterated *downward*; unbounded knapsack (Coin Change) needs it iterated *upward*. Confusing the two either silently permits illegal reuse or silently forbids legal reuse.
- **Forgetting to propagate base-case blocking fully**, as in Unique Paths with Obstacles — an "impossible from here" condition on the border affects *everything past it* in that row/column, not just the one cell.
- **Initializing a rolling "best so far" variable to 0** instead of the first real value — breaks on all-negative or single-element inputs (Kadane's trap from Chapter 2, recurring constantly across this chapter's rolling-variable optimizations).
- **Defaulting to a full O(n²) DP table-fill for Jump Game / Jump Game II** when a simpler greedy one-pass solution exists. Recognizing the collapse is a skill, not a corner cut.
- **Skipping memoization, or memoizing on the wrong key**, in top-down recursion — silently turns a polynomial algorithm back into an exponential one on adversarial inputs (Word Break).
- **Treating the O(n log n) LIS `tails` array as an actual subsequence from the input.** It tracks the best tail value per length, not one coherent sequence of elements — only its *length* is guaranteed meaningful without extra bookkeeping.

## Pattern Recognition Guide

- "Count the ways" or "minimum/maximum X," where brute-force recursion would re-solve the same smaller question repeatedly → DP. Start by naming the state.
- "Sequence of choices, each affecting what's available next, with adjacency/exclusion constraints" → Linear DP, usually collapsible to O(1) space via two rolling variables.
- "Path through a grid" → Grid DP, base cases along row 0 and column 0.
- "Choose a subset respecting a capacity/budget" → 0/1 Knapsack family; "subset sums to X" and "count subsets achieving X" are both knapsack in disguise, framed as existence or counting instead of maximization.
- "Make change / minimum pieces / unlimited supply of each option" → unbounded knapsack; the loop direction flips relative to 0/1 knapsack specifically because reuse is now intentional.
- "Compare or transform two strings/sequences" → 2D String DP, almost always branching on "do the current two characters match."
- "Longest palindrome" → expand around center, O(n²) time and O(1) space.
- "Multiple transactions allowed, with constraints on count or cooldown" → State Machine DP — name the states explicitly before writing any recurrence.
- "Longest increasing run," with an O(n log n) requirement → patience sort / binary search on a `tails` array, not the naive O(n²) table.

## Chapter Summary

- DP exists because brute-force recursion on problems with overlapping subproblems repeats identical work exponentially; caching each distinct subproblem's answer collapses that to polynomial time.
- The five-step framework — state, recurrence, base cases, top-down or bottom-up, space optimization — applies to every problem in this chapter without exception. The state definition is the step that, if wrong, invalidates everything after it.
- Linear DP problems chain directly off each other: Fibonacci's recurrence *is* Climbing Stairs', which generalizes into House Robber's via a different combining function, which generalizes again into House Robber II by splitting one circular problem into two linear ones.
- Grid DP's base cases live along row 0 and column 0, and any "impossible from here" condition must propagate through the rest of that row/column, not just the triggering cell.
- 0/1 Knapsack and unbounded knapsack share an identical recurrence shape but require *opposite* loop directions once space-optimized to 1D — downward forbids reuse, upward permits it. Get this backward and the resulting bug is silent, not a crash.
- String DP recurrences branch on character equality almost universally — a match inherits the diagonal (LCS, Edit Distance); a mismatch pays a cost and takes the best available neighbor.
- State Machine DP names its states explicitly (holding stock or not, which transaction number) and reveals that four seemingly separate Stock problems are one parameterized machine, with "how many transactions are allowed" as the single variable explaining every difference between them.
- This chapter's hardest problems (LIS, Word Break, Coin Change) aren't hard because their recurrences are exotic — they're hard because each hides a non-obvious complexity improvement (patience sort's binary search, memoization preventing exponential blowup, the unbounded-vs-0/1 loop-direction distinction) underneath an otherwise ordinary-looking DP table.
