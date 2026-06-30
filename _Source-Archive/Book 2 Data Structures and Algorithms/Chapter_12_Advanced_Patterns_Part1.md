# Chapter 12: Advanced Patterns
## Part 1 — Binary Search Revisited · Monotonic Deque · Segment Trees

*This chapter is a different shape from the rest of the book: fewer LeetCode problems, more standalone techniques worth having in your pocket. Each one earns its place by solving something the earlier chapters' tools genuinely can't.*

## 12.1 Binary Search, Revisited

Chapter 2 already built the full toolkit — standard search, first/last occurrence, rotated arrays, and binary search on the answer (Koko Eating Bananas). One thing worth adding here: "binary search on the answer" generalizes far beyond eating speeds. Any time a problem asks for the minimum or maximum value of some parameter, and a `feasible(value)` check exists that's monotonic — true above some threshold, false below it, or vice versa — binary search applies, no matter how unrelated the problem's surface domain looks to "searching an array."

**A second domain, to prove the point — Capacity to Ship Packages Within D Days (LeetCode 1011).** Given package weights and `D` days, find the minimum ship capacity such that every package ships within `D` days (packages load in order; a day's load can't exceed capacity).

This is mechanically identical to Koko Eating Bananas — only the feasibility check changes:

```java
public int shipWithinDays(int[] weights, int days) {
    int lo = 0, hi = 0;
    for (int w : weights) { lo = Math.max(lo, w); hi += w; }   // lo must fit the heaviest package alone

    int result = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (canShip(weights, mid, days)) {
            result = mid;
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }
    return result;
}

private boolean canShip(int[] weights, int capacity, int days) {
    int daysNeeded = 1, currentLoad = 0;
    for (int w : weights) {
        if (currentLoad + w > capacity) {
            daysNeeded++;
            currentLoad = 0;
        }
        currentLoad += w;
    }
    return daysNeeded <= days;
}
```

Same `lo`/`hi`/`result` bookkeeping, same "found a valid answer, search left for something tighter" logic as Koko — the only thing that changed is what the feasibility check actually checks. That's the entire value of recognizing this as a pattern rather than memorizing each problem in isolation.

---

## Pattern — Monotonic Deque: Sliding Window Maximum

### Problem — Sliding Window Maximum (LeetCode 239)

**Statement.** Given an array and window size k, return the maximum of every window of size k as it slides left to right.

**Why the obvious approach is too slow.** Recomputing each window's max from scratch costs O(k) per window, O(nk) total.

**Approach — a deque, not a stack.** Maintain a deque of *indices*, kept so their *values* are strictly decreasing from front to back — the front always holds the index of the current window's maximum. For each new index `i`: first, pop from the **back** any index whose value is `≤ nums[i]` (it can never be the max again — `nums[i]` is both later and at least as large, so it dominates for the rest of that index's relevance); then push `i` onto the back. Next, pop from the **front** if that index has aged out of the current window. The front is now the current window's max.

This generalizes Chapter 4's monotonic stack to a **deque** — popping from *both* ends, because elements now need to expire for two different reasons: a bigger element arriving (back of the deque) and simply aging out of the window (front of the deque). A plain stack can only ever pop from one end, which is exactly why it can't handle the "aged out" case.

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    Deque<Integer> deque = new ArrayDeque<>();   // indices, values strictly decreasing front-to-back
    int[] result = new int[nums.length - k + 1];
    int resultIdx = 0;

    for (int i = 0; i < nums.length; i++) {
        while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[i]) {
            deque.pollLast();                          // can never be the max again
        }
        deque.offerLast(i);

        if (deque.peekFirst() <= i - k) {
            deque.pollFirst();                          // aged out of the window
        }

        if (i >= k - 1) {
            result[resultIdx++] = nums[deque.peekFirst()];
        }
    }
    return result;
}
```

**Trace** on `nums=[1,3,-1,-3,5,3,6,7]`, `k=3`:

```
i=0 (1): deque=[0]
i=1 (3): back(0,val1)≤3 → pop.  deque=[1]
i=2 (-1): back(1,val3) not ≤-1 → keep.  deque=[1,2]  → window full → record nums[1]=3
i=3 (-3): back(2,val-1) not ≤-3 → keep.  deque=[1,2,3]  → record nums[1]=3
i=4 (5): pop 3(val-3), pop 2(val-1), pop 1(val3) — all ≤5.  deque=[4]  → record nums[4]=5
i=5 (3): back(4,val5) not ≤3 → keep.  deque=[4,5]  → record nums[4]=5
i=6 (6): pop 5(val3), pop 4(val5) — both ≤6.  deque=[6]  → record nums[6]=6
i=7 (7): pop 6(val6) ≤7.  deque=[7]  → record nums[7]=7

