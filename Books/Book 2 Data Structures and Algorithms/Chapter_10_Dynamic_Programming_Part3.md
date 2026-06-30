# Chapter 10: Dynamic Programming
## Part 3 — String DP · State Machine DP

## Pattern 4 — String DP

### Problem — Longest Common Subsequence (LeetCode 1143)

**Statement.** Given `text1` and `text2`, return the length of their longest common subsequence (not necessarily contiguous, just in relative order).

- **State:** `dp[i][j]` = LCS length of `text1[0..i-1]` and `text2[0..j-1]`.
- **Recurrence:** if the current characters match, extend the diagonal: `dp[i][j] = dp[i-1][j-1] + 1`. Otherwise, take the better of dropping a character from either string: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
- **Base case:** `dp[0][j] = dp[i][0] = 0` — an empty string has LCS length 0 with anything.

```java
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}
```

**Trace** on `text1="abcde"`, `text2="ace"`:

```
        ""  a   c   e
    ""   0  0   0   0
    a    0  1   1   1
    b    0  1   1   1
    c    0  1   2   2
    d    0  1   2   2
    e    0  1   2   3
```

Two cells worth walking through explicitly — this is the "diagonal fill" the recurrence is named for: `dp[3][2]` ('c' vs 'c') **match** → `dp[3][2] = dp[2][1] + 1 = 1+1 = 2`, pulling diagonally up-left. `dp[5][3]` ('e' vs 'e') **match** → `dp[5][3] = dp[4][2] + 1 = 2+1 = 3`. Every non-matching cell just carries forward the better of "above" or "left."

**Final answer:** `dp[5][3] = 3` — the LCS is "ace". ✓

**Complexity:** O(m·n) time, O(m·n) space (collapsible to O(min(m,n)) via rolling rows, the same idea as Grid DP's space optimization in Part 2).

---

### Problem — Edit Distance (LeetCode 72)

**Statement.** Minimum operations (insert, delete, replace) to convert `word1` into `word2`.

- **State:** `dp[i][j]` = minimum edits to convert `word1[0..i-1]` into `word2[0..j-1]`.
- **Recurrence:** if the current characters match, no operation is needed here — inherit the diagonal directly: `dp[i][j] = dp[i-1][j-1]`. Otherwise, pay for one operation plus the best of three choices: `dp[i][j] = 1 + min(dp[i-1][j-1] [replace], dp[i-1][j] [delete], dp[i][j-1] [insert])`.
- **Base case:** `dp[0][j] = j` (j insertions to build word2 from nothing), `dp[i][0] = i` (i deletions to reduce word1 to nothing).

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(dp[i - 1][j - 1],
                                  Math.min(dp[i - 1][j], dp[i][j - 1]));
            }
        }
    }
    return dp[m][n];
}
```

**Trace** on `word1="horse"`, `word2="ros"`:

```
        ""  r   o   s
    ""   0  1   2   3
    h    1  1   2   3
    o    2  2   1   2
    r    3  2   2   2
    s    4  3   3   2
    e    5  4   4   3
```

Two illustrative cells: `dp[2][2]` ('o' vs 'o') — **match**, inherits the diagonal directly: `dp[2][2] = dp[1][1] = 1`, zero cost. `dp[3][1]` ('r' vs 'r') — also a match: `dp[3][1] = dp[2][0] = 2`. Everywhere characters *don't* match, the cell costs 1 plus the best of replace/delete/insert.

**Final answer:** `dp[5][3] = 3` — matching the well-known transformation `horse → rorse` (replace h→r) `→ rose` (delete r) `→ ros` (delete e), three operations. ✓

**Complexity:** O(m·n) time, O(m·n) space.

---

### Problem — Longest Palindromic Substring (LeetCode 5)

**Statement.** Return the longest palindromic substring of `s`.

**Why "expand around center," not a DP table, here.** A natural DP exists — `dp[i][j] = true` if `s[i..j]` is a palindrome, recurrence `dp[i][j] = (s[i]==s[j]) AND dp[i+1][j-1]` — but it needs O(n²) *space* for the full table. Expand-around-center achieves the same O(n²) *time* with only O(1) auxiliary space, by exploiting a different fact: every palindrome has a center — either a single character (odd length) or a gap between two characters (even length) — and the longest palindrome centered there is found by simply expanding outward while both sides keep matching. There are `2n−1` possible centers (n single-character, n−1 between-character), each expansion costs up to O(n), giving O(n · (2n−1)) = O(n²) overall — same time complexity as the table approach, without materializing the table.

```java
public String longestPalindrome(String s) {
    if (s.length() < 1) return "";
    int start = 0, maxLen = 1;

    for (int center = 0; center < s.length(); center++) {
        int len1 = expandFromCenter(s, center, center);       // odd-length center
        int len2 = expandFromCenter(s, center, center + 1);   // even-length center
        int len = Math.max(len1, len2);
        if (len > maxLen) {
            maxLen = len;
            start = center - (len - 1) / 2;
        }
    }
    return s.substring(start, start + maxLen);
}

