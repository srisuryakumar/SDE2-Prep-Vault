# Chapter 2: Arrays and Strings
## Part 1 — Fundamentals · Two Pointers · Sliding Window

*This is the largest chapter in the book, split across two files. Part 1 covers the array/string memory model, both two-pointer patterns, and both sliding-window patterns — five patterns total, fourteen solved problems. Part 2 covers prefix sums, Kadane's algorithm, and five binary search variants.*

---

## 2.1 Array Memory Layout

An array is the simplest possible data structure: a contiguous block of memory where every element occupies exactly the same number of bytes.

```
int[] arr = {10, 30, 50, 70, 90};

Memory (each int = 4 bytes):
Address:  1000  1004  1008  1012  1016
Value:    [10]  [30]  [50]  [70]  [90]
Index:      0     1     2     3     4
```

Because the block is contiguous and every slot is the same size, the address of element `i` is always:

```
address(i) = baseAddress + i * elementSize
```

This formula requires *one multiplication and one addition* regardless of i — the same two operations whether you're accessing index 0 or index 999,999. That's why array random access is O(1): the time to find any element is completely independent of the array's size.

**What you pay for that O(1) access:** the array cannot grow. Java arrays are fixed-size at allocation. If you need `arr[n+1]`, you allocate a new, larger array and copy everything over — O(n) work. `ArrayList` automates that behind the scenes (with the amortized O(1) analysis from Chapter 1), but the underlying reason it works is that every access into the backing array is still O(1).

**Cache locality.** Because the elements live at consecutive addresses, when the CPU fetches `arr[0]` it pulls an entire cache line (typically 64 bytes = 16 ints) into fast L1 cache all at once. Subsequent accesses to `arr[1]` through `arr[15]` hit L1 cache — effectively free. This is the invisible performance advantage of arrays over linked lists (Chapter 3) for sequential traversal, and it's why array-based algorithms are almost always faster in practice than their Big-O alone would predict.

**Insertion and deletion are O(n).** To insert a new element at index k, every element from index k to n−1 must shift one position right to make room. In the worst case (inserting at index 0), that's n shifts — O(n). Same analysis for deletion in reverse.

---

## 2.2 String Immutability in Java

Java `String` objects are immutable — once created, their underlying `char[]` can never change. The "string modification" methods you know (`substring`, `toLowerCase`, `replace`, `+`) don't modify the existing string. They allocate a brand-new `String` object and return it.

```java
String s = "hello";
s = s + " world";   // "hello" still exists in memory unchanged.
                     // A new String "hello world" was allocated.
                     // 's' now points to the new one.
                     // The old one becomes eligible for GC.
```

**Why this is fine most of the time.** In modern Java, string literals are interned (shared from a constant pool), and the JIT is good at optimizing simple concatenation. For occasional single concatenations, `+` is completely acceptable.

**Why this is catastrophically wrong in a loop.** Each `s = s + newPiece` allocates and copies the entire current contents of s into a new object. If you're building a string of length n by appending one character at a time:

```java
// BAD: O(n²) total work
String result = "";
for (int i = 0; i < n; i++) {
    result += chars[i];   // allocates and copies result each time
}
```

The sequence of copies is: 0 chars, then 1 char, then 2 chars, then 3 chars, ..., then n−1 chars. That's 0+1+2+...+(n−1) = n(n−1)/2 total character copies — **O(n²)**.

For n = 100,000 characters that's 5 billion character copies just to build the string. This is the single most common performance bug in Java string code.

**The fix: StringBuilder.** `StringBuilder` is backed by a resizable `char[]`. `append()` copies only the new characters into the buffer, not the entire existing content. When the buffer fills, it resizes (doubling, amortized O(1) per append). The final `toString()` does exactly one copy of the final content.

```java
// GOOD: O(n) total work
StringBuilder sb = new StringBuilder();
for (int i = 0; i < n; i++) {
    sb.append(chars[i]);   // O(1) amortized — appends only the new char
}
String result = sb.toString();   // one O(n) copy at the end
```

Total copies: n appends (O(1) amortized each) + one final O(n) copy = **O(n)**. Know this. Apply it. It comes up in easy and medium problems constantly.

---

## Pattern 1 — Two Pointers (Opposite Ends)

### Intuition

You have a sorted array and need to find a pair (or triple, or window) satisfying some condition. The brute-force approach tests every pair in O(n²). The two-pointer approach exploits **sorted order to make every comparison informative**: if the current pair's sum is too small, you know every pair involving the left pointer is also too small (because moving left only makes sums smaller), so you can eliminate an entire column of pairs in one step by advancing the left pointer. If the sum is too large, the same logic in reverse — you advance the right pointer. The search space collapses to O(n) total movements.

