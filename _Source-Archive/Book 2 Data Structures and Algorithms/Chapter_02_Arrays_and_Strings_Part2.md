# Chapter 2: Arrays and Strings
## Part 2 — Prefix Sum · Kadane's Algorithm · Binary Search (5 Variants)

---

## Pattern 5 — Prefix Sum

### Intuition

You have an array and need to answer range sum queries: "what is the sum of elements from index i to j?" Naively you scan from i to j: O(j−i+1) per query, O(n) worst case. If there are q queries, that's O(nq) total — quadratic if q scales with n.

The prefix sum insight: **precompute** the cumulative sum at every index once in O(n), then answer any range query in O(1) with a subtraction.

Define `prefix[i]` = sum of `arr[0..i-1]` (using a 1-indexed prefix array where `prefix[0] = 0`).

Then: `sum(i, j)` = `prefix[j+1] - prefix[i]`

```
arr:    [3,  1,  4,  1,  5,  9,  2]
index:   0   1   2   3   4   5   6

prefix[0] = 0
prefix[1] = 0 + 3 = 3
prefix[2] = 3 + 1 = 4
prefix[3] = 4 + 4 = 8
prefix[4] = 8 + 1 = 9
prefix[5] = 9 + 5 = 14
prefix[6] = 14 + 9 = 23
prefix[7] = 23 + 2 = 25

sum(2, 5) = prefix[6] - prefix[2] = 23 - 4 = 19
Check: arr[2]+arr[3]+arr[4]+arr[5] = 4+1+5+9 = 19 ✓
```

### Template

```java
// Build prefix sum array (size n+1 to avoid off-by-one handling)
public int[] buildPrefix(int[] arr) {
    int n = arr.length;
    int[] prefix = new int[n + 1];
    for (int i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
    return prefix;
}

// Query: sum of arr[i..j] inclusive
public int rangeSum(int[] prefix, int i, int j) {
    return prefix[j + 1] - prefix[i];
}
```

---

### Problem 5.1 — Range Sum Query (LeetCode 303)

**Statement.** Given an integer array `nums`, implement `NumArray` with a `sumRange(left, right)` method that returns the sum of elements from index `left` to `right` inclusive. `sumRange` will be called multiple times.

**Full Solution:**

```java
class NumArray {
    private int[] prefix;

    public NumArray(int[] nums) {
        prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }

    public int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
}
```

**Complexity:** Constructor O(n). `sumRange` O(1). Space O(n) for the prefix array.

---

### Problem 5.2 — Subarray Sum Equals K (LeetCode 560)

**Statement.** Given an integer array `nums` and an integer `k`, return the number of contiguous subarrays whose sum equals `k`.

