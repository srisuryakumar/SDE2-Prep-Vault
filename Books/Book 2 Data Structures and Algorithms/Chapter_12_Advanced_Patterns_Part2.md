# Chapter 12: Advanced Patterns
## Part 2 — Fenwick Tree · Bit Manipulation · KMP · Math Patterns

## Binary Indexed Tree (Fenwick Tree)

**What it solves.** The identical problem as a segment tree — prefix sum with point updates — with simpler code and better practical performance, at the cost of being less general. Segment trees handle any associative combiner (min, max, gcd, ...); a Fenwick tree relies on a clever index decomposition that works cleanly only for operations with an inverse, like sum (whose inverse is subtraction).

**The key insight.** Index `i` in the Fenwick array stores the sum of a specific range of elements, determined by `i`'s **lowest set bit**: `tree[i]` covers indices `(i - lowbit(i) + 1)` through `i`, where `lowbit(i) = i & (-i)`.

- **Update(index, delta):** add `delta` to `tree[index]`, then jump to the next index that "covers" this one by adding the lowest set bit (`index += index & (-index)`), repeating until past n.
- **Query(index)** (prefix sum from 1 to index): accumulate `tree[index]`, then jump to the parent range by *subtracting* the lowest set bit (`index -= index & (-index)`), repeating until reaching 0.

```java
class FenwickTree {
    int[] tree;
    int n;

    FenwickTree(int n) {
        this.n = n;
        tree = new int[n + 1];   // 1-indexed
    }

    void update(int index, int delta) {
        for (; index <= n; index += index & (-index)) {
            tree[index] += delta;
        }
    }

    int query(int index) {   // prefix sum from 1 to index
        int sum = 0;
        for (; index > 0; index -= index & (-index)) {
            sum += tree[index];
        }
        return sum;
    }

    int rangeQuery(int left, int right) {   // sum from left to right, inclusive (1-indexed)
        return query(right) - query(left - 1);
    }
}
```

**Build trace** via repeated updates on values `[5,3,7,1,4,6,2,8]` at 1-indexed positions 1–8 (this "build by repeated update" approach costs O(n log n); a more clever direct O(n) construction exists but is omitted here for clarity):

```
After all 8 updates:
tree[1]=5  tree[2]=8  tree[3]=7  tree[4]=16  tree[5]=4  tree[6]=10  tree[7]=2  tree[8]=36

Verify a few:
tree[8] (lowbit=8, covers 1-8): 5+3+7+1+4+6+2+8 = 36   ✓
tree[4] (lowbit=4, covers 1-4): 5+3+7+1 = 16            ✓
tree[6] (lowbit=2, covers 5-6): 4+6 = 10                ✓
```

**Query trace** — `query(5)`, expecting `5+3+7+1+4=20`:

```
index=5: sum += tree[5]=4 → sum=4.  index -= lowbit(5)=1 → index=4
index=4: sum += tree[4]=16 → sum=20.  index -= lowbit(4)=4 → index=0 → stop

Final: 20   ✓
```

**Range query trace** — `rangeQuery(3,5)`, expecting `7+1+4=12`:

```
= query(5) - query(2) = 20 - 8 = 12   ✓   (query(2): tree[2]=8, then index→0)
```

**Update trace** — `update(3, 10)` (position 3 changes from 7 to 17):

```
index=3: tree[3] += 10 → 17.  index += lowbit(3)=1 → index=4
index=4: tree[4] += 10 → 26.  index += lowbit(4)=4 → index=8
index=8: tree[8] += 10 → 46.  index += lowbit(8)=8 → 16 > n → stop

Verify: new total = 36+10 = 46 = tree[8]   ✓.  new prefix(1-4) = 5+3+17+1 = 26 = tree[4]   ✓
```

**Complexity:** update and query are both O(log n) — bounded by the bit-length of n. Space O(n).

