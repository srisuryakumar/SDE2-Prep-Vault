# Chapter 5: Hash Maps and Hash Sets

*The data structure itself is old news by now — this chapter is about recognizing the dozen different-looking problems that all reduce to the same question: "have I seen this before, and what was attached to it when I did?"*

## 5.1 HashMap Internals — Quick Review

You already built the mental model for this in Book 1: a HashMap is an array of buckets; a hash function maps each key to a bucket index; collisions within a bucket are handled by chaining.

```
HashMap buckets (array, simplified):
index 0:  []
index 1:  [("a", 1)] → [("q", 99)]     ← collision: "a" and "q" hash to the same bucket
index 2:  []
...
index 7:  [("z", 5)]
...
```

Average-case `get`/`put` is O(1). Worst case — a poor hash function or adversarial collisions piling everything into one bucket — degrades to O(n) per operation, or O(log n) with the red-black-tree bucket optimization Java applies once a single bucket exceeds 8 entries. `HashSet` is a `HashMap` under the hood, storing a fixed dummy value against every key — when "is this present" is the only question, that's all the structure you need.

What's new in this chapter isn't the internals. It's recognizing the family of DSA problems — counting, deduplication, complement-checking, grouping — that all collapse onto exactly the same data structure once you see past their surface differences.

## 5.2 When to Reach for a HashMap

Three signals, and most medium problems trigger at least one:

1. You need O(1) average lookup/insert instead of an O(n) linear scan or an O(log n) sorted search.
2. You're counting something — frequencies, occurrences, duplicates.
3. You're asking "have I seen this value/state before?" — deduplication, complement-checking, visited-tracking.

The trade is always the same: O(n) extra space buys O(1) average time per operation. That's not a footnote — say it out loud in an interview, exactly as Chapter 1's rule demands. A HashMap solution that doesn't mention its O(n) space cost is an incomplete answer.

---

## Pattern 1 — Frequency Counting

### Intuition

Many problems reduce to "how many times does each distinct value appear?" Build that map once, in O(n), and every subsequent question — is this a duplicate, what's the most common element, do two collections contain the same multiset — becomes an O(1) or O(k) lookup, where k is the count of distinct values.

### Template

```java
Map<Character, Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) {
    freq.merge(c, 1, Integer::sum);   // insert 1 if absent, else add 1 to existing count
}
```

`merge` replaces the classic `containsKey` / `get` / `put` dance with one call.

---

### Problem — Valid Anagram (LeetCode 242)

**Statement.** Given strings `s` and `t`, return true if `t` is an anagram of `s`.

**Approach.** Unequal lengths means an immediate false (an anagram must use every character exactly once, both ways). Build a frequency map from `s`. Walk `t`, decrementing counts; if any count goes negative, `t` has more of some character than `s` did — false. Combined with the length check, ending with no negative excursions guarantees an exact match (the total counts must balance since the lengths are equal).

**Trace** on `s = "anagram"`, `t = "nagaram"`:

```
freq from s: {a:3, n:1, g:1, r:1, m:1}

Decrement using t = n,a,g,a,r,a,m:
n: 1-1=0  (ok)
a: 3-1=2  (ok)
g: 1-1=0  (ok)
a: 2-1=1  (ok)
r: 1-1=0  (ok)
a: 1-1=0  (ok)
m: 1-1=0  (ok)

No negative excursions, lengths equal (7=7) → VALID anagram.   ✓
```

**Full Solution:**

```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;

    Map<Character, Integer> freq = new HashMap<>();
    for (char c : s.toCharArray()) {
        freq.merge(c, 1, Integer::sum);
    }
    for (char c : t.toCharArray()) {
        freq.merge(c, -1, Integer::sum);
        if (freq.get(c) < 0) return false;
    }
    return true;
}
```

**Complexity:** Time O(n). Space O(k) — k distinct characters, O(1) for a fixed alphabet like lowercase English.

---

### Problem — Top K Frequent Elements (LeetCode 347)

**Statement.** Given `nums` and integer `k`, return the `k` most frequent elements.

**Approach.** First, build the frequency map (Pattern 1, directly). Second, extract the top k. The generic way to do "top k" is a min-heap of size k — that's the formal Top-K pattern covered in Chapter 7, running in O(n log k). But this problem hands you a constraint a generic top-k problem doesn't: frequency is bounded between 1 and n. That bound enables **bucket sort by frequency** — create an array of lists indexed by frequency, drop each distinct value into `buckets[itsFrequency]`, then walk the buckets from highest frequency down, collecting values until you have k. No comparisons, no heap, O(n) flat.