This problem cannot be solved with a standard sliding window because the array may contain negative numbers (you can't decide whether to expand or shrink based on sum alone). It uses the prefix sum plus a HashMap — the most important prefix sum pattern.

**Key insight.** `sum(i, j) = k` iff `prefix[j+1] - prefix[i] = k` iff `prefix[i] = prefix[j+1] - k`.

So for each position j+1 with prefix sum `curr`, we want to count how many *previous* positions had prefix sum `curr - k`. We've already seen those — count them in a HashMap as we scan left to right.

**Trace** on `nums = [1, 2, 3]`, `k = 3`:

```
HashMap starts as {0: 1}  ← prefix sum of 0 (empty array) appears once
curr = 0, count = 0

i=0: curr = 0+1 = 1. Looking for curr-k = 1-3 = -2. Not in map. count stays 0.
     map = {0:1, 1:1}

i=1: curr = 1+2 = 3. Looking for curr-k = 3-3 = 0. In map with count 1. count = 1.
     This corresponds to subarray nums[0..1] = [1,2] sum=3 ✓
     map = {0:1, 1:1, 3:1}

i=2: curr = 3+3 = 6. Looking for curr-k = 6-3 = 3. In map with count 1. count = 2.
     This corresponds to subarray nums[2..2] = [3] sum=3 ✓
     map = {0:1, 1:1, 3:1, 6:1}

Answer: 2  ([1,2] and [3])  ✓
Also valid: is there a [1,2,3] subarray with sum=6? That's k=6, different problem.
Wait — also check [1,2,3] with k=3? No: 1+2+3=6 ≠ 3. Count=2 is correct.
```

**Why we initialize the map with {0: 1}.** The prefix sum before any element is 0. If a subarray starting from index 0 sums to exactly k, then `curr - k = 0`, and we need to find that 0 in the map. Without the initialization, subarrays starting from index 0 would never be counted.

**Full Solution:**

```java
public int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> prefixCount = new HashMap<>();
    prefixCount.put(0, 1);   // empty prefix — critical initialization
    int curr = 0, count = 0;
    for (int num : nums) {
        curr += num;
        // How many previous prefixes sum to (curr - k)?
        count += prefixCount.getOrDefault(curr - k, 0);
        prefixCount.merge(curr, 1, Integer::sum);
    }
    return count;
}
```

**Complexity:** Time O(n). Space O(n) for the HashMap.

---

### Problem 5.3 — Product of Array Except Self (LeetCode 238)

**Statement.** Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of all elements except `nums[i]`. You may not use division. O(n) time, O(1) auxiliary space (the output array doesn't count).

**Approach.** Think of `answer[i]` as the product of everything to the *left* of i multiplied by the product of everything to the *right* of i. Compute the left products in one left-to-right pass, then multiply in the right products in one right-to-left pass.

```
nums = [1, 2, 3, 4]

Left products (answer[i] = product of nums[0..i-1]):
answer = [1, 1, 2, 6]
  answer[0] = 1 (nothing to the left)
  answer[1] = 1
  answer[2] = 1 * 2 = 2
  answer[3] = 1 * 2 * 3 = 6

Right pass: maintain running right product, multiply into answer right to left:
right = 1
i=3: answer[3] = answer[3]*right = 6*1=6.  right = right*nums[3] = 1*4 = 4.
i=2: answer[2] = answer[2]*right = 2*4=8.  right = right*nums[2] = 4*3 = 12.
i=1: answer[1] = answer[1]*right = 1*12=12. right = right*nums[1] = 12*2 = 24.
i=0: answer[0] = answer[0]*right = 1*24=24. right = right*nums[0] = 24*1 = 24.

answer = [24, 12, 8, 6]  ✓
Check: 2*3*4=24, 1*3*4=12, 1*2*4=8, 1*2*3=6 ✓
```

**Full Solution:**

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] answer = new int[n];

    // Left pass: answer[i] = product of all elements to the left of i
    answer[0] = 1;
    for (int i = 1; i < n; i++) {
        answer[i] = answer[i - 1] * nums[i - 1];
    }

    // Right pass: multiply in product of all elements to the right of i
    int right = 1;
    for (int i = n - 1; i >= 0; i--) {
        answer[i] *= right;
        right *= nums[i];
    }
    return answer;
}
```

**Complexity:** Time O(n). Space O(1) auxiliary (the `answer` array is the output, not counted; the `right` variable is O(1)).

**Pattern Recognition — Prefix Sum:**
- "Sum of subarray from i to j" → build prefix array, O(1) queries.
- "Number of subarrays with sum equals k (possibly with negatives)" → prefix sum + HashMap.
- "Product except self, no division" → left-pass product array + right-pass running product.
- The unifying idea: precompute accumulated state left-to-right (or right-to-left) once, then answer queries in O(1) by subtracting or dividing out the prefix.

---

## 2.6 Kadane's Algorithm — Maximum Subarray Sum

### Intuition

**Problem (LeetCode 53).** Given an integer array `nums`, find the contiguous subarray with the largest sum and return its sum.

Brute force tests every pair (i, j) — O(n²) with the prefix sum optimization, O(n³) naively. Kadane's runs in O(n) with O(1) space by asking a different question at each position:

> "Is it worth continuing the current subarray, or better to start fresh here?"

At each index i, the maximum subarray ending *exactly* at i is either:
- `nums[i]` alone (start fresh — the previous subarray was dragging us down, i.e., had negative sum)
- `maxEndingHere + nums[i]` (extend the previous best — it was positive, worth keeping)

Which one? Whichever is larger:

```
maxEndingHere = max(nums[i], maxEndingHere + nums[i])
```

The global answer is the maximum `maxEndingHere` seen across all positions.

**Trace** on `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`:

```
i=0: maxEndingHere = max(-2, -2)       = -2.  maxSoFar = -2.
i=1: maxEndingHere = max(1, -2+1=-1)   =  1.  maxSoFar =  1.
i=2: maxEndingHere = max(-3, 1-3=-2)   = -2.  maxSoFar =  1.
i=3: maxEndingHere = max(4, -2+4=2)    =  4.  maxSoFar =  4.
i=4: maxEndingHere = max(-1, 4-1=3)    =  3.  maxSoFar =  4.
i=5: maxEndingHere = max(2, 3+2=5)     =  5.  maxSoFar =  5.
i=6: maxEndingHere = max(1, 5+1=6)     =  6.  maxSoFar =  6.
i=7: maxEndingHere = max(-5, 6-5=1)    =  1.  maxSoFar =  6.
i=8: maxEndingHere = max(4, 1+4=5)     =  5.  maxSoFar =  6.