**Common mistake:** forgetting the 1-indexed convention. `index & (-index)` on index 0 gives 0, breaking the loop entirely (an infinite loop, or a silent no-op, depending on the exact code shape) — always shift to 1-indexing.

**Segment tree vs. Fenwick tree, practically:** segment trees are more general (any associative combiner) and conceptually more direct, at the cost of more code and roughly 4× the memory. Fenwick trees are shorter and faster in practice, but fundamentally tied to operations with a clean inverse — sum's inverse is subtraction, which is what makes `rangeQuery`'s prefix-difference trick work; min/max have no such inverse, so a plain Fenwick tree can't support range-min-query the way it supports range-sum-query. Default to Fenwick tree when the problem is specifically about sums with point updates; reach for a segment tree otherwise, or when range *updates* (not just range queries) are needed — segment-tree variants with lazy propagation handle that, a topic beyond this book's scope.

---

## Bit Manipulation

### XOR Trick — Find the Single Number (LeetCode 136)

**Statement.** Every element appears twice except one, which appears once. Find it in O(n) time, O(1) space.

**Why XOR solves this.** Two properties: `x ^ x = 0` (a number XORed with itself cancels), and XOR is commutative/associative (order doesn't matter). XOR the entire array together: every paired element cancels itself out, leaving only the single unpaired element (since XORing anything with 0 leaves it unchanged).

```java
public int singleNumber(int[] nums) {
    int result = 0;
    for (int num : nums) {
        result ^= num;
    }
    return result;
}
```

**Trace** on `nums=[4,1,2,1,2]`: `0^4=4`, `4^1=5`, `5^2=7`, `7^1=6`, `6^2=4`. **Final: 4** ✓ (1 and 2 each appear twice and cancel; 4 is left over).

**Complexity:** O(n) time, O(1) space — dramatically better than a HashMap-based frequency count (O(n) time, but O(n) space), precisely because XOR cancels pairs without needing to remember which values were seen.

### Popcount — Counting Set Bits

**The trick (Brian Kernighan's algorithm):** `n & (n-1)` clears the *lowest* set bit of n. Repeating this and counting iterations gives the number of set bits — the loop runs once per set bit, not once per bit position.

```java
public int popcount(int n) {
    int count = 0;
    while (n != 0) {
        n = n & (n - 1);
        count++;
    }
    return count;
}
```

**Why `n & (n-1)` clears the lowest set bit.** Subtracting 1 flips every bit from the lowest set bit downward — that bit becomes 0, and every 0 bit below it becomes 1 (binary subtraction's borrow chain). ANDing the original n with this flipped version keeps only the bits unchanged by the subtraction (everything *above* the original lowest set bit); the lowest set bit itself, now 0 in `n-1`, gets zeroed by the AND.

**Trace** on `n=12` (binary `1100`): `1100 & 1011 = 1000` (count=1) → `1000 & 0111 = 0000` (count=2) → loop ends. **popcount(12) = 2** ✓.

**Complexity:** O(k), k = number of set bits — better than a flat O(32) bit-by-bit scan when the number is sparse.

### Power of Two Check

A power of 2 has exactly one set bit. The same `n & (n-1)` trick: clearing that single bit leaves exactly 0.

```java
public boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

(`n > 0` matters because `n=0` would otherwise pass: `0 & (-1) = 0`, but 0 isn't a power of 2.)

**Trace:** `n=16` (`10000`): `10000 & 01111 = 0` and `n>0` → **true**. `n=18` (`10010`, not a power of 2): `10010 & 10001 = 10000 ≠ 0` → **false**. Both correct.

**Complexity:** O(1).

---

## KMP (Knuth-Morris-Pratt) String Matching

**What it solves.** Find every occurrence of a pattern in a text, in O(n+m) time — strictly better than naive O(n·m) matching, which re-scans overlapping prefixes from scratch on every mismatch.

**The key insight — the failure function (LPS array, "longest proper prefix which is also a suffix").** Precompute, for every position i in the *pattern*, the length of the longest proper prefix of `pattern[0..i]` that's also a suffix of it. On a mismatch during matching, instead of restarting the pattern comparison from scratch, jump the pattern pointer directly to the next position that could still match — skipping everything guaranteed to fail, because the characters leading up to the mismatch are already known (from the precomputed overlap) to match a known prefix of the pattern.

### Building the Failure Function

```java
private int[] buildLPS(String pattern) {
    int m = pattern.length();
    int[] lps = new int[m];
    int len = 0;
    int i = 1;

    while (i < m) {
        if (pattern.charAt(i) == pattern.charAt(len)) {
            len++;
            lps[i] = len;
            i++;
        } else if (len != 0) {
            len = lps[len - 1];   // fall back to a shorter candidate, don't advance i
        } else {
            lps[i] = 0;
            i++;
        }
    }
    return lps;
}
```

**Trace** on `pattern="ababaca"`:

```
i=1 'b' vs pattern[0]='a': mismatch, len=0 → lps[1]=0
i=2 'a' vs pattern[0]='a': match → len=1, lps[2]=1
i=3 'b' vs pattern[1]='b': match → len=2, lps[3]=2
i=4 'a' vs pattern[2]='a': match → len=3, lps[4]=3
i=5 'c' vs pattern[3]='b': mismatch → len=lps[2]=1
     'c' vs pattern[1]='b': still mismatch → len=lps[0]=0
     'c' vs pattern[0]='a': still mismatch, len=0 → lps[5]=0
i=6 'a' vs pattern[0]='a': match → len=1, lps[6]=1

Final lps = [0,0,1,2,3,0,1]
```

**Verify:** `lps[4]=3` — the longest proper prefix of "ababa" that's also a suffix is "aba" (length 3). ✓ `lps[6]=1` — for the whole pattern "ababaca," it's just "a" (the trailing 'c' breaks any longer match). ✓

### Matching with the Failure Function

```java
public List<Integer> kmpSearch(String text, String pattern) {
    List<Integer> matches = new ArrayList<>();
    int[] lps = buildLPS(pattern);
    int n = text.length(), m = pattern.length();
    int i = 0, j = 0;

    while (i < n) {
        if (text.charAt(i) == pattern.charAt(j)) {
            i++; j++;
            if (j == m) {
                matches.add(i - j);
                j = lps[j - 1];   // keep searching for further (possibly overlapping) matches
            }
        } else if (j != 0) {
            j = lps[j - 1];      // fall back via the failure function — i does NOT move
        } else {
            i++;
        }
    }
    return matches;
}
```

**Why this is O(n+m), not O(n·m).** The text pointer `i` *never* moves backward across the entire algorithm — at most O(n) total advancement. The pattern pointer `j` falls back via the failure function, but each fallback strictly decreases j, and j was only ever increased at most n times total (once per matching advance of i); so total fallback operations are bounded by O(n) as well. Building the LPS array is a separate O(m) step. Combined: O(n+m).

**Trace**, isolating the failure-function payoff, on `text="ababcababaca"`, `pattern="ababaca"` (lps = `[0,0,1,2,3,0,1]`):

```
i=0..3: 'a','b','a','b' all match → i=4, j=4
i=4: text[4]='c' vs pattern[4]='a' → mismatch.  j=lps[3]=2  (i stays at 4!)
     text[4]='c' vs pattern[2]='a' → still mismatch.  j=lps[1]=0
     text[4]='c' vs pattern[0]='a' → still mismatch, j=0 → ONLY NOW does i advance: i=5
i=5: text[5]='a' vs pattern[0]='a' → match → i=6, j=1
...(continues to find a full match starting at index 5)
```

The point worth isolating: at `i=4`, the algorithm tried `j=2` then `j=0` *without ever moving `i` backward or rescanning `text[0..3]`* — the failure function supplied "what's the next-best partial match length" using information already extracted from the pattern during preprocessing, never touching the text a second time for characters already known to match.

**Complexity:** O(n+m) time, O(m) space for the LPS array.

---

## Math Patterns

### GCD / LCM

```java
public int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}
```

**Why this works.** `gcd(a,b) = gcd(b, a mod b)` because any common divisor of a and b must also divide `a mod b` (since `a mod b = a - k·b` for some integer k, and a divisor of both a and `k·b` divides their difference too). Repeating shrinks the pair until one side hits 0, at which point the other side *is* the gcd (`gcd(x, 0) = x`, since everything divides 0).

```java
public long lcm(int a, int b) {
    return (long) a / gcd(a, b) * b;   // divide before multiplying to reduce overflow risk
}
```

(`lcm(a,b) = a·b / gcd(a,b)` — dividing by gcd *before* multiplying, rather than after, keeps intermediate values smaller.)

### Sieve of Eratosthenes

**What it solves.** All primes up to n, in roughly O(n log log n) — far better than checking each number individually for primality (O(√n) each, O(n√n) total).

```java
public boolean[] sieveOfEratosthenes(int n) {
    boolean[] isPrime = new boolean[n + 1];
    Arrays.fill(isPrime, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; (long) i * i <= n; i++) {
        if (isPrime[i]) {
            for (int multiple = i * i; multiple <= n; multiple += i) {
                isPrime[multiple] = false;
            }
        }
    }
    return isPrime;
}
```

**Why start marking at `i*i`, not `2*i`.** Every multiple of i smaller than `i*i` (`2i, 3i, ..., (i-1)i`) was already marked non-prime by some smaller prime factor by the time the outer loop reaches i (e.g., `6 = 2×3` was already marked when `i=2` ran). Starting at `i*i` skips this guaranteed-redundant work.

**Trace** on `n=30`: `i=2` marks `4,6,8,...,30`. `i=3` marks `9,12,...,30` (some already marked — harmless). `i=4`: already marked non-prime, skipped via the guard. `i=5` marks `25`. `i=6`: `6²=36 > 30` → loop ends. **Remaining primes:** `2,3,5,7,11,13,17,19,23,29` — matches the known list exactly. ✓

**Complexity:** O(n log log n) time, O(n) space.

### Modular Arithmetic

**What it solves.** Keeping intermediate results bounded when the true answer could be astronomically large (e.g., "count the ways, modulo 10⁹+7").

```
(a + b) % m = ((a % m) + (b % m)) % m
(a - b) % m = ((a % m) - (b % m) + m) % m     // +m guards against a negative result
(a * b) % m = ((a % m) * (b % m)) % m
```

**Why the `+m` guard matters specifically for subtraction.** In Java and C++, `%` can return a *negative* result when the left operand is negative (unlike Python, where `%` matches the divisor's sign). `(a%m) - (b%m)` can go negative even though the true result, modulo m, should sit in `[0, m-1]`. Adding `m` before the final `% m` shifts any negative intermediate back into range without changing its value modulo m.

Division is **not** simply `(a/b) % m` — it requires a modular multiplicative inverse (Fermat's Little Theorem when m is prime: `a⁻¹ ≡ a^(m-2) (mod m)`, via fast exponentiation), a topic that surfaces in modular-arithmetic-heavy combinatorics but is beyond this book's core scope. Worth knowing it exists, even without the full derivation here.

**Common mistake:** applying `% m` only at the very end of a long computation, after intermediate values have *already* overflowed. The entire point is reducing after every individual operation, not once at the end when it's too late.

---

## Common Mistakes — Chapter-Wide

- **Reaching for a segment tree when a Fenwick tree would do** — for sum-with-point-updates specifically, the Fenwick tree is shorter and faster in practice.
- **Forgetting the 1-indexed convention for Fenwick trees** — raw 0-indexing breaks the `index & (-index)` bit trick entirely.
- **Using a plain monotonic stack where a deque is needed** — anything requiring elements to expire by age (not just by a bigger element arriving) needs removal from both ends.
- **Computing actual floating-point operations when an integer bit trick would do the same job** — `n & (n-1)` for popcount or power-of-two checks is both simpler and faster.
- **Advancing the text pointer on a KMP mismatch instead of falling back via the failure function** — this degrades KMP straight back to naive O(n·m) matching.
- **Taking the modulo only at the end of a computation chain** instead of after every operation — by the time a single final `% m` runs, intermediate overflow has already happened.
- **Forgetting the `+m` guard when subtracting under a modulus** in Java/C++, producing an incorrectly negative result.

## Pattern Recognition Guide

- "Minimum/maximum value of a parameter, with a monotonic feasibility check" → binary search on the answer, regardless of the problem's surface domain.
- "Maximum/minimum of every sliding window" → monotonic deque, not a stack.
- "Range query with point updates, frequent interleaving" → segment tree (general aggregates) or Fenwick tree (sums specifically, simpler code).
- "Find the unique element where everything else is paired" → XOR.
- "Count set bits," "check power of two" → the `n & (n-1)` trick.
- "Find all occurrences of a pattern in a text, efficiently" → KMP's failure function.
- "Count the ways, modulo a large prime" → reduce after every operation; remember the `+m` guard for subtraction.
- "Find all primes up to n" → Sieve of Eratosthenes, marking from each prime's square.

## Chapter Summary

- Binary search on the answer is a genuinely general pattern — any monotonic feasibility check over a bounded parameter range qualifies, no matter how unrelated the problem's surface domain looks to "searching an array."
- A monotonic deque generalizes Chapter 4's monotonic stack to support removal from both ends — exactly what's needed when elements expire either by a bigger arrival or by simply aging out of a window.
- Segment trees answer range queries and point updates in O(log n) each; Fenwick trees solve the identical sum-specific case with simpler code, at the cost of needing a clean inverse operation rather than full generality.
- XOR's self-canceling property turns "find the one unpaired element" into one O(n), O(1)-space pass; `n & (n-1)` clears the lowest set bit, powering both popcount and power-of-two checks.
- KMP's failure function guarantees the text pointer never moves backward, which is exactly what brings string matching down from O(n·m) to O(n+m).
- GCD via the Euclidean algorithm, LCM derived from it, the Sieve's "start at i²" optimization, and modular arithmetic's "reduce after every operation" discipline round out the standard toolkit for counting and number-theoretic problems.

---

#### Advanced DSA — Complete Java Implementations

**Segment Tree — Full Implementation:**

```java
// A Segment Tree supports:
// - Point update: update a single element — O(log n)
// - Range query: sum/min/max over [l, r] — O(log n)
// Better than prefix sum when there are FREQUENT UPDATES
// (prefix sum update = O(n); Segment Tree update = O(log n))

// LeetCode #307 — Range Sum Query Mutable
// Time: build O(n), query O(log n), update O(log n)
// Space: O(n)

class NumArray {
    private int[] tree;  // segment tree stored as array
    private int n;

    public NumArray(int[] nums) {
        n = nums.length;
        tree = new int[2 * n];  // 2n nodes for n leaves
        // Build: fill leaves first (indices n to 2n-1)
        for (int i = 0; i < n; i++) tree[n + i] = nums[i];
        // Build internal nodes bottom-up
        for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }

    public void update(int index, int val) {
        // Update leaf
        tree[n + index] = val;
        // Propagate up to root
        int pos = n + index;
        while (pos > 1) {
            pos /= 2;  // parent index
            tree[pos] = tree[2 * pos] + tree[2 * pos + 1];
        }
    }

    public int sumRange(int left, int right) {
        // Convert to leaf indices; expand to next-level boundaries
        int l = left + n, r = right + n;
        int sum = 0;
        while (l <= r) {
            if (l % 2 == 1) sum += tree[l++];  // l is right child: add and move up
            if (r % 2 == 0) sum += tree[r--];  // r is left child: add and move up
            l /= 2;
            r /= 2;
        }
        return sum;
    }
}
```

**Binary Indexed Tree (Fenwick Tree) — Complete Implementation:**

```java
// Fenwick Tree: simpler code than Segment Tree for prefix sum queries.
// Prefix sum with updates: O(log n) for both operations.
// Preferred over Segment Tree when you only need prefix sums (not range min/max).

// LeetCode #315 — Count of Smaller Numbers After Self
// For each element, count how many elements to its RIGHT are smaller.
// Strategy: traverse RIGHT to LEFT, for each element query count(nums[i]-1)
// using a Fenwick Tree indexed by value.

class FenwickTree {
    private int[] tree;
    private int n;

    FenwickTree(int n) {
        this.n = n;
        tree = new int[n + 1];
    }

    // Add delta to position i (1-indexed)
    public void update(int i, int delta) {
        for (; i <= n; i += i & (-i))  // i & (-i) = lowest set bit of i
            tree[i] += delta;
    }

    // Query prefix sum [1..i]
    public int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & (-i))
            sum += tree[i];
        return sum;
    }

    // Query range sum [l..r]
    public int queryRange(int l, int r) {
        return query(r) - query(l - 1);
    }
}