private int expandFromCenter(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return right - left - 1;
}
```

**Trace** on `s="babad"`:

```
center=0 ('b'): odd expand → len=1.  even expand ('b' vs 'a') → no match, len=0.
                max=1, not > current best (1) → no update.

center=1 ('a'): odd expand: 'a' matches itself, then 'b' vs 'b' matches, then 'a' vs (out of bounds
                comparison fails the loop since left<0) → len=3.  even: 'a' vs 'b' → len=0.
                max=3 > 1 → update: maxLen=3, start=1-(3-1)/2=0.

center=2 ('b'): odd expand: 'b' matches, 'a' vs 'a' matches, 'b' vs 'd' → stop. len=3.
                even: 'b' vs 'a' → len=0.
                max=3, not > current best (3) → no update (keeps the first-found tie, "bab").

center=3,4: shorter palindromes found, neither beats maxLen=3.
```

**Final:** `maxLen=3`, `start=0` → `"bab"` ✓ (LeetCode accepts either `"bab"` or `"aba"` for this input — both are valid longest palindromes; this trace happens to find `"bab"` first since it was checked first and ties don't overwrite).

**Complexity:** O(n²) time. Space O(1) auxiliary.

**Common mistake:** checking only odd-length centers (or only even-length). Skipping either misses roughly half of all possible palindromes outright — `"abba"` is even-length and would never be found by single-character centers alone.

---

## Pattern 5 — State Machine DP

### Best Time to Buy and Sell Stock I (LeetCode 121) — One Transaction

**Statement.** `prices[i]` = price on day i. Maximize profit from exactly one buy and one sell (buy before sell).

**The state machine.** On any day you're in one of two states — holding no stock, or holding one share — and you track the best profit achievable in each:

- `cash[i]` = max profit on day i, not holding stock.
- `hold[i]` = max profit on day i, holding stock (this can be negative — money spent on a still-unsold share).

**Recurrence:** `cash[i] = max(cash[i-1], hold[i-1] + prices[i])` (stay in cash, or sell today). `hold[i] = max(hold[i-1], -prices[i])` (keep holding from before, or buy today — starting fresh, since only one transaction total is allowed).

**Base case:** `cash[0]=0`, `hold[0]=-prices[0]`.

```java
public int maxProfit(int[] prices) {
    int cash = 0, hold = -prices[0];
    for (int i = 1; i < prices.length; i++) {
        cash = Math.max(cash, hold + prices[i]);
        hold = Math.max(hold, -prices[i]);
    }
    return cash;
}
```

**Trace** on `prices=[7,1,5,3,6,4]`:

```
cash=0, hold=-7
i=1(1): cash=max(0,-7+1=-6)=0.  hold=max(-7,-1)=-1
i=2(5): cash=max(0,-1+5=4)=4.   hold=max(-1,-5)=-1
i=3(3): cash=max(4,-1+3=2)=4.   hold stays -1
i=4(6): cash=max(4,-1+6=5)=5.   hold stays -1
i=5(4): cash=max(5,-1+4=3)=5.   hold stays -1

Final cash = 5   ✓   (buy at 1, sell at 6: profit 5)
```

**Complexity:** O(n) time, O(1) space.

### Best Time to Buy and Sell Stock II (LeetCode 122) — Unlimited Transactions

**The one change.** Buying no longer starts fresh at `-prices[i]` — it can **reinvest** cash already banked from a previous completed transaction: `hold[i] = max(hold[i-1], cash[i-1] - prices[i])`.

```java
public int maxProfit(int[] prices) {
    int cash = 0, hold = -prices[0];
    for (int i = 1; i < prices.length; i++) {
        int prevCash = cash;
        cash = Math.max(cash, hold + prices[i]);
        hold = Math.max(hold, prevCash - prices[i]);   // reinvest, don't start fresh
    }
    return cash;
}
```

(`prevCash` is saved *before* updating `cash` this iteration — `hold`'s update needs *yesterday's* cash, not today's just-updated value. A subtle but easy ordering trap.)

**Trace** on `prices=[7,1,5,3,6,4]`:

```
cash=0, hold=-7
i=1(1): cash=0.  hold=max(-7,0-1=-1)=-1
i=2(5): cash=max(0,-1+5=4)=4.  hold=max(-1,0-5)=-1
i=3(3): cash=max(4,-1+3=2)=4.  hold=max(-1,4-3=1)=1
i=4(6): cash=max(4,1+6=7)=7.   hold=max(1,4-6)=1
i=5(4): cash=max(7,1+4=5)=7.   hold=max(1,7-4=3)=3

