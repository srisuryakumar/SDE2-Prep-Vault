# Chapter 10: Dynamic Programming
## Part 1 — Why DP Exists · The Framework · Linear DP

*This is the second-largest chapter in the book, split across four files. Part 1 covers why DP exists at all and the five-step framework that makes every problem in this chapter approachable the same way, then works through Linear DP — six problems that build on each other so directly you'll be reusing code, not just ideas.*

## 10.1 Why DP Exists

Brute-force recursive solutions to many problems solve the *identical* subproblem over and over, because the recursion tree's branches overlap. Chapter 1's naive Fibonacci is the canonical example: `fib(5)` calls `fib(4)` and `fib(3)`; `fib(4)` *also* calls `fib(3)` — so `fib(3)` gets computed twice, `fib(2)` three times, and so on. The same question gets re-asked, and re-solved from scratch, every single time it comes up — turning what should be a small amount of genuinely distinct work into exponential O(2ⁿ) total work.

**DP's entire insight:** if you've already computed the answer to a subproblem once, cache it, and look it up instead of recomputing. This collapses the exponential blowup into something bounded by the number of *distinct* subproblems — not the number of *times* each one happens to get asked for.

## 10.2 DP vs. Recursion: Same Structure, Two Implementations

**Top-down (memoization):** write the natural recursive solution exactly as you would without DP, but check a cache first before recursing, and store the result before returning.

```java
Map<Integer, Integer> memo = new HashMap<>();

public int fib(int n) {
    if (n <= 1) return n;
    if (memo.containsKey(n)) return memo.get(n);
    int result = fib(n - 1) + fib(n - 2);
    memo.put(n, result);
    return result;
}
```

**Bottom-up (tabulation):** instead of starting at the top question and recursing down, build the answer iteratively from the smallest subproblems up, filling a table where each entry depends only on already-computed earlier entries.

```java
public int fib(int n) {
    if (n <= 1) return n;
    int[] dp = new int[n + 1];
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}
```

Both compute the *identical* thing in the *identical* O(n) time. The difference is direction of construction — and, often, how obvious the next optimization becomes. Bottom-up tends to make it visually clear when you only ever need the last few table entries, not the entire table — exactly the space optimization this Part uses repeatedly below.

## 10.3 The DP Framework — Five Steps

1. **Define the state.** What does `dp[i]` (or `dp[i][j]`) actually *represent*? Get this wrong and nothing downstream works. ("`dp[i]` = the maximum profit achievable using only the first i days.")
2. **Write the recurrence.** How does `dp[i]` relate to smaller/earlier dp values? This is "what choices exist at this step, and which is best."
3. **Identify base cases.** The smallest subproblems that can't be broken down further, with known, trivial answers.
4. **Choose top-down or bottom-up.** Top-down usually mirrors the recursive brute force you'd write first, and is often easier to *derive*. Bottom-up avoids recursion overhead and stack-depth limits, and usually makes space optimization easier to *see*.
5. **Optimize space, if possible.** If `dp[i]` only ever depends on a constant number of previous entries — not the entire history — an O(n) array often collapses to O(1) variables (or an O(n²) table to O(n), for 2D problems where each row depends only on the previous one).

---

## Pattern 1 — Linear DP (1D)

### Fibonacci → Climbing Stairs → House Robber → House Robber II

Watch how directly each problem reuses the *previous* one's state and recurrence, with only a small twist each time.

**Fibonacci:** `dp[i] = dp[i-1] + dp[i-2]` (shown above).

**Climbing Stairs (LeetCode 70).** Climb 1 or 2 steps at a time; how many distinct ways to reach the top of an n-step staircase?

- **State:** `dp[i]` = number of distinct ways to reach step i.
- **Recurrence:** `dp[i] = dp[i-1] + dp[i-2]` — your last move to reach step i was either a 1-step from i−1, or a 2-step from i−2; sum the ways to reach each.
- **Base cases:** `dp[0]=1` (one way to be at the start: do nothing), `dp[1]=1` (one way: a single 1-step).

This *is* the Fibonacci recurrence — the insight is recognizing that "ways to combine 1s and 2s summing to n" is structurally identical to "sum of the two previous terms."

```java
public int climbStairs(int n) {
    if (n <= 1) return 1;
    int prev2 = 1, prev1 = 1;   // dp[0], dp[1]
    for (int i = 2; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

(Already space-optimized to O(1) — only the last two values are ever needed. Framework Step 5, in action.)

**House Robber (LeetCode 198).** Houses hold money; you can't rob two *adjacent* houses. Maximize total money robbed.

- **State:** `dp[i]` = max money robbable considering houses `0..i`.
- **Recurrence:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` — either skip house i (keep the best from before), or rob it (plus the best achievable from two houses back, since house i−1 must then be skipped).
- **Base cases:** `dp[0]=nums[0]`, `dp[1]=max(nums[0], nums[1])`.

