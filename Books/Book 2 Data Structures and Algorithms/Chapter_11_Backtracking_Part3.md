# Chapter 11: Backtracking
## Part 3 — Sudoku Solver · Word Search · Palindrome Partitioning

## Problem — Sudoku Solver (LeetCode 37)

**Statement.** Fill a 9×9 Sudoku board so every row, column, and 3×3 box contains 1–9 with no repeats.

**Approach.** Backtracking with constraint propagation: for each empty cell, try every digit 1–9, checking validity against its row, column, and box. Maintain three boolean tracking structures — `rows[r][d]`, `cols[c][d]`, `boxes[b][d]` — so each validity check is O(1) instead of an O(9) scan, the same trade N-Queens made with its three sets.

```java
public void solveSudoku(char[][] board) {
    boolean[][] rows = new boolean[9][9];
    boolean[][] cols = new boolean[9][9];
    boolean[][] boxes = new boolean[9][9];

    for (int r = 0; r < 9; r++) {
        for (int c = 0; c < 9; c++) {
            if (board[r][c] != '.') {
                int d = board[r][c] - '1';
                rows[r][d] = true;
                cols[c][d] = true;
                boxes[boxIndex(r, c)][d] = true;
            }
        }
    }
    backtrack(board, 0, 0, rows, cols, boxes);
}

private int boxIndex(int r, int c) {
    return (r / 3) * 3 + (c / 3);
}

private boolean backtrack(char[][] board, int r, int c, boolean[][] rows, boolean[][] cols, boolean[][] boxes) {
    if (r == 9) return true;                                            // every row filled — solved
    if (c == 9) return backtrack(board, r + 1, 0, rows, cols, boxes);    // move to the next row
    if (board[r][c] != '.') return backtrack(board, r, c + 1, rows, cols, boxes);   // already filled

    int box = boxIndex(r, c);
    for (char digitChar = '1'; digitChar <= '9'; digitChar++) {
        int d = digitChar - '1';
        if (rows[r][d] || cols[c][d] || boxes[box][d]) continue;   // PRUNE: conflict

        board[r][c] = digitChar;
        rows[r][d] = true; cols[c][d] = true; boxes[box][d] = true;

        if (backtrack(board, r, c + 1, rows, cols, boxes)) {
            return true;   // a full solution exists down this path — propagate success upward
        }

        board[r][c] = '.';
        rows[r][d] = false; cols[c][d] = false; boxes[box][d] = false;
    }
    return false;   // no digit worked here — this entire branch fails, backtrack further
}
```

**Why this returns `boolean`, unlike every other problem in this chapter.** Every prior problem wanted *every* valid solution, accumulating into a list while every branch got explored regardless of earlier successes. Sudoku wants exactly *one* solution (the puzzle has a unique answer by construction), so the moment a complete solution is found, that success must propagate all the way back up through every level of recursion, halting all further exploration immediately. That's exactly what `if (backtrack(...)) return true;` does at every level — a meaningfully different shape of backtracking: existence search with immediate short-circuit, not exhaustive enumeration.

