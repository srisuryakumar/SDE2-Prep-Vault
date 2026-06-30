# Chapter 11: Backtracking
## Part 1 — The Template · Subsets → Subsets II → Permutations → Permutations II

*Backtracking is DFS with one extra discipline: undo every choice before trying its sibling. Forget that one step and every branch after the first one inherits corrupted state. This chapter is built around making that single line impossible to forget.*

## 11.1 What Backtracking Is

Backtracking systematically searches every possible configuration — combination, permutation, arrangement — by building a partial solution incrementally, and abandoning ("pruning") that partial solution the *instant* it's clear it can't lead anywhere valid, backtracking to try a different choice instead.

It's DFS over an implicit decision tree: each node is a partial solution, each edge is one additional choice. The efficiency gain over brute-force enumeration is real: pruning skips *entire subtrees* of invalid possibilities the moment a violation is detected, instead of generating every complete candidate and checking validity only at the very end.

## 11.2 The Template: Choose → Explore → Unchoose

```java
void backtrack(/* current state, parameters */) {
    if (/* base case: complete solution found */) {
        result.add(/* copy of current state */);
        return;
    }
    for (/* each possible choice at this point */) {
        if (/* choice is invalid — prune */) continue;

        currentState.add(choice);          // CHOOSE
        backtrack(/* updated parameters */);   // EXPLORE
        currentState.remove(currentState.size() - 1);   // UNCHOOSE
    }
}
```

**The unchoose step is the entire reason this differs from plain DFS** (Chapter 8). After fully exploring everything that follows from a choice, it must be undone before trying the *sibling* choice — otherwise the state at the next loop iteration incorrectly still reflects a choice that's supposed to be off the table again. Forgetting to unchoose is the single most common backtracking bug, and it silently corrupts every branch that runs after the first one.

## 11.3 When to Reach for Backtracking

"Find all X" or "does there exist an X" questions, where X is built incrementally from smaller pieces, *and* partial validity can be checked before the structure is complete — that second condition is what enables pruning. Without early pruning opportunities, backtracking degrades to brute-force enumeration with extra bookkeeping — still correct, just without the part that makes the technique worth naming.

---

## Problem — Subsets (LeetCode 78)

**Statement.** Given distinct integers, return all possible subsets (the power set).

**Approach.** Build subsets by choosing a starting index and deciding, for each index from there onward, whether to add it before recursing further. Every single recursive call — not just a "base case" — represents a valid subset, so the result is recorded on *entry* to every call, not just at the end of a branch.

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current));   // every partial state is itself a valid subset

    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);                       // CHOOSE
        backtrack(nums, i + 1, current, result);     // EXPLORE
        current.remove(current.size() - 1);          // UNCHOOSE
    }
}
```

**Trace** on `nums=[1,2,3]` (the decision tree, condensed):

```
backtrack(start=0, []): record []
  choose 1 → backtrack(start=1, [1]): record [1]
    choose 2 → backtrack(start=2, [1,2]): record [1,2]
      choose 3 → backtrack(start=3, [1,2,3]): record [1,2,3]
      unchoose 3
    unchoose 2
    choose 3 → backtrack(start=3, [1,3]): record [1,3]
    unchoose 3
  unchoose 1
  choose 2 → backtrack(start=2, [2]): record [2]
    choose 3 → backtrack(start=3, [2,3]): record [2,3]
    unchoose 3
  unchoose 2
  choose 3 → backtrack(start=3, [3]): record [3]
  unchoose 3

Final: [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]   — 8 subsets = 2³   ✓
```

**Complexity:** O(n · 2ⁿ) time (2ⁿ subsets, each up to O(n) to copy). Space O(n) recursion depth, excluding output.

---

## Problem — Subsets II (LeetCode 90)

**Statement.** Same as Subsets, but the input may contain duplicates — return all subsets with no duplicate subset in the result.

**Approach.** Sort first, grouping equal values adjacent to each other. At each level of the loop, skip a candidate if it equals the *previous* candidate considered **at this same level** (`i > start && nums[i] == nums[i-1]`). This blocks generating the same subset twice by treating "the first occurrence of value X" and "the second occurrence of value X" as interchangeable *at the same depth* — while still allowing duplicates to appear *together* in one subset, since the first occurrence at a level can still recurse downward and pick up the second occurrence one level deeper (that's exactly how `[2,2]` gets generated below).

```java
public List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums);   // required for the skip condition to work at all
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current));

    for (int i = start; i < nums.length; i++) {
        if (i > start && nums[i] == nums[i - 1]) continue;   // skip a duplicate choice AT THIS LEVEL

        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

**Trace** on `nums=[1,2,2]` (sorted):

```
backtrack(start=0, []): record []
  choose 1 → backtrack(start=1, [1]): record [1]
    choose 2(idx1) → backtrack(start=2, [1,2]): record [1,2]
      choose 2(idx2) → backtrack(start=3, [1,2,2]): record [1,2,2]
    i=2: i>start(2>1) AND nums[2]==nums[1] → SKIP
  choose 2(idx1) → backtrack(start=2, [2]): record [2]
    choose 2(idx2) → backtrack(start=3, [2,2]): record [2,2]
  i=2: i>start(2>0) AND nums[2]==nums[1] → SKIP

Final: [[],[1],[1,2],[1,2,2],[2],[2,2]]   — 6 unique subsets
```

**Verify:** the multiset `{1,2,2}` has `2 × 3 = 6` distinct subsets (value 2 can appear 0, 1, or 2 times, independent of value 1 appearing 0 or 1 times): `{}, {1}, {2}, {1,2}, {2,2}, {1,2,2}`. Matches exactly. ✓ Without the skip, `[2]` and `[2,2]` would each get generated twice — once for "use the first 2," once for "use the second 2" — even though both produce identical output.

**Complexity:** O(n · 2ⁿ) time, O(n) space — the skip is O(1) extra work per iteration, same asymptotic class as Subsets.

---

## Problem — Permutations (LeetCode 46)

**Statement.** Given distinct integers, return all permutations.

**Approach.** Unlike Subsets (which only ever moves a starting index forward, never revisiting earlier elements), a permutation needs every element available at *every* position — just not reused within the same permutation. Track which indices are currently "used" with a boolean array.

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    backtrack(nums, used, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;

        used[i] = true;                              // CHOOSE
        current.add(nums[i]);
        backtrack(nums, used, current, result);        // EXPLORE
        current.remove(current.size() - 1);             // UNCHOOSE
        used[i] = false;
    }
}
```

**Trace** on `nums=[1,2,3]` (one full branch shown in detail; the remaining five permutations follow the identical mechanism):

```
choose 1 → [1]
  choose 2 → [1,2]
    choose 3 → [1,2,3]: size==3 → record [1,2,3]
    unchoose 3
  unchoose 2
  choose 3 → [1,3]
    choose 2 → [1,3,2]: record [1,3,2]
    unchoose 2
  unchoose 3