Answer: 6  (subarray [4, -1, 2, 1])  ✓
```

**Full Solution:**

```java
public int maxSubArray(int[] nums) {
    int maxEndingHere = nums[0];
    int maxSoFar = nums[0];
    for (int i = 1; i < nums.length; i++) {
        maxEndingHere = Math.max(nums[i], maxEndingHere + nums[i]);
        maxSoFar = Math.max(maxSoFar, maxEndingHere);
    }
    return maxSoFar;
}
```

**Complexity:** Time O(n). Space O(1).

**Common mistake:** Initializing `maxSoFar = 0`. This is wrong when all elements are negative — the correct answer is the least negative element (e.g., for `[-3, -1, -2]` the answer is `-1`, not 0). Initialize both to `nums[0]`.

**Pattern Recognition — Kadane's:**
- "Maximum subarray sum" → Kadane's directly.
- "Maximum product subarray" → Kadane's variant where you track both max and min (because multiplying two negatives can flip to a max).
- Any problem that asks "best contiguous subarray ending here" decomposition → Kadane's framework.

---

## 2.7 Binary Search — Five Variants

Binary search looks deceptively simple — halve the search space each step — but the edge cases on loop conditions and pointer updates cause most candidates to write incorrect code under pressure. The key is to have one precise template per variant and know exactly which condition changes between them.

### Variant 1 — Standard Binary Search

**Find target in sorted array. Return index or -1.**

**Template:**

```java
public int binarySearch(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;    // avoids integer overflow vs (lo+hi)/2
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}
```

**Why `lo + (hi - lo) / 2` instead of `(lo + hi) / 2`?** If `lo` and `hi` are both near `Integer.MAX_VALUE`, their sum overflows to a negative number. The subtraction form never overflows because `hi - lo >= 0` and the result fits in an int. Write it correctly every time without thinking.

**Loop invariant:** The target, if present, is always within `[lo, hi]`. When `lo > hi`, the search space is empty — target not found.

**Trace** on `nums = [1,3,5,7,9]`, `target = 7`:

```
lo=0 hi=4: mid=2. nums[2]=5 < 7 → lo=3.
lo=3 hi=4: mid=3. nums[3]=7 == 7 → return 3. ✓
```

---

### Variant 2 — Find First Occurrence (Left-Biased Binary Search)

**Find the first (leftmost) index of target. Return -1 if not found.**

The key change: when `nums[mid] == target`, don't return immediately — record the position and keep searching *left* for an earlier occurrence.

```java
public int findFirst(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    int result = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) {
            result = mid;       // record, but keep searching left
            hi = mid - 1;
        } else if (nums[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return result;
}
```

**Trace** on `nums = [1,2,2,2,3]`, `target = 2`:

```
lo=0 hi=4: mid=2. nums[2]=2 == 2 → result=2, hi=1.
lo=0 hi=1: mid=0. nums[0]=1 < 2 → lo=1.
lo=1 hi=1: mid=1. nums[1]=2 == 2 → result=1, hi=0.
lo=1 hi=0: lo>hi, stop. Return 1. ✓ (first occurrence is index 1)
```

---

### Variant 3 — Find Last Occurrence (Right-Biased Binary Search)

Mirror of Variant 2: when equal, record and keep searching *right*.

```java
public int findLast(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    int result = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) {
            result = mid;       // record, but keep searching right
            lo = mid + 1;
        } else if (nums[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return result;
}
```

**LeetCode 34 — Find First and Last Position in Sorted Array** uses exactly these two variants back-to-back:

```java
public int[] searchRange(int[] nums, int target) {
    return new int[]{findFirst(nums, target), findLast(nums, target)};
}
```

**Complexity of both:** Time O(log n). Space O(1).

---

### Variant 4 — Search in Rotated Sorted Array (LeetCode 33)

**Statement.** A sorted array was rotated at some unknown pivot. Find `target`. Return its index or -1.

Example: `[4,5,6,7,0,1,2]` is `[0,1,2,3,4,5,6]` rotated at index 3.

**Key insight.** Even in a rotated array, splitting at `mid` always produces at least one *sorted half*. Specifically:
- If `nums[lo] <= nums[mid]`, the left half `[lo, mid]` is sorted.
- Otherwise, the right half `[mid, hi]` is sorted.

For the sorted half, you can check in O(1) whether `target` lies within it. If it does, search that half; otherwise, search the other half.

**Trace** on `nums = [4,5,6,7,0,1,2]`, `target = 0`:

```
lo=0 hi=6: mid=3. nums[0]=4 <= nums[3]=7 → left half [4,5,6,7] is sorted.
  Is target=0 in [4..7]? No. Search right half: lo=4.

lo=4 hi=6: mid=5. nums[4]=0 <= nums[5]=1 → left half [0,1] is sorted.
  Is target=0 in [0..1]? Yes (0 >= nums[4]=0 and 0 <= nums[5]=1). Search left half: hi=5.

lo=4 hi=5: mid=4. nums[4]=0 == 0 → return 4. ✓
```

**Full Solution:**

```java
public int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;

        if (nums[lo] <= nums[mid]) {
            // Left half is sorted
            if (nums[lo] <= target && target < nums[mid]) {
                hi = mid - 1;   // target in sorted left half
            } else {
                lo = mid + 1;   // target in right half
            }
        } else {
            // Right half is sorted
            if (nums[mid] < target && target <= nums[hi]) {
                lo = mid + 1;   // target in sorted right half
            } else {
                hi = mid - 1;   // target in left half
            }
        }
    }
    return -1;
}
```

**Complexity:** Time O(log n). Space O(1).

**Common mistake:** Using `<` instead of `<=` in `nums[lo] <= nums[mid]`. The `=` case handles when `lo == mid` (a 2-element array). Without it, some edge cases silently fall into the wrong branch.

---

### Variant 5 — Binary Search on the Answer (Koko Eating Bananas — LeetCode 875)

This is the advanced pattern that expands binary search beyond "find a value in a sorted array" to "find the optimal value of a parameter."

**Statement.** Koko has piles of bananas `piles[i]`. She can eat `k` bananas per hour. She must finish all piles in `h` hours (eating one pile per hour, taking a full hour for any partial pile). Find the minimum `k` such that she can finish in time.

**Why binary search?** The relationship between `k` and feasibility is monotonic: if she can finish at speed `k`, she can also finish at any speed `k' > k`. If she can't finish at speed `k`, she can't finish at any speed `k' < k` either. This monotonicity means there's a clean threshold: everything to its right is "too fast but valid," everything to its left is "too slow and invalid." Binary search finds that threshold in O(log(max)) time.

**The general pattern:**
1. Identify the answer space (here: `k` ranges from 1 to `max(piles)`).
2. Write a `canFinish(k)` function — O(n) to check feasibility.
3. Binary search the answer space, keeping the tightest valid answer seen so far.

**Trace** on `piles = [3,6,7,11]`, `h = 8`:

```
Answer space: k ∈ [1, 11]
lo=1, hi=11.

