---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 11 — Backtracking"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, backtracking, n-queens, hard]
---

# N-Queens Pattern

## Intuition
Place $n$ queens on an $n \times n$ board so no two attack each other.
Instead of an $O(N)$ scan to check conflicts for every placed queen, we can make conflict checking **$O(1)$** using three Sets:
- `cols`: Occupied columns.
- `diag1`: Occupied main diagonals (`row - col` is constant).
- `diag2`: Occupied anti-diagonals (`row + col` is constant).

We place queens **one row at a time**, which automatically guarantees no two queens ever share a row.

## Template
```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    int[] queens = new int[n]; // queens[row] = column of the queen
    backtrack(0, n, queens, new HashSet<>(), new HashSet<>(), new HashSet<>(), result);
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
        // O(1) conflict check
        if (cols.contains(col) || diag1.contains(d1) || diag2.contains(d2)) {
            continue; 
        }

        // CHOOSE
        queens[row] = col;
        cols.add(col); diag1.add(d1); diag2.add(d2);

        // EXPLORE
        backtrack(row + 1, n, queens, cols, diag1, diag2, result);

        // UNCHOOSE
        cols.remove(col); diag1.remove(d1); diag2.remove(d2);
    }
}
```