**Trace** on `nums = [1,1,1,2,2,3]`, `k = 2`:

```
freq = {1:3, 2:2, 3:1}

buckets (indices 0..6, since nums.length=6):
  bucket[3] = [1]
  bucket[2] = [2]
  bucket[1] = [3]
  (all others empty)

Scan count from 6 down to 1, collecting until idx == k:
count=6,5,4: empty, skip.
count=3: bucket[3]=[1] → result[0]=1, idx=1.
count=2: bucket[2]=[2] → result[1]=2, idx=2 → idx==k, stop.

Final result: [1, 2]   ✓  (1 has the highest frequency, 2 the next-highest)
```

**Full Solution:**

```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) {
        freq.merge(num, 1, Integer::sum);
    }

    List<Integer>[] buckets = new List[nums.length + 1];   // index = frequency
    for (Map.Entry<Integer, Integer> entry : freq.entrySet()) {
        int num = entry.getKey(), count = entry.getValue();
        if (buckets[count] == null) buckets[count] = new ArrayList<>();
        buckets[count].add(num);
    }

    int[] result = new int[k];
    int idx = 0;
    for (int count = buckets.length - 1; count >= 1 && idx < k; count--) {
        if (buckets[count] != null) {
            for (int num : buckets[count]) {
                result[idx++] = num;
                if (idx == k) break;
            }
        }
    }
    return result;
}
```

**Complexity:** Time O(n) — frequency counting is O(n), bucket filling visits each distinct value once (≤ n), bucket scanning visits at most n total slots. Space O(n). The heap-based alternative (O(n log k)) is worth mentioning if asked "what if frequency weren't bounded" — it's the general-purpose tool; bucket sort is the specialized one that wins specifically because this problem bounds frequency by n.

---

## Pattern 2 — Complement Lookup

### Intuition

For "find two elements that sum to a target," brute force checks every pair — O(n²). The complement-lookup insight: instead of asking "which pairs sum to target," ask, for each element x, "have I already seen `target - x`?" If yes, you've found your pair in O(1), instead of an O(n) inner scan for every outer element. One pass, building the seen-set incrementally, turns O(n²) into O(n).

**Why incrementally, not all-at-once.** If you build the *entire* seen-set before scanning, you risk matching an element against itself (when `target = 2x` and only one `x` exists) or matching against a value that, per the problem's rules, shouldn't count yet. Checking the map *before* inserting the current element naturally avoids both traps.

### Template

```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();   // value → index
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{-1, -1};
}
```

### Problem — Two Sum (LeetCode 1)

**Statement.** Given `nums` and `target`, return the indices of the two numbers that add up to `target`. Exactly one solution exists.

**Trace** on `nums = [2, 7, 11, 15]`, `target = 9`:

```
i=0, num=2: complement = 9-2 = 7.  seen={} → not found.  seen.put(2, 0).
i=1, num=7: complement = 9-7 = 2.  seen contains 2 (at index 0)!  → return [0, 1]   ✓
```

**Complexity:** Time O(n) — one pass, O(1) average lookup per element. Space O(n).

This is the same problem as Chapter 2's **Two Sum II** in spirit, solved with a different tool. Two Sum II gave you a *sorted* array and solved it with two pointers in O(n) time **and O(1) space** — no extra memory needed, because sorted order alone was enough structure to exploit. This version gives you an *unsorted* array and needs the original (pre-sort) indices, so sorting first either costs O(n log n) or destroys the index information you need to return. The HashMap version trades that O(1) space for O(n) space but works without sorting and preserves original indices. Same underlying idea — "narrow the search using what you already know about one side of the equation" — two different tools depending on what the input gives you for free.

---

## Pattern 3 — Grouping via Canonical Key

### Intuition

Two strings are anagrams exactly when they have identical character frequencies — equivalently, sorting both strings' characters produces the identical result. That sorted string is a **canonical key**: every anagram of a given string maps to the same key, and nothing else does. Use the canonical key as a HashMap key, and every anagram group falls into the same bucket in one pass.

### Problem — Group Anagrams (LeetCode 49)

**Statement.** Given an array of strings, group the anagrams together.

