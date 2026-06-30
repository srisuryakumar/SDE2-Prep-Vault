# Chapter 11: Backtracking
## Part 2 — Combination Sum I → II → III · N-Queens

## Problem — Combination Sum (LeetCode 39)

**Statement.** Given distinct positive integers `candidates` and a `target`, return all unique combinations summing to target. The **same number may be reused unlimited times**.

**Approach.** At each step, either include the current candidate (recursing while staying at the *same* index — reuse is unlimited, so nothing prevents picking it again) or move to the next candidate. Prune the moment a candidate alone would overshoot the remaining target — since every candidate is positive, adding more can only make things worse from there.

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, target, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] candidates, int remaining, int start,
                        List<Integer> current, List<List<Integer>> result) {
    if (remaining == 0) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = start; i < candidates.length; i++) {
        if (candidates[i] > remaining) continue;   // PRUNE: this candidate alone overshoots

        current.add(candidates[i]);
        backtrack(candidates, remaining - candidates[i], i, current, result);   // SAME i — reuse allowed
        current.remove(current.size() - 1);
    }
}
```

**Trace** on `candidates=[2,3,6,7]`, `target=7`:

```
choose 2 → remaining=5
  choose 2 (reuse) → remaining=3
    choose 2 (reuse) → remaining=1 → nothing fits (smallest candidate is 2) → dead end
    choose 3 → remaining=0 → RECORD [2,2,3]
  choose 3 → remaining=2 → nothing fits (3 itself already exceeds 2) → dead end
choose 3 → remaining=4
  choose 3 (reuse) → remaining=1 → dead end
choose 6 → remaining=1 → dead end
choose 7 → remaining=0 → RECORD [7]

Final: [[2,2,3],[7]]   ✓   (2+2+3=7, 7=7 — exactly the two known answers for this input)
```

**Complexity:** roughly O(n^(target/min(candidates))) in the worst case — hard to express tightly, since it depends on candidate values, not just count. Space O(target / min(candidate)) for recursion depth.

---

## Problem — Combination Sum II (LeetCode 40)

**Statement.** Candidates **may contain duplicates**; each number used **at most once**. Return all unique combinations summing to target.

**Approach — combining two techniques already seen.** Switch the recursive call to `i+1` instead of `i` (Combination Sum I's "no reuse" change), *and* add Subsets II's duplicate-skip (`i > start && candidates[i] == candidates[i-1]`) to avoid generating the same combination twice when a value repeats in the input.

```java
public List<List<Integer>> combinationSum2(int[] candidates, int target) {
    Arrays.sort(candidates);   // required for both the duplicate-skip and the break below
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, target, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] candidates, int remaining, int start,
                        List<Integer> current, List<List<Integer>> result) {
    if (remaining == 0) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = start; i < candidates.length; i++) {
        if (candidates[i] > remaining) break;     // sorted — everything after this also overshoots
        if (i > start && candidates[i] == candidates[i - 1]) continue;   // skip duplicate AT THIS LEVEL

        current.add(candidates[i]);
        backtrack(candidates, remaining - candidates[i], i + 1, current, result);   // i+1 — no reuse
        current.remove(current.size() - 1);
    }
}
```

**Two changes from Combination Sum I, side by side:** the recursive call now advances to `i+1` (each number used at most once), and the overshoot check now `break`s instead of `continue`s — safe specifically *because* the array is sorted, so once one candidate overshoots, every candidate after it (all equal or larger) overshoots too. No need to check them individually.

**Trace** on `candidates=[10,1,2,7,6,1,5]`, `target=8` — sorted first: `[1,1,2,5,6,7,10]`:

```
i=0 (val=1, idx0): choose → remaining=7
  i=1 (val=1, idx1): i==start, not a same-level repeat → choose → remaining=6
    i=2 (val=2): choose → remaining=4 → next candidate (5) exceeds 4 → dead end
    i=3 (val=5): choose → remaining=1 → next candidate (6) exceeds 1 → dead end
    i=4 (val=6): choose → remaining=0 → RECORD [1,1,6]
    i=5 (val=7): 7 > 6 → break
  i=2 (val=2): choose → remaining=5
    i=3 (val=5): choose → remaining=0 → RECORD [1,2,5]
    i=4 (val=6): 6 > 5 → break
  i=3 (val=5): choose → remaining=2 → next candidate (6) exceeds 2 → dead end
  i=4 (val=6): choose → remaining=1 → next candidate (7) exceeds 1 → dead end
  i=5 (val=7): choose → remaining=0 → RECORD [1,7]