**The core invariant:** left pointer always points to the smallest remaining candidate; right pointer always points to the largest. When they meet, every pair has been considered (either directly tested or logically eliminated).

### Template

```java
public static void twoPointersOppEnds(int[] sorted) {
    int left = 0, right = sorted.length - 1;
    while (left < right) {
        // Compute something involving sorted[left] and sorted[right]
        int value = sorted[left] + sorted[right]; // example: sum

        if (value == TARGET) {
            // found! record result, advance both (or just one based on problem)
            left++;
            right--;
        } else if (value < TARGET) {
            left++;   // sum too small → need a bigger left element
        } else {
            right--;  // sum too big  → need a smaller right element
        }
    }
}
```

The loop runs at most n iterations (left and right together take at most n steps to meet), so the template is always O(n) — the cost of the sort that precedes it is what dominates.

---

### Problem 1.1 — Two Sum II (LeetCode 167)

**Statement.** Given a 1-indexed array `numbers` sorted in non-decreasing order, find two numbers that add to `target`. Return their indices as `[index1, index2]` (1-indexed). Exactly one solution is guaranteed.

**Approach.** Because the array is already sorted, two pointers works directly. Set left = 0, right = n−1. At each step, check the sum:
- sum == target → done.
- sum < target → the only way to increase the sum is to move left forward to a larger element.
- sum > target → the only way to decrease the sum is to move right backward to a smaller element.

**Trace** on `numbers = [2, 7, 11, 15]`, `target = 9`:

```
left=0 right=3:  arr[0]+arr[3] = 2+15 = 17 > 9  → right--
left=0 right=2:  arr[0]+arr[2] = 2+11 = 13 > 9  → right--
left=0 right=1:  arr[0]+arr[1] = 2+ 7 =  9 == 9 → return [1, 2]
```

**Full Solution:**

```java
public int[] twoSum(int[] numbers, int target) {
    int left = 0, right = numbers.length - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) {
            return new int[]{left + 1, right + 1};  // convert to 1-indexed
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    return new int[]{-1, -1};  // unreachable per problem constraints
}
```

**Complexity:** Time O(n) — left and right together take at most n steps. Space O(1) — no extra data structures.

---

### Problem 1.2 — Container With Most Water (LeetCode 11)

**Statement.** Given an integer array `height` of length n, where `height[i]` is the height of a vertical line at position i, find two lines that together with the x-axis form a container that holds the most water. Return the maximum water volume.

Volume of water between lines i and j = `min(height[i], height[j]) * (j - i)`.