**Approach.** For each string, sort its characters to get the canonical key, then append the original string to that key's group.

**Trace** on `strs = ["eat","tea","tan","ate","nat","bat"]`:

```
"eat" → sorted "aet" →  groups = {"aet": [eat]}
"tea" → sorted "aet" →  groups = {"aet": [eat, tea]}
"tan" → sorted "ant" →  groups = {"aet": [...], "ant": [tan]}
"ate" → sorted "aet" →  groups = {"aet": [eat, tea, ate], "ant": [tan]}
"nat" → sorted "ant" →  groups = {"aet": [...], "ant": [tan, nat]}
"bat" → sorted "abt" →  groups = {..., "abt": [bat]}

Final:  [[eat, tea, ate], [tan, nat], [bat]]   ✓  (group order may vary)
```

**Full Solution:**

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);   // canonical form
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```

**Complexity:** Time O(n · m log m), where n = number of strings, m = max string length (sorting each costs O(m log m)). Space O(n · m).

**A faster canonical key, if asked "can you avoid sorting":** use a frequency signature instead — a fixed-size count array (e.g., 26 ints for lowercase letters) converted to a string like `"3#0#1#0..."`. Building it costs O(m), not O(m log m), bringing the total to O(n · m).

---

## Pattern 4 — Prefix Sum + HashMap (The Generalized Complement Lookup)

This exact problem already got a full trace in Chapter 2 as the flagship example of combining prefix sums with a HashMap — **Subarray Sum Equals K** (LeetCode 560). It's worth a second look from this chapter's vantage point, because it reveals something Chapter 2 didn't yet have the vocabulary to say: **this is structurally the same trick as Two Sum, one layer removed.**

Recall the identity: a subarray's sum equals k exactly when `prefix[j+1] - prefix[i] = k`, which rearranges to `prefix[i] = prefix[j+1] - k`. Compare that to Two Sum's check: `complement = target - nums[i]`. Both ask the identical question — "have I already seen this specific complementary value?" — just computed over a running *prefix sum* instead of a raw array element. Recognizing a problem as "Two Sum in disguise, but over some transformed running quantity instead of raw elements" is one of the highest-leverage skills in this book; it's what lets you solve Subarray Sum Equals K, Continuous Subarray Sum, and several of their cousins with the same five lines once Two Sum's complement-lookup shape is internalized, rather than re-deriving each one from scratch.

For the complete step-by-step trace — including exactly why the map must be seeded with `{0: 1}` before the scan starts — see **Chapter 2, Pattern 5, Problem 5.2**. The code, for reference:

```java
public int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> prefixCount = new HashMap<>();
    prefixCount.put(0, 1);
    int curr = 0, count = 0;
    for (int num : nums) {
        curr += num;
        count += prefixCount.getOrDefault(curr - k, 0);
        prefixCount.merge(curr, 1, Integer::sum);
    }
    return count;
}
```

**Complexity:** Time O(n). Space O(n).

---

## Bonus Pattern — HashSet for O(n) Sequence Detection

### Problem — Longest Consecutive Sequence (LeetCode 128)

**Statement.** Given an unsorted array of integers, find the length of the longest run of consecutive integers — e.g., `[100,4,200,1,3,2]` → the run `[1,2,3,4]`, length 4. Required: O(n).

**Why sorting first doesn't qualify.** Sorting gets you there in O(n log n), which is close but not what's asked. A HashSet gets the true O(n).

**Approach.** Drop every number into a `HashSet` — O(n), and duplicates collapse automatically (a repeated value can't extend a run any further than it already does). For each number, only **start** counting a run from it if `num - 1` is *not* in the set — i.e., it's genuinely the start of a run. If `num - 1` *is* in the set, some earlier number already owns this entire run and will count it when its own turn comes; counting from the middle of a run would be redundant work. For each true start, walk forward (`num+1`, `num+2`, ...) checking set membership until the chain breaks, tracking the longest chain found.

**Why this is O(n) despite the inner `while` loop.** Every number is only ever the start of a count-forward walk once (non-starts are skipped entirely), and every number gets visited by *some* inner `while` loop at most once across the whole algorithm — it can only ever be walked-through by the one sequence-start that owns its run. Total work summed across every inner loop, over the entire run of the algorithm, is O(n) — not (number of starts) × (average run length).

**Trace** on `nums = [100, 4, 200, 1, 3, 2]`:

```
set = {100, 4, 200, 1, 3, 2}