mid=6. canFinish(6)?
  ceil(3/6)=1, ceil(6/6)=1, ceil(7/6)=2, ceil(11/6)=2. Total=6 <= 8. YES.
  result=6. Search left: hi=5.

lo=1 hi=5: mid=3. canFinish(3)?
  ceil(3/3)=1, ceil(6/3)=2, ceil(7/3)=3, ceil(11/3)=4. Total=10 > 8. NO.
  Search right: lo=4.

lo=4 hi=5: mid=4. canFinish(4)?
  ceil(3/4)=1, ceil(6/4)=2, ceil(7/4)=2, ceil(11/4)=3. Total=8 <= 8. YES.
  result=4. Search left: hi=3.

lo=4 hi=3: lo>hi. Stop. Return result=4. ✓
```

**Full Solution:**

```java
public int minEatingSpeed(int[] piles, int h) {
    int lo = 1, hi = 0;
    for (int pile : piles) hi = Math.max(hi, pile);  // max of piles

    int result = hi;  // worst case: eat fastest pile's count per hour
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (canFinish(piles, mid, h)) {
            result = mid;   // valid — record and try slower (search left)
            hi = mid - 1;
        } else {
            lo = mid + 1;   // too slow — must go faster
        }
    }
    return result;
}

private boolean canFinish(int[] piles, int k, int h) {
    int hours = 0;
    for (int pile : piles) {
        hours += (pile + k - 1) / k;  // ceiling division: ceil(pile/k)
    }
    return hours <= h;
}
```

**Why `(pile + k - 1) / k` for ceiling division?** In Java, integer division truncates (floor). The ceiling of `a/b` in integers is `(a + b - 1) / b`. You'll use this trick constantly. Alternatively, `(int) Math.ceil((double) pile / k)` works but is slower and has floating-point edge cases.

**Complexity:** Time O(n log(max(piles))). Space O(1).

**The "Binary Search on the Answer" Recognition Checklist:**
1. You're asked for a minimum/maximum value of some parameter.
2. The feasibility function is monotonic: above some threshold, always feasible; below it, never (or vice versa).
3. The parameter's range is known and bounded.
4. You can check feasibility in polynomial time (usually O(n) or O(n log n)).

Examples you'll encounter: Capacity to Ship Within D Days (same as Koko), Minimum Number of Days to Make m Bouquets, Split Array Largest Sum, Find K-th Smallest Pair Distance — all use this identical structure.

---

## Chapter 2 Summary

**What you built in this chapter:**

Five two-pointer / window patterns, one accumulation pattern, one greedy pattern, and one metapattern that expands binary search to any monotonic optimisation:

| Pattern | What it solves | Complexity |
|---|---|---|
| Two Pointers (Opposite) | Pair/triplet search in sorted arrays | O(n) after O(n log n) sort |
| Two Pointers (Same Direction) | In-place partition/filter | O(n) time, O(1) space |
| Sliding Window (Fixed) | Subarray aggregate of size k | O(n) |
| Sliding Window (Variable) | Longest/shortest subarray satisfying condition | O(n) |
| Prefix Sum | Range queries, subarray sum = k | O(n) build, O(1) query |
| Kadane's | Maximum subarray sum | O(n) |
| Binary Search (5 variants) | Sorted search, rotated arrays, answer-space search | O(log n) to O(n log n) |

**Master Pattern Recognition:**

- Sorted array + pair/triple satisfying condition → Two Pointers Opposite
- In-place partition, filter preserving order → Two Pointers Same Direction
- "Subarray of exactly k elements" → Fixed Sliding Window
- "Longest/shortest window where [condition]" → Variable Sliding Window
- "Range sum query" or "subarray sum = k" → Prefix Sum (+ HashMap for the k-sum variant)
- "Max subarray sum" → Kadane's
- Sorted array, search → Binary Search (choose variant based on first/last/any)
- "Find minimum k such that..." where feasibility is monotonic → Binary Search on Answer

**Common Mistakes — Chapter-Wide:**

1. **Two Pointers on unsorted array** without sorting first. Opposite-end two pointers require sorted order. If the problem gives you an unsorted array, sort it first (and count that O(n log n) cost).
2. **Not handling the {0:1} initialization in the Subarray Sum = K map.** Subarrays starting at index 0 are always missed without it.
3. **Initializing Kadane's maxSoFar to 0.** Wrong when all elements are negative.
4. **Integer overflow in binary search.** Always write `lo + (hi - lo) / 2`, never `(lo + hi) / 2`.
5. **Missing the `>= left` guard** in Longest Substring Without Repeating Characters's lastSeen check.
6. **Forgetting ceiling division** in binary-search-on-answer feasibility checks. `(a + b - 1) / b`, not `a / b`.