**Approach.** The volume formula has two parts: the width `(j - i)` and the effective height `min(height[i], height[j])`. Start left at 0, right at n−1 — maximum possible width. Now: if we move the taller of the two lines inward, we reduce width *and* the height can only stay the same or get worse (because the taller line already isn't the limiting factor). So moving the taller pointer can never increase volume. The only hope for a larger volume when shrinking width is to move the *shorter* pointer — maybe the next inner line is much taller.

**Why this is correct (rigorous argument).** Suppose height[left] < height[right]. Consider all containers that include the left boundary at position `left`. The best such container is already the one we just computed, because right is as far right as possible. Any container formed by moving right inward while keeping left fixed will have smaller width and the same (or worse) height, giving strictly smaller volume. So we can safely discard left and advance it, knowing we've already found the best container involving position `left`.

**Trace** on `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`:

```
left=0 right=8:  min(1,7)*8 = 1*8 = 8.   height[0]=1 < height[8]=7 → left++
left=1 right=8:  min(8,7)*7 = 7*7 = 49.  height[1]=8 > height[8]=7 → right--
left=1 right=7:  min(8,3)*6 = 3*6 = 18.  height[1]=8 > height[7]=3 → right--
left=1 right=6:  min(8,8)*5 = 8*5 = 40.  height[1]=8 == height[6]=8 → either (right--)
left=1 right=5:  min(8,4)*4 = 4*4 = 16.  height[1]=8 > height[5]=4 → right--
left=1 right=4:  min(8,5)*3 = 5*3 = 15.  height[1]=8 > height[4]=5 → right--
left=1 right=3:  min(8,2)*2 = 2*2 = 4.   height[1]=8 > height[3]=2 → right--
left=1 right=2:  min(8,6)*1 = 6*1 = 6.   left >= right-1 → stop
Best seen: 49 ✓
```

**Full Solution:**

```java
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1;
    int maxWater = 0;
    while (left < right) {
        int water = Math.min(height[left], height[right]) * (right - left);
        maxWater = Math.max(maxWater, water);
        // Move the shorter side inward — only chance of improvement
        if (height[left] <= height[right]) {
            left++;
        } else {
            right--;
        }
    }
    return maxWater;
}
```

**Complexity:** Time O(n). Space O(1).

---

### Problem 1.3 — 3Sum (LeetCode 15)

**Statement.** Given an integer array `nums`, return all unique triplets `[nums[i], nums[j], nums[k]]` such that `i != j != k` and `nums[i] + nums[j] + nums[k] == 0`. The result must not contain duplicate triplets.

**Approach.** Sort the array first. Then fix one element (`nums[i]`) at a time with an outer loop, and for the remaining sub-array to the right of i, run two-pointer two-sum looking for a pair that sums to `-nums[i]`. The sort also makes duplicate skipping easy: after processing a fixed i, skip ahead over any identical values of `nums[i]` to avoid generating duplicate triplets. Same skip logic at the inner pointers.

This transforms an O(n³) brute force into **O(n²)**: n choices for the fixed element × O(n) two-pointer scan each.

**Trace** on `nums = [-4, -1, -1, 0, 1, 2]` (already sorted):

```
Outer i=0: nums[i]=-4, target for pair = +4
  left=1 right=5: -1+2=1 < 4 → left++
  left=2 right=5: -1+2=1 < 4 → left++
  left=3 right=5:  0+2=2 < 4 → left++
  left=4 right=5:  1+2=3 < 4 → left++
  left=right=5: loop ends. No triplets.

Outer i=1: nums[i]=-1, target for pair = +1
  left=2 right=5: -1+2=1 == 1 → triplet [-1,-1,2] ✓  left++ right--
  left=3 right=4:  0+1=1 == 1 → triplet [-1, 0,1] ✓  left++ right--
  left=right: loop ends.

Outer i=2: nums[i]=-1 == nums[i-1]=-1 → SKIP (duplicate outer)

Outer i=3: nums[i]=0, target for pair = 0
  left=4 right=5: 1+2=3 > 0 → right--
  left=right=4: loop ends. No triplets.

Result: [[-1,-1,2], [-1,0,1]]  ✓
```

**Full Solution:**

```java
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();

    for (int i = 0; i < nums.length - 2; i++) {
        // Early termination: smallest remaining element is positive, impossible to sum to 0
        if (nums[i] > 0) break;
        // Skip duplicate values for the fixed element
        if (i > 0 && nums[i] == nums[i - 1]) continue;

        int left = i + 1, right = nums.length - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                // Skip duplicates at the left pointer
                while (left < right && nums[left] == nums[left + 1]) left++;
                // Skip duplicates at the right pointer
                while (left < right && nums[right] == nums[right - 1]) right--;
                left++;
                right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    return result;
}
```

**Complexity:** Time O(n²) — O(n log n) sort + O(n) outer × O(n) inner two-pointer scan. Space O(1) auxiliary (the output list doesn't count as auxiliary space — it's the required return value).

**Common mistake on 3Sum specifically:** Checking `nums[left] == nums[left + 1]` and advancing *before* recording the result. Do it after — the current position is valid, it's future duplicates you want to skip.

---

## Pattern 2 — Two Pointers (Same Direction)

### Intuition

Two pointers don't have to start from opposite ends. A powerful second configuration uses both pointers starting at the left, one "fast" pointer that explores ahead and one "slow" pointer that marks where the next valid element should go. The fast pointer sees every element; the slow pointer advances only when something worth keeping has been found. This is equivalent to an in-place partition: everything at or below `slow` is "cleaned," everything ahead of `slow` but behind `fast` has been scanned and discarded.

### Template

```java
public static int twoPointersSameDirection(int[] arr) {
    int slow = 0;
    for (int fast = 0; fast < arr.length; fast++) {
        if (isValid(arr[fast])) {      // condition depends on the problem
            arr[slow] = arr[fast];     // write valid element to slow position
            slow++;                    // advance slow
        }
        // invalid elements: fast advances but slow does not
    }
    return slow;   // slow is the length of the valid portion
}
```

After this template runs, `arr[0..slow-1]` holds all valid elements in order; `arr[slow..n-1]` is garbage. For problems that don't want in-place modification, the same logic works with a result list.

---

### Problem 2.1 — Remove Duplicates from Sorted Array (LeetCode 26)

**Statement.** Given an integer array `nums` sorted in non-decreasing order, remove duplicates in-place so each unique element appears only once. Return the count `k` of unique elements. The first k elements of `nums` should be the unique elements in order.

**Approach.** Slow pointer marks the position of the last unique element written. Fast pointer scans forward; when it finds an element different from `nums[slow]` (a new unique value), write it to `nums[slow+1]` and advance slow.

**Trace** on `nums = [1, 1, 2, 2, 3]`:

```
slow=0 (arr[slow]=1)
fast=0: arr[0]=1 == arr[slow]=1 → skip
fast=1: arr[1]=1 == arr[slow]=1 → skip
fast=2: arr[2]=2 != arr[slow]=1 → slow++ → slow=1, arr[1]=2
fast=3: arr[3]=2 == arr[slow]=2 → skip
fast=4: arr[4]=3 != arr[slow]=2 → slow++ → slow=2, arr[2]=3

Array now: [1, 2, 3, 2, 3]   (first slow+1=3 elements are valid)
Return 3.
```

**Full Solution:**

```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int slow = 0;
    for (int fast = 1; fast < nums.length; fast++) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;  // slow is 0-indexed, count is slow+1
}
```

**Complexity:** Time O(n). Space O(1).

---

### Problem 2.2 — Move Zeroes (LeetCode 283)

**Statement.** Given an integer array `nums`, move all zeroes to the end while maintaining the relative order of non-zero elements. Do it in-place.

**Approach.** Slow pointer marks the next write position for non-zero elements. Fast pointer scans the entire array. Every time fast finds a non-zero element, copy it to `nums[slow]` and advance slow. After the scan, fill everything from `nums[slow]` to the end with zeroes.

**Trace** on `nums = [0, 1, 0, 3, 12]`:

```
slow=0
fast=0: arr[0]=0  → skip
fast=1: arr[1]=1  → arr[slow]=arr[1]=1, slow=1.   Array: [1,1,0,3,12]
fast=2: arr[2]=0  → skip
fast=3: arr[3]=3  → arr[slow]=arr[3]=3, slow=2.   Array: [1,3,0,3,12]
fast=4: arr[4]=12 → arr[slow]=arr[4]=12, slow=3.  Array: [1,3,12,3,12]

Now zero-fill from slow=3 to end:
Array: [1,3,12,0,0]  ✓
```

**Full Solution:**

```java
public void moveZeroes(int[] nums) {
    int slow = 0;
    // Pass 1: copy all non-zero elements to the front
    for (int fast = 0; fast < nums.length; fast++) {
        if (nums[fast] != 0) {
            nums[slow] = nums[fast];
            slow++;
        }
    }
    // Pass 2: fill the rest with zeroes
    while (slow < nums.length) {
        nums[slow] = 0;
        slow++;
    }
}
```

**Complexity:** Time O(n) — two O(n) passes = O(n). Space O(1).

---

### Problem 2.3 — Sort Colors (LeetCode 75) — The Dutch National Flag

**Statement.** Given an array `nums` with values only 0, 1, or 2, sort it in-place in one pass without using a counting sort (i.e., without counting occurrences then re-filling).

**Approach — three pointers.** This is a generalisation of the two-pointer same-direction idea. Maintain three regions:
- `[0, lo)` — all 0s
- `[lo, mid)` — all 1s
- `(hi, n-1]` — all 2s
- `[mid, hi]` — unexplored

Pointer `mid` explores. When `nums[mid]` is 0, swap it with `nums[lo]` (both lo and mid advance). When it's 2, swap with `nums[hi]` (hi retreats, mid stays — the swapped element is unexplored). When it's 1, it's already in the right region, just advance mid.

**Trace** on `nums = [2, 0, 2, 1, 1, 0]`:

```
lo=0 mid=0 hi=5
nums[mid]=2 → swap(0,5) → [0,0,2,1,1,2], hi=4
nums[mid]=0 → swap(lo,mid) → [0,0,2,1,1,2], lo=1, mid=1
nums[mid]=0 → swap(lo,mid) → [0,0,2,1,1,2], lo=2, mid=2
nums[mid]=2 → swap(2,4) → [0,0,1,1,2,2], hi=3
nums[mid]=1 → mid=3
nums[mid]=1 → mid=4
mid=4 > hi=3 → stop
Result: [0,0,1,1,2,2]  ✓
```

**Full Solution:**

```java
public void sortColors(int[] nums) {
    int lo = 0, mid = 0, hi = nums.length - 1;
    while (mid <= hi) {
        if (nums[mid] == 0) {
            swap(nums, lo, mid);
            lo++;
            mid++;
        } else if (nums[mid] == 2) {
            swap(nums, mid, hi);
            hi--;
            // don't advance mid — nums[mid] is now fresh from hi, unexplored
        } else {
            mid++;
        }
    }
}

private void swap(int[] nums, int i, int j) {
    int tmp = nums[i]; nums[i] = nums[j]; nums[j] = tmp;
}
```

**Complexity:** Time O(n) — each element is moved at most once (lo, mid, hi together take at most n steps). Space O(1).

**Pattern Recognition — Two Pointers (Same Direction):** Reach for this when the problem asks you to partition an array in-place, remove/filter elements while preserving order, or overwrite an array with a "cleaned" version without using extra memory. Key phrase recognition: "in-place," "do not allocate extra space," "maintain relative order."

---

## Pattern 3 — Sliding Window (Fixed Size)

### Intuition

You need to compute something over every contiguous subarray of a fixed size k. Brute force recomputes from scratch for each window: O(nk) total. The sliding window insight: **consecutive windows share most of their elements**. The window `arr[i..i+k-1]` and the window `arr[i+1..i+k]` differ in exactly two elements — the one that slid out on the left (`arr[i]`) and the one that slid in on the right (`arr[i+k]`). If your aggregation (sum, count, hash) supports O(1) removal and addition, updating the window is O(1) rather than O(k), bringing total complexity down to O(n).

```
Initial window:    [ 2  3  4 | 5  1  3 ]
                    ^           ^
                    |           first element outside window

Slide right:       [ 2  3  4  5 | 1  3 ]
                          ^       ^
                   removed: 2    added: 5
                   new sum = old sum - 2 + 5
```

### Template

```java
public static int slidingWindowFixed(int[] arr, int k) {
    // Build initial window
    int windowSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];

    int result = windowSum;  // or whatever you're tracking

    // Slide the window
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i];       // add the new right element
        windowSum -= arr[i - k];   // remove the element that fell off the left
        result = Math.max(result, windowSum);  // or min, or however you aggregate
    }
    return result;
}
```

---

### Problem 3.1 — Maximum Sum Subarray of Size K

**Statement.** Given an array of integers and an integer k, find the maximum sum of any contiguous subarray of size k.

**Approach.** Direct application of the fixed-size sliding window template.

**Trace** on `arr = [2, 1, 5, 1, 3, 2]`, `k = 3`:

```
Initial window [0..2]: 2+1+5 = 8.  maxSum = 8.

i=3: windowSum = 8 + arr[3] - arr[0] = 8 + 1 - 2 = 7.  maxSum = max(8,7) = 8.
i=4: windowSum = 7 + arr[4] - arr[1] = 7 + 3 - 1 = 9.  maxSum = max(8,9) = 9.
i=5: windowSum = 9 + arr[5] - arr[2] = 9 + 2 - 5 = 6.  maxSum = max(9,6) = 9.

Answer: 9  (subarray [5,1,3])
```

**Full Solution:**

```java
public int maxSumSubarrayOfSizeK(int[] arr, int k) {
    int windowSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];
    int maxSum = windowSum;
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}
```

**Complexity:** Time O(n). Space O(1).

---

### Problem 3.2 — Average of Subarrays of Size K (LeetCode 643 variant)

**Statement.** Given an array of integers and an integer k, find the maximum average of any contiguous subarray of size k. Return as a double.

**Approach.** Maximizing the average of a fixed-size window is equivalent to maximizing the sum (since k is constant). Same sliding window, just divide the maximum sum by k at the end.

**Full Solution:**

```java
public double findMaxAverage(int[] nums, int k) {
    int windowSum = 0;
    for (int i = 0; i < k; i++) windowSum += nums[i];
    int maxSum = windowSum;
    for (int i = k; i < nums.length; i++) {
        windowSum += nums[i] - nums[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return (double) maxSum / k;
}
```

**Complexity:** Time O(n). Space O(1).

**Pattern Recognition — Sliding Window Fixed:** The giveaway is "subarray (or substring) of exactly size k." Fixed window = fixed k in the problem statement. Any aggregation (sum, product, max, average, count distinct) over a fixed-size window follows this template exactly.

---

## Pattern 4 — Sliding Window (Variable Size)

### Intuition

The fixed window has a rigid size k. Many problems instead have a *condition*: "the longest subarray where all elements are distinct," "the smallest subarray whose sum is at least target," "the longest substring where no character appears more than once." The window still has a left and right boundary, but now the boundaries move according to whether the current window satisfies the condition.

The invariant to maintain: **the window always satisfies (or is working toward satisfying) the problem's condition.** When you're maximizing, you expand (move right) until the condition breaks, then shrink (move left) until it's restored. When you're minimizing, you expand until the condition is met, record the current answer, then shrink to see if you can do better.

### Template

```java
public static int slidingWindowVariable(int[] arr) {
    int left = 0;
    // Window state — whatever you need to track the condition
    // e.g., Map<Character, Integer> freq, int distinct, int sum
    int result = 0;  // or Integer.MAX_VALUE for minimization

    for (int right = 0; right < arr.length; right++) {
        // 1. Expand: include arr[right] in the window
        // update window state with arr[right]

        // 2. Shrink: while condition is violated, remove arr[left]
        while (/* condition is violated */) {
            // remove arr[left] from window state
            left++;
        }

        // 3. At this point, window [left..right] satisfies the condition
        // Update result (for maximization: update every iteration; for minimization: update when condition met)
        result = Math.max(result, right - left + 1);
    }
    return result;
}
```

The key insight about correctness: each element is added to the window once (when `right` passes it) and removed from the window at most once (when `left` passes it). Total work = O(n) regardless of how many times the inner `while` loop triggers — because the total number of left-advances across all iterations of the outer loop is at most n.

---

### Problem 4.1 — Longest Substring Without Repeating Characters (LeetCode 3)

**Statement.** Given a string `s`, find the length of the longest substring without repeating characters.

**Approach.** Use a `HashMap<Character, Integer>` mapping each character to its most recent index in the string. Maintain `left` as the start of the current valid (no-repeat) window. As `right` expands, if `s[right]` was seen before *and* its last occurrence is inside the current window (index >= left), jump `left` to `lastSeen[s[right]] + 1` to skip past the duplicate. Update the result at every step.

**Trace** on `s = "abcabcbb"`:

```
left=0 result=0
right=0 'a': not seen. lastSeen={'a':0}. window=[0,0], len=1. result=1.
right=1 'b': not seen. lastSeen={'a':0,'b':1}. window=[0,1], len=2. result=2.
right=2 'c': not seen. lastSeen={'a':0,'b':1,'c':2}. window=[0,2], len=3. result=3.
right=3 'a': seen at 0 >= left=0 → left=0+1=1. lastSeen={'a':3,'b':1,'c':2}. window=[1,3], len=3. result=3.
right=4 'b': seen at 1 >= left=1 → left=1+1=2. lastSeen={'a':3,'b':4,'c':2}. window=[2,4], len=3. result=3.
right=5 'c': seen at 2 >= left=2 → left=2+1=3. lastSeen={'a':3,'b':4,'c':5}. window=[3,5], len=3. result=3.
right=6 'b': seen at 4 >= left=3 → left=4+1=5. lastSeen={'a':3,'b':6,'c':5}. window=[5,6], len=2. result=3.
right=7 'b': seen at 6 >= left=5 → left=6+1=7. lastSeen={'a':3,'b':7,'c':5}. window=[7,7], len=1. result=3.

Answer: 3  (any of "abc", "bca", "cab", "abc")
```

**Full Solution:**

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> lastSeen = new HashMap<>();
    int left = 0, result = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        // If c was seen inside the current window, shrink from left
        if (lastSeen.containsKey(c) && lastSeen.get(c) >= left) {
            left = lastSeen.get(c) + 1;
        }
        lastSeen.put(c, right);
        result = Math.max(result, right - left + 1);
    }
    return result;
}
```

**Complexity:** Time O(n) — right and left each traverse the string at most once. Space O(min(n, charset_size)) — the HashMap holds at most 26 entries for lowercase letters, or 128 for ASCII.

**Common mistake:** Forgetting the `&& lastSeen.get(c) >= left` condition. If `lastSeen` contains `c` but at an index that's already outside (before) the current window, advancing `left` past it would actually move `left` *backward* — or in Java, you'd set `left` to a smaller value, silently invalidating the window. Always check that the last seen position is inside the current window before jumping.

---

### Problem 4.2 — Minimum Window Substring (LeetCode 76) — Hard, Full Explanation

**Statement.** Given strings `s` and `t`, return the minimum length window substring of `s` that contains every character in `t` (including duplicates). If no such window exists, return `""`.

This is the hardest variable-size sliding window problem. Work through it fully.

**Approach.** We need to track whether the current window of `s` contains all characters of `t` with the required frequencies. Two key data structures:
1. `need`: a `Map<Character, Integer>` with the required count of each character in `t`.
2. `window`: a `Map<Character, Integer>` with the current count of each character in the window.
3. `have`: count of character types whose window count has reached (≥) their needed count.
4. `required`: total number of distinct character types needed (= `need.size()`).

When `have == required`, the window is valid. Record its length, then shrink from the left to find the smallest valid window, then keep expanding.

**Why this works in O(n).** Each character in `s` enters the window once (right pointer) and leaves the window at most once (left pointer). The `have` count only increases when `window[c] == need[c]` (just satisfied), and only decreases when `window[c]` drops below `need[c]` (no longer satisfied). So `have` changes at most 2 × |t| times total, not n times.

**Trace** on `s = "ADOBECODEBANC"`, `t = "ABC"`:

```
need = {A:1, B:1, C:1}.  required = 3.  have = 0.
left = 0.  minLen = ∞.  result = "".