public List<Integer> countSmaller(int[] nums) {
    // Coordinate compression: map values to 1..n range for Fenwick indexing
    int[] sorted = nums.clone();
    Arrays.sort(sorted);
    // sorted = [-1, 1, 2, 3] → we map -1→1, 1→2, 2→3, 3→4

    Map<Integer, Integer> rank = new HashMap<>();
    int r = 0;
    for (int v : sorted) rank.putIfAbsent(v, ++r);

    FenwickTree bit = new FenwickTree(nums.length);
    Integer[] result = new Integer[nums.length];

    // Traverse right to left
    for (int i = nums.length - 1; i >= 0; i--) {
        int mappedVal = rank.get(nums[i]);
        // Count elements already inserted with rank < mappedVal
        result[i] = mappedVal > 1 ? bit.query(mappedVal - 1) : 0;
        bit.update(mappedVal, 1);  // register current element
    }
    return Arrays.asList(result);
}
```

**KMP String Matching — Complete Implementation:**

```java
// Knuth-Morris-Pratt (KMP): find pattern in text in O(n + m)
// Naive: O(n × m) — resets comparison on every mismatch
// KMP: uses a failure function to skip redundant comparisons
//
// LeetCode #28 — Find the Index of the First Occurrence in a String

public int strStr(String haystack, String needle) {
    if (needle.isEmpty()) return 0;
    int n = haystack.length(), m = needle.length();

    // Build failure function (LPS array)
    // lps[i] = length of longest proper prefix of needle[0..i] that is also a suffix
    int[] lps = buildLPS(needle);

    int i = 0; // haystack pointer
    int j = 0; // needle pointer

    while (i < n) {
        if (haystack.charAt(i) == needle.charAt(j)) {
            i++;
            j++;
            if (j == m) return i - m; // found!
        } else if (j > 0) {
            // Mismatch after some matches: use LPS to avoid re-examining chars
            j = lps[j - 1]; // don't increment i
        } else {
            i++; // no match at all, advance text pointer
        }
    }
    return -1; // not found
}