num=100: is 99 in set? No → start. Forward: is 101? No. length=1.  longest=1.
num=4:   is 3 in set? Yes → NOT a start. Skip.
num=200: is 199 in set? No → start. Forward: is 201? No. length=1.  longest stays 1.
num=1:   is 0 in set? No → start. Forward: 2? yes(len2). 3? yes(len3). 4? yes(len4). 5? No, stop.
                                                                                       longest=4.
num=3:   is 2 in set? Yes → NOT a start. Skip.
num=2:   is 1 in set? Yes → NOT a start. Skip.

Final longest = 4   ✓   (the run [1, 2, 3, 4])
```

**Full Solution:**

```java
public int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int num : nums) set.add(num);

    int longest = 0;
    for (int num : set) {
        if (!set.contains(num - 1)) {   // only count forward from a true start
            int length = 1;
            int curr = num;
            while (set.contains(curr + 1)) {
                curr++;
                length++;
            }
            longest = Math.max(longest, length);
        }
    }
    return longest;
}
```

**Complexity:** Time O(n) — building the set is O(n), and the combined cost of every inner `while` loop across the entire run is O(n), as argued above. Space O(n).

**Common mistake:** skipping the `!set.contains(num - 1)` start-check and counting forward from *every* number. This still produces the *correct* answer — but degrades to O(n²) in the worst case (a single long consecutive run causes every number in it to redundantly re-walk the rest of the chain). The bug doesn't show up as a wrong answer on small test cases, which is exactly what makes it easy to ship by accident; it shows up as a timeout on large ones.

---

## Common Mistakes — Chapter-Wide

- **Skipping the length check in Valid Anagram.** Without it guaranteed up front, checking only for negative counts isn't enough — you'd also need a second pass verifying every count lands at exactly zero.
- **Reaching for a heap by reflex in Top K Frequent.** The bounded frequency range (1 to n) makes bucket sort the faster O(n) option; know when the specialized tool beats the generic one.
- **Forgetting the sequence-start check in Longest Consecutive Sequence.** Produces a correct-but-O(n²) solution that passes small tests and times out on large ones.
- **Forgetting the `{0: 1}` seed in any prefix-sum-as-complement-lookup problem.** Silently undercounts subarrays that start at index 0.
- **Using a raw `char[]` as a HashMap key.** Java arrays don't override `equals()`/`hashCode()` — they use identity comparison by default, so two different array objects with identical contents are treated as *different* keys. Always convert to `String` (or another type with proper value-based `equals`/`hashCode`) before using something as a map key — this is exactly the trap Group Anagrams is built to test.

## Pattern Recognition Guide

- "Count occurrences," "find duplicates," "most/least frequent" → frequency counting.
- "Two elements satisfying a sum/relationship," on an unsorted array, needing original indices → complement lookup.
- "Subarray sum/count satisfying a target, array may include negatives" → prefix sum + HashMap — recognize it as complement lookup over running prefix sums, not raw elements.
- "Group items by equivalence" (anagrams, or any same-shape-different-label relationship) → canonical key as the HashMap key.
- "Longest run / longest consecutive sequence," where sorting's O(n log n) is too slow → HashSet + count-forward-from-true-starts-only.
- The chapter-wide tell: if you're writing a nested loop just to check "does X already exist somewhere in here," stop — that's almost always an O(n²)-to-O(n) HashMap or HashSet opportunity waiting to happen.

## Chapter Summary

- A HashMap trades O(n) space for O(1) average time per lookup/insert. Reach for it when counting, deduplicating, or asking "have I seen this before."
- Frequency counting (one O(n) pass) underlies anagram checks, top-k-frequent problems, and any "what's the most/least common X" question.
- Complement lookup turns O(n²) pair-finding into O(n) by checking "have I already seen the complement" incrementally, rather than testing every pair.
- Prefix Sum + HashMap is complement lookup wearing a disguise — same idea, applied to running prefix sums instead of raw values. Seeing that connection is what generalizes one memorized trick into a whole family of solvable problems.
- Canonical keys (sorted strings, frequency signatures) let semantically-equivalent-but-differently-ordered items collapse into the same HashMap bucket in a single pass.
- A HashSet's O(1) membership check turns "longest consecutive run" from an O(n log n) sorting problem into a true O(n) one — but only with the discipline to count forward exclusively from genuine sequence starts.