right=0 'A': window={A:1}. A: have(1)==need(1) → have=1.
right=1 'D': window={A:1,D:1}.
right=2 'O': window={A:1,D:1,O:1}.
right=3 'B': window={A:1,D:1,O:1,B:1}. B: have(1)==need(1) → have=2.
right=4 'E': window={...,E:1}.
right=5 'C': window={...,C:1}. C: have(1)==need(1) → have=3. ← VALID WINDOW!
  Window = "ADOBEC" (len=6). minLen=6. result="ADOBEC".
  Shrink: left=0 'A'. window[A]=1→0. A: 0 < need(1) → have=2. left=1.
  have != required, stop shrinking.

right=6 'O': window={D:1,O:2,B:1,E:1,C:1}.
right=7 'D': window={D:2,...}.
right=8 'E': window={...,E:2}.
right=9 'B': window={...,B:2}.
right=10 'A': window={...,A:1}. A: have(1)==need(1) → have=3. ← VALID WINDOW!
  Window = "DOBECODEBA..." wait let me recount.
  s = "ADOBECODEBANC", indices 0-12.
  Window is s[1..10] = "DOBECODEBA" len=10. minLen stays 6.
  Shrink: left=1 'D'. window[D]=2→1. D not in need, have unchanged. left=2.
  have==required, still valid. Window s[2..10]="OBECODEBA" len=9. minLen stays 6.
  Shrink: left=2 'O'. window[O]=2→1. not in need. left=3.
  Window s[3..10]="BECODEBA" len=8. minLen stays 6.
  Shrink: left=3 'B'. window[B]=2→1. 1 >= need(1). have unchanged. left=4.
  Window s[4..10]="ECODEBA" len=7. minLen stays 6.
  Shrink: left=4 'E'. not in need. left=5.
  Window s[5..10]="CODEBA" len=6. minLen stays 6 (tie, keep first).
  Shrink: left=5 'C'. window[C]=1→0. 0 < need(1) → have=2. left=6.
  have != required, stop shrinking.