i=1 (val=1, idx1): i>start AND candidates[1]==candidates[0] → SKIP (duplicate at this level)
i=2 (val=2): choose → remaining=6
  i=4 (val=6): choose → remaining=0 → RECORD [2,6]
  (i=3 leads to remaining=1, dead end; i=5 exceeds 6, break)
i=3..6: each dead-ends before reaching remaining=0

Final: [[1,1,6],[1,2,5],[1,7],[2,6]]   ✓   matches the well-known answer for this exact input
```

**Complexity:** bounded by the search tree's actual size; sorting plus the `break`/skip pruning keeps real work well below brute-force 2ⁿ. Space O(n) for recursion depth.

---

## Problem — Combination Sum III (LeetCode 216)

**Statement.** Find all combinations of **exactly k** numbers, using only **1–9**, each used at most once, summing to **n**.

**Approach — two new constraints stacked on the same shape.** The candidate pool is now fixed (1–9, no input array), and there's a *fixed required count* k, not just a sum target — so the success check needs *both* `remaining == 0` *and* `current.size() == k` simultaneously. Reaching `remaining == 0` with the wrong count is not success here, unlike Combination Sum I/II where any count that reaches the target works.

```java
public List<List<Integer>> combinationSum3(int k, int n) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(k, n, 1, new ArrayList<>(), result);
    return result;
}

private void backtrack(int k, int remaining, int start, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == k && remaining == 0) {
        result.add(new ArrayList<>(current));
        return;
    }
    if (current.size() == k || remaining <= 0) {
        return;   // PRUNE: wrong count already, or overshot — this branch can never succeed
    }
    for (int i = start; i <= 9; i++) {
        current.add(i);
        backtrack(k, remaining - i, i + 1, current, result);   // i+1 — each digit used at most once
        current.remove(current.size() - 1);
    }
}
```

**The new pruning condition worth calling out:** `current.size() == k || remaining <= 0` stops a branch the instant *either* constraint is already violated — too many numbers chosen with the sum not yet hit, or the sum already overshot — without waiting to hit a leaf of the recursion tree first. Pruning on two independent conditions simultaneously is a step up from Combination Sum I/II's single condition.

**Trace** on `k=3, n=7`:

```
choose 1 → remaining=6, need 2 more digits ≥2 summing to 6
  choose 2 → remaining=4, need 1 more digit ≥3 summing to exactly 4
    choose 3 → remaining=1, size==3 but remaining≠0 → PRUNE
    choose 4 → remaining=0, size==3 AND remaining==0 → RECORD [1,2,4]
    choose 5 → remaining=-1, size==3 → PRUNE
    (6,7,8,9 similarly overshoot and prune)
  choose 3 → remaining=3, need 1 more digit ≥4 summing to exactly 3 → impossible, every choice prunes
  (4,5,6,7 similarly leave an impossible-to-fill gap)
choose 2 → remaining=5, need 2 more digits ≥3 — the smallest possible pair, 3+4=7, already exceeds 5
           → impossible, every branch prunes