private int[] buildLPS(String pattern) {
    int m = pattern.length();
    int[] lps = new int[m];
    int len = 0; // length of previous longest prefix-suffix
    int i = 1;

    while (i < m) {
        if (pattern.charAt(i) == pattern.charAt(len)) {
            lps[i++] = ++len;
        } else if (len > 0) {
            len = lps[len - 1]; // try shorter prefix
        } else {
            lps[i++] = 0;
        }
    }
    return lps;
}
// Example: needle = "AAACAAAA"
// lps =    [0,1,2,0,1,2,3,3]
// lps[2]=2 means "AA" is both a prefix and suffix of "AAA"
// When mismatch at i=3 with j=3: jump to lps[2]=2 (not j=0)
// This is what makes KMP O(n+m) instead of O(n×m)
```

**Bit Manipulation — Complete Pattern Library:**

```java
public class BitPatterns {

    // ─── Single Number (LeetCode #136) ─────────────────────────────────
    // Every element appears twice except one. Find the single element.
    // XOR trick: A^A=0, A^0=A → all pairs cancel, single remains
    // Time: O(n), Space: O(1)
    public int singleNumber(int[] nums) {
        int result = 0;
        for (int num : nums) result ^= num;
        return result;
    }

    // ─── Counting Bits (LeetCode #338) ─────────────────────────────────
    // For every number 0..n, count the number of 1-bits.
    // DP approach: dp[i] = dp[i >> 1] + (i & 1)
    // i >> 1 = i / 2 (one fewer bit to process)
    // i & 1 = the least significant bit of i
    // Time: O(n), Space: O(n)
    public int[] countBits(int n) {
        int[] dp = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            dp[i] = dp[i >> 1] + (i & 1);
        }
        return dp;
    }

    // ─── Hamming Weight (LeetCode #191) ────────────────────────────────
    // Count the number of '1' bits in an integer.
    // Brian Kernighan trick: n & (n-1) clears the lowest set bit
    // Time: O(k) where k = number of set bits, Space: O(1)
    public int hammingWeight(int n) {
        int count = 0;
        while (n != 0) {
            n &= (n - 1);  // clear lowest set bit
            count++;
        }
        return count;
    }

    // ─── Power of Two ───────────────────────────────────────────────────
    // Powers of 2 have exactly ONE set bit: 1=001, 2=010, 4=100, 8=1000
    // n & (n-1) clears that one bit → result is 0
    public boolean isPowerOfTwo(int n) {
        return n > 0 && (n & (n - 1)) == 0;
    }

    // ─── Bit manipulation helpers ───────────────────────────────────────
    public int getBit(int n, int pos)    { return (n >> pos) & 1; }
    public int setBit(int n, int pos)    { return n | (1 << pos); }
    public int clearBit(int n, int pos)  { return n & ~(1 << pos); }
    public int toggleBit(int n, int pos) { return n ^ (1 << pos); }

    // ─── Sieve of Eratosthenes (LeetCode #204) ─────────────────────────
    // Count primes less than n.
    // Time: O(n log log n), Space: O(n)
    public int countPrimes(int n) {
        boolean[] composite = new boolean[n]; // composite[i]=true means i is NOT prime
        int count = 0;
        for (int i = 2; i < n; i++) {
            if (!composite[i]) {
                count++;
                // Mark all multiples of i as composite
                // Start at i*i: smaller multiples already marked by previous primes
                for (long j = (long) i * i; j < n; j += i) {
                    composite[(int) j] = true;
                }
            }
        }
        return count;
    }

    // ─── Fast Power / Modular Exponentiation ────────────────────────────
    // Compute x^n mod MOD in O(log n)
    // Used when result must be returned modulo 10^9+7
    private static final long MOD = 1_000_000_007L;

    public long powMod(long base, long exp, long mod) {
        long result = 1;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1) == 1) result = result * base % mod;
            base = base * base % mod;
            exp >>= 1;
        }
        return result;
    }

    // LeetCode #50 — Pow(x, n) (handles negative n)
    public double myPow(double x, int n) {
        long N = n;
        if (N < 0) { x = 1 / x; N = -N; }
        double result = 1.0;
        while (N > 0) {
            if ((N & 1) == 1) result *= x;
            x *= x;
            N >>= 1;
        }
        return result;
    }
}
```