right=11 'N': not in need.
right=12 'C': window[C]=1. C: have(1)==need(1) → have=3. ← VALID WINDOW!
  Window = s[6..12] = "ODEBANC" len=7. minLen stays 6.
  Shrink: left=6 'O'. not in need. left=7.
  Window s[7..12] = "DEBANC" len=6. tie, keep first.
  Shrink: left=7 'D'. not in need. left=8.
  Window s[8..12] = "EBANC" len=5. minLen=5. result="EBANC".
  Shrink: left=8 'E'. not in need. left=9.
  Window s[9..12] = "BANC" len=4. minLen=4. result="BANC".
  Shrink: left=9 'B'. window[B]=1→0. 0 < need(1) → have=2. left=10.
  have != required, stop shrinking.

right exhausted. Answer: "BANC"  ✓
```

**Full Solution:**

```java
public String minWindow(String s, String t) {
    if (s.isEmpty() || t.isEmpty()) return "";

    Map<Character, Integer> need = new HashMap<>();
    for (char c : t.toCharArray()) need.merge(c, 1, Integer::sum);

    Map<Character, Integer> window = new HashMap<>();
    int have = 0, required = need.size();
    int left = 0;
    int minLen = Integer.MAX_VALUE;
    int minLeft = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        window.merge(c, 1, Integer::sum);
        // Check if this character just became "satisfied"
        if (need.containsKey(c) && window.get(c).equals(need.get(c))) {
            have++;
        }

        // Shrink from left while window is valid
        while (have == required) {
            // Record this window if it's the smallest so far
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minLeft = left;
            }
            // Remove left character from window
            char leftChar = s.charAt(left);
            window.merge(leftChar, -1, Integer::sum);
            if (need.containsKey(leftChar) && window.get(leftChar) < need.get(leftChar)) {
                have--;
            }
            left++;
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(minLeft, minLeft + minLen);
}
```

**Complexity:** Time O(|s| + |t|) — right traverses s once, left traverses s at most once, building `need` is O(|t|). Space O(|s| + |t|) in the worst case for the window and need maps, though for a fixed character set (e.g., ASCII) this is O(1).

---

### Problem 4.3 — Longest Repeating Character Replacement (LeetCode 424)

**Statement.** Given a string `s` and integer `k`, you may change at most k characters in any window to any letter. Find the length of the longest substring you can get where all characters are the same.

**Key insight.** In any window, the minimum number of changes needed to make all characters identical equals `(window length) - (count of the most frequent character in the window)`. The window is valid if this value ≤ k:

```
valid condition: (right - left + 1) - maxFreq <= k
equivalently:   (right - left + 1) <= maxFreq + k
```

**Approach.** Expand right, maintain a `freq` array for character counts, and track `maxFreq` (the highest count seen in the current window). When the window becomes invalid (needs more than k changes), advance `left` by one (shrink by one). Note: we don't reduce `maxFreq` when shrinking — this is a subtle but intentional optimization. We only need to check if we've *improved* (i.e., found a window at least as large as the current best), and `maxFreq` only ever needs to be updated when a new character count exceeds the old maximum. If shrinking doesn't produce a larger `maxFreq`, we don't care.

**Trace** on `s = "AABABBA"`, `k = 1`:

```
freq={}, maxFreq=0, left=0.
right=0 'A': freq[A]=1. maxFreq=1. window=1. valid(1<=1+1=2)? yes. result=1.
right=1 'A': freq[A]=2. maxFreq=2. window=2. valid(2<=2+1=3)? yes. result=2.
right=2 'B': freq[B]=1. maxFreq=2. window=3. valid(3<=2+1=3)? yes. result=3.
right=3 'A': freq[A]=3. maxFreq=3. window=4. valid(4<=3+1=4)? yes. result=4.
right=4 'B': freq[B]=2. maxFreq=3. window=5. valid(5<=3+1=4)? NO → shrink.
  Remove left=0 'A': freq[A]=2. left=1. window=4. valid(4<=3+1=4)? yes. result still 4.