```java
public int rob(int[] nums) {
    if (nums.length == 1) return nums[0];
    int prev2 = nums[0];
    int prev1 = Math.max(nums[0], nums[1]);
    for (int i = 2; i < nums.length; i++) {
        int curr = Math.max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

The *shape* is identical to Climbing Stairs — a look-back-2-steps recurrence, already O(1)-space — only the combining function changed, from `a + b` to `max(a, b + value)`.

**Trace** on `nums=[2,7,9,3,1]`:

```
prev2=2 (dp[0])   prev1=max(2,7)=7 (dp[1])
i=2 (val=9): curr=max(7, 2+9=11)=11.  prev2=7,  prev1=11
i=3 (val=3): curr=max(11, 7+3=10)=11. prev2=11, prev1=11
i=4 (val=1): curr=max(11, 11+1=12)=12. prev2=11, prev1=12

Final answer: 12   ✓   (rob houses 0, 2, 4: 2+9+1=12, skipping 1 and 3)
```

**Complexity:** O(n) time, O(1) space.

**House Robber II (LeetCode 213).** Same problem, but houses form a *circle* — house 0 and house n−1 are now also adjacent.

**Key insight:** house 0 and house n−1 can never *both* be robbed (they're adjacent in the circle), so the answer is the max of two separate ordinary House Robber runs: one over houses `[0, n-2]` (excluding the last), one over `[1, n-1]` (excluding the first). Either house 0, or house n−1, or neither gets excluded — never both included.

```java
public int robCircular(int[] nums) {
    if (nums.length == 1) return nums[0];
    return Math.max(
        robLinear(nums, 0, nums.length - 2),
        robLinear(nums, 1, nums.length - 1)
    );
}