unchoose 1
... (i=1 branch generates [2,1,3],[2,3,1]; i=2 branch generates [3,1,2],[3,2,1])

Final: [1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]   — 6 = 3!   ✓
```

**Complexity:** O(n · n!) time (n! permutations, each O(n) to build). Space O(n) for `used` plus recursion depth.

---

## Problem — Permutations II (LeetCode 47)

**Statement.** Same as Permutations, but the input may have duplicates — return only unique permutations.

**Approach.** Sort first, then skip a candidate value if it equals the previous candidate at the *same position* **and** the previous one hasn't been used yet: `nums[i] == nums[i-1] && !used[i-1]`.

**Why `!used[i-1]`, not `used[i-1]` — the trickiest line in this entire chapter.** Think of duplicate values as having a strict left-to-right priority among *themselves*, even though they're indistinguishable in the final output: only ever use the leftmost *unused* occurrence of a repeated value before considering one to its right, at the same recursive depth. If `nums[i] == nums[i-1]` and `used[i-1]` is **false**, the earlier identical value is sitting unused right now, fully available — choosing the *later* occurrence instead, while skipping over an available identical earlier one, generates the exact same resulting permutation through a redundant second path. Skip it. If `used[i-1]` is **true** instead, the earlier copy is already locked into a *different* position higher up in the current partial permutation — using this occurrence now isn't redundant with anything, it's necessary.

```java
public List<List<Integer>> permuteUnique(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    backtrack(nums, used, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;   // the key skip

        used[i] = true;
        current.add(nums[i]);
        backtrack(nums, used, current, result);
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```

**Trace** on `nums=[1,1,2]` (sorted) — every branch shown, since the skip logic is exactly what needs verifying:

```
i=0 (val=1, idx0): not used, i=0 so no dup check applies. CHOOSE.  used=[T,F,F]  current=[1]
  i=0: used → skip.
  i=1 (val=1, idx1): nums[1]==nums[0] AND !used[0]? used[0]=TRUE right now → !used[0]=FALSE
                      → condition FAILS → NOT skipped (the earlier copy is in use — fine to use this one).
                      CHOOSE.  used=[T,T,F]  current=[1,1]
    i=2 (val=2): no dup issue. CHOOSE → current=[1,1,2]: size==3 → record [1,1,2]. UNCHOOSE.
  UNCHOOSE idx1 → current=[1]
  i=2 (val=2, idx2): no dup issue. CHOOSE.  used=[T,F,T]  current=[1,2]
    i=1 (val=1, idx1): nums[1]==nums[0] AND !used[0]? used[0]=TRUE → !used[0]=FALSE → NOT skipped.
                        CHOOSE → current=[1,2,1]: size==3 → record [1,2,1]. UNCHOOSE.
  UNCHOOSE idx2 → current=[1]
UNCHOOSE idx0 → current=[]

i=1 (val=1, idx1): nums[1]==nums[0] AND !used[0]? used[0]=FALSE (just unchosen) → !used[0]=TRUE
                    → condition HOLDS → SKIP.
                    (This is exactly the redundant path: using the SECOND '1' while the FIRST
                     sits unused would just regenerate permutations already covered by i=0's branch.)

i=2 (val=2, idx2): CHOOSE.  used=[F,F,T]  current=[2]
  i=0 (val=1, idx0): i=0, no dup check. CHOOSE.  used=[T,F,T]  current=[2,1]
    i=1 (val=1, idx1): nums[1]==nums[0] AND !used[0]? used[0]=TRUE → NOT skipped.
                        CHOOSE → current=[2,1,1]: size==3 → record [2,1,1]. UNCHOOSE.
  UNCHOOSE idx0 → current=[2]
  i=1 (val=1, idx1): nums[1]==nums[0] AND !used[0]? used[0]=FALSE (just unchosen) → SKIP.
UNCHOOSE idx2 → current=[]

Final: [[1,1,2],[1,2,1],[2,1,1]]   — 3 unique permutations
```

**Verify:** the multiset `{1,1,2}` has `3! / 2! = 3` distinct permutations (dividing by `2!` because the two 1's are indistinguishable). Matches exactly. ✓

**Complexity:** O(n · n!) time worst case (pruning reduces actual work whenever duplicates exist). Space O(n).

---

*Part 2 covers Combination Sum I → II → III — showing exactly how the pruning logic changes across three closely related problems — and N-Queens.*