(starting from 3 or higher leaves even less room — every branch prunes)
```

**Final result:** `[[1,2,4]]` — and there's a clean reason it's the *only* answer: the minimum possible sum of 3 distinct digits is `1+2+3=6`. Reaching exactly 7 means increasing that minimal set by just 1 without creating a duplicate — `{1,2,3} → {1,2,4}` is the only way to do it. ✓

**Complexity:** bounded by C(9,k) candidate combinations in the worst case. Space O(k) for recursion depth.

---

## Problem — N-Queens (LeetCode 51)

**Statement.** Place n queens on an n×n board so no two attack each other (shared row, column, or diagonal). Return all distinct solutions.

**Approach.** Place queens **one row at a time** — this alone guarantees no two queens ever share a row, by construction. For each row, try every column, checking before placing whether it conflicts with any already-placed queen.

**Making conflict-checking O(1) instead of O(n).** Instead of scanning every previously placed queen on each attempt, maintain three sets: `cols` (occupied columns), `diag1` (occupied `row − col` values — one diagonal direction), `diag2` (occupied `row + col` values — the other diagonal direction). Two cells share a "\\"-diagonal exactly when their `row − col` values are equal, and a "/"-diagonal exactly when their `row + col` values are equal.

```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    int[] queens = new int[n];   // queens[row] = column of the queen placed in that row
    Set<Integer> cols = new HashSet<>();
    Set<Integer> diag1 = new HashSet<>();   // row - col
    Set<Integer> diag2 = new HashSet<>();   // row + col

    backtrack(0, n, queens, cols, diag1, diag2, result);
    return result;
}

private void backtrack(int row, int n, int[] queens, Set<Integer> cols,
                        Set<Integer> diag1, Set<Integer> diag2, List<List<String>> result) {
    if (row == n) {
        result.add(buildBoard(queens, n));
        return;
    }
    for (int col = 0; col < n; col++) {
        int d1 = row - col, d2 = row + col;
        if (cols.contains(col) || diag1.contains(d1) || diag2.contains(d2)) {
            continue;   // PRUNE: conflicts with an already-placed queen
        }

        queens[row] = col;
        cols.add(col); diag1.add(d1); diag2.add(d2);

        backtrack(row + 1, n, queens, cols, diag1, diag2, result);

        cols.remove(col); diag1.remove(d1); diag2.remove(d2);
    }
}

private List<String> buildBoard(int[] queens, int n) {
    List<String> board = new ArrayList<>();
    for (int row = 0; row < n; row++) {
        char[] rowChars = new char[n];
        Arrays.fill(rowChars, '.');
        rowChars[queens[row]] = 'Q';
        board.add(new String(rowChars));
    }
    return board;
}
```

**Trace** on `n=4` (the smallest n with a non-trivial answer):

```
row=0, col=0: place.  d1=0, d2=0.
  row=1: col=1 conflicts (shares diagonal d1=0 with (0,0)). col=2 works → place.
    row=2: every column conflicts with either (0,0) or (1,2) → dead end, fully backtrack.
  row=1: col=3 works → place.
    row=2: col=1 works → place.
      row=3: every column conflicts → dead end.
  → the entire row=0,col=0 branch produces no solution.

row=0, col=1: place.  d1=-1, d2=1.
  row=1: col=3 works → place.  d1=-2, d2=4.
    row=2: col=0 works → place.  d1=2, d2=2.
      row=3: col=2 works → place.  d1=1, d2=5 — no conflict with any prior queen.
        row=4 == n → SUCCESS: queens = [1,3,0,2]

row=0, col=2: (mirror image of the col=1 branch) → SUCCESS: queens = [2,0,3,1]
row=0, col=3: (mirror image of the col=0 branch) → no solution
```

**Final: 2 solutions** — `[1,3,0,2]` and `[2,0,3,1]`, mirror images of each other. Matches the well-known fact that N-Queens for n=4 has exactly 2 solutions. ✓

**Complexity:** O(n!) absolute worst case (n choices for row 0, at most n−1 surviving for row 1, and so on) — diagonal pruning cuts the *actual* search far below this in practice, which is the entire reason the O(1) conflict check matters. Space O(n) for the three tracking sets plus recursion depth.

**Common mistake:** checking conflicts by scanning every previously placed queen (O(n) per check, O(n²) per row, O(n³) total just for conflict-checking) instead of maintaining the three O(1)-lookup sets. Both are correct; the set-based version is meaningfully faster and is the version worth having memorized.

---

*Part 3 closes the chapter with Sudoku Solver (constraint propagation + backtracking), Word Search (the single-word version, building directly on Chapter 9's Word Search II), Palindrome Partitioning (backtracking + memoization), and the chapter-wide wrap-up.*