Final cash = 7   ✓   (buy@1 sell@5: +4.  buy@3 sell@6: +3.  total 7)
```

**Complexity:** O(n) time, O(1) space.

### Best Time to Buy and Sell Stock III (LeetCode 123) — At Most Two Transactions

Now there are two transaction "slots" to track, each with its own hold/cash pair: `hold1, cash1` (after the first transaction), `hold2, cash2` (after the second, funded by the first's profit).

```java
public int maxProfit(int[] prices) {
    int hold1 = -prices[0], cash1 = 0;
    int hold2 = -prices[0], cash2 = 0;

    for (int i = 1; i < prices.length; i++) {
        cash2 = Math.max(cash2, hold2 + prices[i]);      // sell 2nd stock
        hold2 = Math.max(hold2, cash1 - prices[i]);       // buy 2nd, funded by 1st transaction's profit
        cash1 = Math.max(cash1, hold1 + prices[i]);       // sell 1st stock
        hold1 = Math.max(hold1, -prices[i]);               // buy 1st, starting fresh
    }
    return cash2;
}
```

**Why this exact update order (cash2, hold2, cash1, hold1) matters.** `hold2`'s update reads `cash1`, which must still hold *yesterday's* value — the first transaction's profit *before* today's potential sale. If `cash1` were updated earlier in the same iteration, `hold2` would read *today's* `cash1`, letting the two transactions effectively overlap on the same day. Processing the second-transaction states before the first-transaction states means every read happens before its corresponding write this iteration — no temp variables needed.

**Trace** on `prices=[3,3,5,0,0,3,1,4]`:

```
hold1=-3, cash1=0, hold2=-3, cash2=0

i=3 (price=0): cash1=max(0,-3+0)=0.  hold1=max(-3,0)=0
i=5 (price=3): cash1=max(0,0+3)=3.   cash2=max(...,2,2-3...)→ cash2 reaches 2→5 across the
                                       relevant steps as hold2 picks up cash1's value of 2
i=7 (price=4): cash2 reaches 6
```

*(Full step-by-step values: after processing every price, `cash2` ends at 6.)*

**Verify:** buy@0 (day index 3, price 0), sell@3 (day index 5, price 3): profit 3. Buy@1 (day index 6, price 1), sell@4 (day index 7, price 4): profit 3. Total = 6. ✓ Matches `cash2 = 6`.

**Complexity:** O(n) time, O(1) space.

### Best Time to Buy and Sell Stock IV (LeetCode 188) — At Most K Transactions

**The generalization.** Instead of hardcoding two `(hold, cash)` pairs, use arrays of size `k+1`, and loop over transaction number on each day, applying the identical update logic as Stock III — just parameterized by k instead of fixed at 2.

```java
public int maxProfit(int k, int[] prices) {
    if (prices.length == 0) return 0;
    int[] hold = new int[k + 1];
    int[] cash = new int[k + 1];
    Arrays.fill(hold, -prices[0]);

    for (int i = 1; i < prices.length; i++) {
        for (int t = k; t >= 1; t--) {   // highest transaction number first — same reason as Stock III
            cash[t] = Math.max(cash[t], hold[t] + prices[i]);
            hold[t] = Math.max(hold[t], cash[t - 1] - prices[i]);
        }
    }
    return cash[k];
}
```

This single piece of code, run with `k=2`, computes *exactly* what the hand-unrolled Stock III solution computes — and with `k=1`, exactly Stock I.

**Stand back and look at what just happened across all four problems.** Stock I is this k-parameterized machine with `k=1`. Stock III is `k=2`, unrolled by hand into named variables instead of array indices. Stock IV is the identical machine, generalized to any `k`. The one problem that *doesn't* fit this mold is Stock II — and that's not a coincidence, it's the defining feature of "unlimited": once there's no cap on transaction count, there's nothing left to index by, so the state collapses from k separate pairs down to a single pair that simply reinvests freely. Four problems, one state machine, with "how many transactions are allowed" as the single parameter explaining every difference between them.

**Complexity:** O(n·k) time, O(k) space.

---

*Part 4 closes the chapter with the three Hard DP problems — Longest Increasing Subsequence (O(n²), then the O(n log n) patience-sort refinement), Word Break (top-down with memoization), and Coin Change's full bottom-up trace — followed by the chapter-wide common mistakes, pattern recognition guide, and summary.*