Final: [3,3,5,5,6,7]
```

**Verify:** windows are `[1,3,-1]→3`, `[3,-1,-3]→3`, `[-1,-3,5]→5`, `[-3,5,3]→5`, `[5,3,6]→6`, `[3,6,7]→7`. Matches exactly. ✓

**Complexity:** O(n) — each index is pushed once and popped at most once across both ends combined, the identical amortized argument as Chapter 4's monotonic stack. Space O(k) for the deque.

**Common mistake:** reaching for a plain (single-ended) monotonic stack instead of a deque. A stack can't efficiently expire the *oldest* element when it ages out of the window — only a structure supporting removal from both ends can do that in O(1).

---

## Segment Trees

### What They Solve, and When to Use One Instead of a Prefix Sum

Range queries (sum/min/max over a sub-range) **with point updates** (changing a single element). Prefix sums answer range-sum queries in O(1), but a single update forces rebuilding the entire prefix array — O(n), since every prefix sum from the updated index onward shifts. A segment tree answers range queries in O(log n) *and* handles point updates in O(log n) — strictly worse per-query than prefix sum's O(1), but dramatically better the moment updates are frequent, since prefix sum's O(n) update cost becomes the bottleneck as soon as updates happen at all regularly.

**The rule of thumb:** static array, no updates → prefix sum, O(1) query, no update cost to worry about. Frequent updates interleaved with queries → segment tree (or a Fenwick tree, next section), O(log n) for both operations.

### Structure

A segment tree is a binary tree where each node represents a *range* of the original array and stores an aggregate (sum, min, max, ...) over that range. The root covers the entire array; each node's two children split its range in half; leaves represent single elements. Stored as an array — the same index-arithmetic trick as Chapter 7's binary heap — conventionally sized `4n` to comfortably hold a complete tree regardless of n's exact value (a tighter bound exists, but `4n` is the standard safe choice).

```java
class SegmentTree {
    int[] tree;
    int n;

    SegmentTree(int[] nums) {
        n = nums.length;
        tree = new int[4 * n];
        build(nums, 0, 0, n - 1);
    }

    private void build(int[] nums, int node, int start, int end) {
        if (start == end) {
            tree[node] = nums[start];
            return;
        }
        int mid = (start + end) / 2;
        build(nums, 2 * node + 1, start, mid);
        build(nums, 2 * node + 2, mid + 1, end);
        tree[node] = tree[2 * node + 1] + tree[2 * node + 2];   // combine (sum, here)
    }

    void update(int index, int value) {
        update(0, 0, n - 1, index, value);
    }

    private void update(int node, int start, int end, int index, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }
        int mid = (start + end) / 2;
        if (index <= mid) {
            update(2 * node + 1, start, mid, index, value);
        } else {
            update(2 * node + 2, mid + 1, end, index, value);
        }
        tree[node] = tree[2 * node + 1] + tree[2 * node + 2];   // recombine on the way back up
    }

    int query(int left, int right) {
        return query(0, 0, n - 1, left, right);
    }

    private int query(int node, int start, int end, int left, int right) {
        if (right < start || end < left) return 0;            // no overlap — contributes nothing
        if (left <= start && end <= right) return tree[node];  // fully covered — use this node directly
        int mid = (start + end) / 2;
        int leftSum = query(2 * node + 1, start, mid, left, right);
        int rightSum = query(2 * node + 2, mid + 1, end, left, right);
        return leftSum + rightSum;   // partially covered — combine both children's contributions
    }
}
```

**Build trace** on `nums=[1,3,5,7,9,11]`:

```
Leaves: tree[7]=1, tree[8]=3, tree[4]=5, tree[11]=7, tree[12]=9, tree[6]=11
tree[3]=tree[7]+tree[8]=1+3=4        (covers indices 0-1)
tree[1]=tree[3]+tree[4]=4+5=9         (covers indices 0-2)
tree[5]=tree[11]+tree[12]=7+9=16      (covers indices 3-4)
tree[2]=tree[5]+tree[6]=16+11=27      (covers indices 3-5)
tree[0]=tree[1]+tree[2]=9+27=36       (covers indices 0-5)

Sanity check: 1+3+5+7+9+11 = 36 = tree[0]   ✓
```

**Query trace** — `query(1, 4)`, expecting `3+5+7+9=24`:

```
node0 [0,5]: partial overlap with [1,4] → split
  node1 [0,2]: partial → split
    node3 [0,1]: partial → split
      node7 [0,0]: entirely before [1,4] → contributes 0
      node8 [1,1]: fully inside [1,4] → return tree[8]=3
    = 3
    node4 [2,2]: fully inside [1,4] → return tree[4]=5
  = 3+5 = 8
  node2 [3,5]: partial → split
    node5 [3,4]: fully inside [1,4] → return tree[5]=16
    node6 [5,5]: entirely after [1,4] → contributes 0
  = 16+0 = 16
= 8+16 = 24   ✓
```

**Update trace** — `update(2, 100)` (change index 2 from 5 to 100):

```
node0 → index2 ≤ mid(2) → recurse left into node1
node1 → index2 ≤ mid(1)? No → recurse right into node4
node4 (leaf, start==end==2): tree[4] = 100

Recombine on the way back up:
tree[1] = tree[3] + tree[4] = 4 + 100 = 104
tree[0] = tree[1] + tree[2] = 104 + 27 = 131

Verify: array is now [1,3,100,7,9,11], sum = 131 = tree[0]   ✓
```

**Complexity:** build O(n). update O(log n) — one path from root to a leaf. query O(log n) — at each level, at most a constant number of nodes are "partial," and every other node returns in O(1) as either fully-covered or fully-excluded (the full rigorous proof is beyond this book's scope, but O(log n) is the standard, well-established result). Space O(n) (the `4n`-sized array).

---

*Part 2 covers the Fenwick Tree (Binary Indexed Tree) as a simpler alternative for prefix-sum-with-updates, the core bit manipulation tricks, KMP string matching, and the standard math patterns — closing with the chapter-wide wrap-up.*