**Illustrating the mechanism** (an 81-cell trace would be too long to be useful — here's the part that actually matters):

Suppose the search reaches an empty cell at row 4, column 5, inside box `(4/3)*3 + (5/3) = 3`. Row 4 already contains `{2,7,9}`; column 5 already contains `{1,7}`; box 3 already contains `{2,5,9}`. Trying `'1'`: `cols[5][0]` is true (1 is used in column 5) → conflict, skip. Trying `'3'`: none of the three structures contain it → place it, mark all three, recurse into `(4,6)`.

If that recursive call eventually returns `true` — every later cell filled successfully — the `if (backtrack(...)) return true;` line propagates that success immediately back through `(4,5)`, then through whatever called `(4,5)`, all the way to the original call, without any further alternative branches ever being attempted. If instead some *later* cell exhausts every digit without success, it returns `false`, `(4,5)`'s `'3'` gets undone, and `'4'` gets tried in its place.

**Complexity:** exponential in the absolute worst case, but constraint propagation prunes this enormously — well-formed puzzles solve quickly because the three tracking structures eliminate almost every branch almost immediately. Space O(1) for the fixed-size tracking arrays, O(81) recursion depth worst case.

**Common mistake:** undoing the board character on backtrack but forgetting to also undo the `rows`/`cols`/`boxes` markers — leaving stale "this digit is used" flags that incorrectly block valid placements in sibling branches.

---

## Problem — Word Search (LeetCode 79)

**Statement.** Given a grid and a single target word, return true if the word can be built from sequentially adjacent cells (no cell reused within one attempt).

This is the single-word predecessor to Word Search II (Chapter 9's hardest Trie problem) — worth seeing on its own because it's the *pure* backtracking mechanism, mark-explore-restore, with no Trie machinery layered on top. It's the cleanest version of that discipline in the entire book.

```java
public boolean exist(char[][] board, String word) {
    int rows = board.length, cols = board[0].length;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (dfs(board, r, c, word, 0)) {
                return true;
            }
        }
    }
    return false;
}

private boolean dfs(char[][] board, int r, int c, String word, int index) {
    if (index == word.length()) return true;
    if (r < 0 || r >= board.length || c < 0 || c >= board[0].length) return false;
    if (board[r][c] != word.charAt(index)) return false;

    char original = board[r][c];
    board[r][c] = '#';   // mark visited FOR THIS PATH ONLY

    boolean found = dfs(board, r + 1, c, word, index + 1)
                 || dfs(board, r - 1, c, word, index + 1)
                 || dfs(board, r, c + 1, word, index + 1)
                 || dfs(board, r, c - 1, word, index + 1);

    board[r][c] = original;   // BACKTRACK — restore unconditionally, regardless of outcome

    return found;
}
```

**Why this is the cleanest "mark, explore, restore" in the book.** No Trie, no constraint sets — just one cell marked, four directions tried via short-circuiting `||` (the instant one direction succeeds, the rest are never even attempted), and the cell restored unconditionally before returning. Word Search II is this *exact* mechanism, walking a Trie alongside the board instead of one fixed target string, and searching for many words at once instead of one.

**Trace** on `board=[['A','B','C','E'],['S','F','C','S'],['A','D','E','E']]`, `word="ABCCED"` — following only the successful path (every other direction is tried and discarded via the short-circuit, exactly like any other backtracking search):

```
(0,0)='A' matches word[0]. mark '#'.
  → right (0,1)='B' matches word[1]. mark '#'.
    → right (0,2)='C' matches word[2]. mark '#'.
      → down (1,2)='C' matches word[3]. mark '#'.
        → down (2,2)='E' matches word[4]. mark '#'.
          → left (2,1)='D' matches word[5]. mark '#'.
            → index now equals word.length() (6) → SUCCESS, return true immediately

true propagates all the way back up through every restore, short-circuiting every `||`
along the way — none of the other three directions at any level ever get tried once
one of them has already returned true.
```

**Final result:** `true`. Every cell gets restored to its original character on the way back out, regardless of outcome — restoration is unconditional, not reserved for the failure path.

**Complexity:** O(rows · cols · 4^L) worst case, L = word length. Space O(L) for the recursion stack.

**Common mistake:** restoring the cell only inside the failure branch, not on success too. For *this* problem (which just returns a boolean) that particular slip happens to be harmless — but the identical bug in Word Search II, which needs the board correctly restored between multiple independent starting searches, would silently corrupt every search that runs afterward.

---

## Problem — Palindrome Partitioning (LeetCode 131)

**Statement.** Partition a string so every piece is a palindrome. Return every possible partitioning.

**Approach.** At each starting position, try every possible end position for the next piece; if it's a palindrome, recurse on the remainder. Reaching the end of the string means the partition built so far is complete and valid.

```java
public List<List<String>> partition(String s) {
    List<List<String>> result = new ArrayList<>();
    backtrack(s, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(String s, int start, List<String> current, List<List<String>> result) {
    if (start == s.length()) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int end = start + 1; end <= s.length(); end++) {
        String substr = s.substring(start, end);
        if (isPalindrome(substr)) {
            current.add(substr);
            backtrack(s, end, current, result);
            current.remove(current.size() - 1);
        }
    }
}

private boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) return false;
        left++; right--;
    }
    return true;
}
```

**Trace** on `s="aab"`:

```
start=0:
  "a" (0,1) → palindrome → choose
    start=1: "a" (1,2) → palindrome → choose
      start=2: "b" (2,3) → palindrome → choose
        start=3 == length → RECORD ["a","a","b"]
    start=1: "ab" (1,3) → NOT palindrome → skip
  "aa" (0,2) → palindrome → choose
    start=2: "b" (2,3) → palindrome → choose
      start=3 == length → RECORD ["aa","b"]
  "aab" (0,3) → NOT palindrome → skip

Final: [["a","a","b"], ["aa","b"]]   ✓   the only two valid partitionings of "aab"
```

**Complexity (unmemoized):** O(n · 2ⁿ) worst case — up to 2ⁿ cut-point combinations, each piece costing up to O(n) to palindrome-check. Space O(n) recursion depth.

**The "memo" this problem is named for.** `isPalindrome` gets called repeatedly on overlapping substrings across different branches of the recursion. Precompute it **once**, for *every* possible substring, with a 2D table: `isPalin[i][j] = true` if `s[i..j]` is a palindrome — built with the *identical* expand-from-the-inside-out recurrence as Chapter 10's palindrome DP: `isPalin[i][j] = (s[i]==s[j]) && (j-i < 2 || isPalin[i+1][j-1])`. Backtracking still explores the same set of partitions; every individual validity check just becomes O(1) instead of an O(n) scan.

```java
public List<List<String>> partition(String s) {
    int n = s.length();
    boolean[][] isPalin = new boolean[n][n];
    for (int i = n - 1; i >= 0; i--) {
        for (int j = i; j < n; j++) {
            isPalin[i][j] = (s.charAt(i) == s.charAt(j)) && (j - i < 2 || isPalin[i + 1][j - 1]);
        }
    }

    List<List<String>> result = new ArrayList<>();
    backtrack(s, 0, isPalin, new ArrayList<>(), result);
    return result;
}

private void backtrack(String s, int start, boolean[][] isPalin, List<String> current, List<List<String>> result) {
    if (start == s.length()) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int end = start; end < s.length(); end++) {
        if (isPalin[start][end]) {   // O(1) lookup instead of an O(n) scan
            current.add(s.substring(start, end + 1));
            backtrack(s, end + 1, isPalin, current, result);
            current.remove(current.size() - 1);
        }
    }
}
```

**Why `j - i < 2` guards the recursion, and what breaks without it.** For a length-1 substring (`i==j`) or length-2 substring (`j==i+1`), there's no valid "inner" substring to check — `isPalin[i+1][j-1]` would mean an index where the row exceeds the column, a cell the fill loop (which only ever fills `j >= i`) never wrote to. Without the short-circuit, reading that cell would silently fall back to its default `false`, incorrectly marking a genuinely valid 2-character palindrome (like `"aa"`) as not one.

**Complexity (memoized):** building the table is O(n²) time and space. The backtracking enumeration itself still dominates at up to O(2ⁿ) in the worst case, but every individual check inside it is now O(1) instead of O(n) — a much smaller constant factor per branch, even though the overall complexity class doesn't change.

---

## Common Mistakes — Chapter-Wide

- **Forgetting the unchoose step, or restoring the wrong piece of state.** The single most common backtracking bug in this entire chapter — it corrupts every sibling branch explored afterward.
- **Mixing up `i` vs. `i+1` in the recursive call** when reuse should or shouldn't be allowed — Combination Sum's unlimited reuse vs. Combination Sum II/III's at-most-once.
- **Getting the duplicate-skip condition backward in Permutations II** — `!used[i-1]`, not `used[i-1]` — and treating it as something to memorize rather than derive.
- **Checking conflicts via O(n) scans instead of maintaining O(1)-lookup tracking structures** (N-Queens' three sets, Sudoku's rows/cols/boxes) — both correct, but the gap compounds across a large search tree.
- **Forgetting to restore tracking structures, not just the visible board/array**, on backtrack — leaving stale state that incorrectly blocks valid future placements.
- **Recomputing each substring's palindrome status from scratch inside the loop**, skipping the precomputed table — still correct, just needlessly slower; the table *is* the "memo" the problem's name refers to.
- **Checking a recursive call's return value without acting on it in existence-search backtracking** (Sudoku) — `if (backtrack(...)) return true;` has to happen at *every* level for the short-circuit to actually propagate.

## Pattern Recognition Guide

- "Generate all subsets/combinations/permutations" → Choose-Explore-Unchoose, varying only how the loop advances (same index for reuse, `i+1` for none) and what gets skipped for duplicates.
- "Input may have duplicates, output must not" → sort, then skip a candidate equal to the previous one *at the same recursive level* — recurring across Subsets II, Permutations II, Combination Sum II.
- "Sum to a target," reuse allowed → stay at the same index (Combination Sum I). Reuse forbidden → advance to `i+1` (Combination Sum II).
- "Place items on a board with no two conflicting" → N-Queens' shape: eliminate one constraint by construction (one queen per row), track the rest with O(1) sets.
- "Fill a constrained grid to a single valid solution" → Sudoku's shape: existence search with immediate short-circuit, not exhaustive enumeration.
- "Search a grid for a path matching a sequence" → mark-visited/explore/restore — Word Search's mechanism, and exactly what Word Search II builds on top of a Trie.
- "Partition a sequence so every piece satisfies a property" → backtracking over cut points, usually paired with a precomputed table so each piece's validity check is O(1) instead of recomputed from scratch every time.

## Chapter Summary

- Backtracking is DFS with one non-negotiable extra step: undo every choice before trying its sibling. The unchoose line is what makes backtracking backtracking, not a stylistic nicety.
- Subsets, Permutations, and their duplicate-handling variants differ only in how the loop advances and what gets explicitly skipped — four problems, one template, two small knobs.
- Combination Sum I → II → III is a guided tour of how pruning conditions accumulate: reuse-or-not changes the recursive index, sorted input turns a `continue` into a `break`, and a fixed required count adds a second, independent prune condition alongside the sum check.
- N-Queens and Sudoku both replace O(n) conflict-scanning with O(1)-lookup tracking structures — the same trade Chapter 5's HashMap made, applied here to backtracking's choice-validation step instead of array lookups.
- Sudoku's existence search (find the *one* valid completion, short-circuit immediately) is structurally different from every other problem in this chapter (find *every* valid completion, keep exploring regardless) — recognizing which shape a problem wants changes whether the function accumulates into a list or returns a boolean that propagates upward.
- Word Search is the cleanest possible illustration of mark-explore-restore in this book — one cell, four directions, an unconditional restore on the way out, nothing else competing for attention.
- Palindrome Partitioning's "memo" is a precomputed O(n²) table answering "is this substring a palindrome" in O(1), built with the same expand-from-the-inside recurrence as Chapter 10's palindrome DP — backtracking still explores the identical set of partitions, but every check along the way becomes instant.