right=5 'B': freq[B]=3. maxFreq=3. window=5. valid(5<=3+1=4)? NO → shrink.
  Remove left=1 'A': freq[A]=1. left=2. window=4. valid(4<=3+1=4)? yes. result still 4.
right=6 'A': freq[A]=2. maxFreq=3. window=5. valid(5<=3+1=4)? NO → shrink.
  Remove left=2 'B': freq[B]=2. left=3. window=4. valid(4<=3+1=4)? yes. result still 4.

Answer: 4  (e.g., "AABA" → change one B to A → "AAAA")
```

**Full Solution:**

```java
public int characterReplacement(String s, int k) {
    int[] freq = new int[26];
    int left = 0, maxFreq = 0, result = 0;
    for (int right = 0; right < s.length(); right++) {
        freq[s.charAt(right) - 'A']++;
        maxFreq = Math.max(maxFreq, freq[s.charAt(right) - 'A']);
        // If window is invalid, shrink by one from left
        if ((right - left + 1) - maxFreq > k) {
            freq[s.charAt(left) - 'A']--;
            left++;
        }
        result = Math.max(result, right - left + 1);
    }
    return result;
}
```

**Complexity:** Time O(n). Space O(1) — the freq array has fixed size 26.

**Common Mistakes for Variable Sliding Window:**

1. **Using `if` instead of `while` to shrink.** For this specific problem (character replacement), the shrink-by-one approach works because we always either maintain or grow the window. For Minimum Window Substring, you need `while` because you might need to shrink many times. Know which you need before you code it.
2. **Not checking `lastSeen[c] >= left` in LCS Without Repeating.** Already covered, but worth re-emphasising — it's the most common bug on that specific problem.
3. **Counting `have` based on count equality vs count adequacy.** In Minimum Window, `have` increases when `window[c] == need[c]` (exact threshold crossing), not when `window[c] > need[c]`. Extra copies don't add to `have`. Correspondingly, `have` decreases when `window[c]` drops *below* `need[c]`, not just when it drops at all.

**Pattern Recognition — Sliding Window (Variable):**
- "Longest subarray/substring such that [condition]" → expand until condition breaks, shrink to restore.
- "Minimum subarray/substring such that [condition]" → expand until condition met, record, then shrink to see if still satisfied.
- "At most k [something]" → condition is the count exceeds k.
- "With replacement of at most k characters" → the LRCR pattern: valid condition is `windowSize - maxFreq <= k`.