private int robLinear(int[] nums, int start, int end) {
    int prev2 = 0, prev1 = 0;
    for (int i = start; i <= end; i++) {
        int curr = Math.max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

This is the lesson worth internalizing here: recognizing "this is just House Robber, run twice on two overlapping sub-ranges, then take the max" — reducing a new problem to *exactly* a previous one's code, rather than re-deriving a recurrence from scratch — is the actual skill being tested.

**Trace** on `nums=[2,3,2]` (circular):

```
robLinear(0,1) [houses 0,1; excludes house 2]:
  i=0(2): curr=max(0,0+2)=2.  i=1(3): curr=max(2,0+3)=3.  returns 3.
robLinear(1,2) [houses 1,2; excludes house 0]:
  i=1(3): curr=max(0,0+3)=3.  i=2(2): curr=max(3,0+2)=3.  returns 3.

max(3,3) = 3
```

**Verify:** with only 3 houses arranged in a circle, every pair is adjacent — at most *one* house can ever be robbed. Best single house is house 1, value 3. Matches exactly.

**Complexity:** O(n) time, O(1) space.

---

## Problem — Decode Ways (LeetCode 91)

**Statement.** A digit string encodes letters (`A`=1, ..., `Z`=26). Count the number of ways to decode it.

- **State:** `dp[i]` = number of ways to decode the first i characters.
- **Recurrence:** `dp[i]` accumulates from two possible sources — if the single last digit (`s[i-1]`) isn't `'0'`, it can stand alone as a letter, contributing `dp[i-1]`; if the last *two* digits form a number from 10 to 26, they can be decoded together as one letter, contributing `dp[i-2]`.
- **Base cases:** `dp[0]=1` (an empty string has exactly one way to decode: nothing). `dp[1] = 1` if `s[0] != '0'`, else `0` (a leading zero can never be validly decoded).

```java
public int numDecodings(String s) {
    int n = s.length();
    if (s.charAt(0) == '0') return 0;
    int[] dp = new int[n + 1];
    dp[0] = 1;
    dp[1] = 1;

    for (int i = 2; i <= n; i++) {
        char first = s.charAt(i - 2);
        char second = s.charAt(i - 1);

        if (second != '0') {
            dp[i] += dp[i - 1];   // last digit alone is valid (1-9)
        }
        int twoDigit = (first - '0') * 10 + (second - '0');
        if (twoDigit >= 10 && twoDigit <= 26) {
            dp[i] += dp[i - 2];   // last two digits together are valid (10-26)
        }
    }
    return dp[n];
}
```

**Trace** on `s="226"`:

```
dp[0]=1, dp[1]=1 (s[0]='2' ≠ '0')

i=2: first='2', second='2'.  second≠'0' → dp[2]+=dp[1]=1.
     twoDigit=22, valid (10≤22≤26) → dp[2]+=dp[0]=1.   dp[2]=2.

i=3: first='2', second='6'.  second≠'0' → dp[3]+=dp[2]=2.
     twoDigit=26, valid → dp[3]+=dp[1]=1.               dp[3]=3.

Final dp[3] = 3
```

**Verify:** "226" decodes as `2,2,6`→"BBF", `22,6`→"VF", `2,26`→"BZ" — exactly 3 ways. ✓

**Complexity:** O(n) time, O(n) space (collapsible to O(1), exactly as Fibonacci was — `dp[i]` only ever needs `dp[i-1]` and `dp[i-2]`).

**Common mistake:** forgetting the leading-zero guard (a string starting with `'0'` has zero valid decodings — no letter maps to 0), and not noticing that the `twoDigit >= 10` check is precisely what excludes a pair like `"06"` from being treated as a valid two-digit code (since `06` as a number is `6`, which fails the `>=10` test on its own).

---

## Problem — Jump Game (LeetCode 55)

**Statement.** `nums[i]` is the maximum jump length from position i. Can you reach the last index starting from index 0?

This is normally solved *greedily*, not with classic DP table-filling — included here because "can I reach position i" is fundamentally a DP state, and the greedy simplification teaches something important: not every DP-shaped problem needs the full DP machinery. Sometimes the state collapses to a single rolling value.

**DP framing:** `dp[i] = true` if position i is reachable. Recurrence: `dp[i] = true` if some `j < i` has `dp[j]=true` and `j + nums[j] >= i`. Naive, this is O(n²) — scanning all `j < i` for every `i`.

**The greedy collapse.** Instead of tracking every individual position's reachability, track only the *farthest* reachable position seen so far while scanning left to right. The moment the current index exceeds that farthest reach, you're stuck — no jump could have gotten you here.

```java
public boolean canJump(int[] nums) {
    int farthest = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > farthest) return false;
        farthest = Math.max(farthest, i + nums[i]);
    }
    return true;
}
```

**Trace** on `nums=[3,2,1,0,4]` — deliberately built to fail:

```
farthest=0
i=0: 0>0? No.  farthest=max(0,3)=3
i=1: 1>3? No.  farthest=max(3,1+2=3)=3
i=2: 2>3? No.  farthest=max(3,2+1=3)=3
i=3: 3>3? No.  farthest=max(3,3+0=3)=3
i=4: 4>3? YES → return false   ✓   (the 0 at position 3 traps you)
```

**Complexity:** O(n) time, O(1) space — strictly better than the O(n²) naive DP, precisely because the greedy insight collapses "track every position's reachability" down to "track only the single farthest reach."

---

## Problem — Jump Game II (LeetCode 45)

**Statement.** Same setup, but minimize the number of jumps to reach the last index (guaranteed reachable).

**Approach.** Think in terms of "jump levels" — the same spirit as BFS's level-order processing (Chapter 8). All positions reachable within k jumps form one level. Track the *current level's* boundary and the farthest reach achievable from anywhere inside it. The instant the scan reaches the current level's boundary, that level is exhausted — increment the jump count and advance the boundary to the farthest reach found.

```java
public int jump(int[] nums) {
    int jumps = 0, currentEnd = 0, farthest = 0;
    for (int i = 0; i < nums.length - 1; i++) {   // never need to jump FROM the last index
        farthest = Math.max(farthest, i + nums[i]);
        if (i == currentEnd) {
            jumps++;
            currentEnd = farthest;
        }
    }
    return jumps;
}
```

**Trace** on `nums=[2,3,1,1,4]`:

```
jumps=0, currentEnd=0, farthest=0
i=0: farthest=max(0,0+2=2)=2.  i==currentEnd(0) → jumps=1, currentEnd=2
i=1: farthest=max(2,1+3=4)=4.  i==currentEnd(2)? No (1≠2)
i=2: farthest=max(4,2+1=3)=4 (unchanged).  i==currentEnd(2) → jumps=2, currentEnd=4
i=3: farthest=max(4,3+1=4)=4.  i==currentEnd(4)? No (3≠4)
loop ends (i stops at 3, since length-1=4)

Final jumps = 2   ✓   (optimal path 0→1→4: jump of 1 using nums[0]=2's capability,
                        then jump of 3 using nums[1]=3's capability)
```

**Complexity:** O(n) time, O(1) space.

**Common mistake for both Jump Game problems:** defaulting to the full O(n²) DP table under time pressure when the greedy simplification is both simpler and faster. Recognizing when a DP-shaped problem collapses to a one-pass greedy solution is itself a skill worth having — not a shortcut to feel guilty about taking.

---

*Part 2 covers Grid DP (Unique Paths, Minimum Path Sum, Unique Paths with Obstacles) and the 0/1 Knapsack family (Classic Knapsack, Partition Equal Subset Sum, Target Sum, plus the space-optimization rolling-array trick).*
