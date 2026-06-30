---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 11 — Backtracking"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, backtracking, sudoku, existence-search]
---

# Sudoku Solver Pattern

## Intuition
Fill a 9x9 Sudoku board. Unlike other backtracking problems that find *all* solutions, Sudoku has a unique answer, so we want to find **exactly one** solution and short-circuit.

We use **constraint propagation** with three boolean arrays (`rows`, `cols`, `boxes`) so that validity checks are $O(1)$ instead of an $O(9)$ scan.

## Template
```java
public void solveSudoku(char[][] board) {
    boolean[][] rows = new boolean[9][9];
    boolean[][] cols = new boolean[9][9];
    boolean[][] boxes = new boolean[9][9];

    // Pre-fill tracking arrays with existing board state
    for (int r = 0; r < 9; r++) {
        for (int c = 0; c < 9; c++) {
            if (board[r][c] != '.') {
                int d = board[r][c] - '1';
                rows[r][d] = cols[c][d] = boxes[boxIndex(r, c)][d] = true;
            }
        }
    }
    backtrack(board, 0, 0, rows, cols, boxes);
}

private int boxIndex(int r, int c) {
    return (r / 3) * 3 + (c / 3);
}

private boolean backtrack(char[][] board, int r, int c, boolean[][] rows, boolean[][] cols, boolean[][] boxes) {
    if (r == 9) return true; // Solved
    if (c == 9) return backtrack(board, r + 1, 0, rows, cols, boxes); // Next row
    if (board[r][c] != '.') return backtrack(board, r, c + 1, rows, cols, boxes); // Skip filled

    int box = boxIndex(r, c);
    for (char digitChar = '1'; digitChar <= '9'; digitChar++) {
        int d = digitChar - '1';
        if (rows[r][d] || cols[c][d] || boxes[box][d]) continue; // Prune

        // CHOOSE
        board[r][c] = digitChar;
        rows[r][d] = cols[c][d] = boxes[box][d] = true;

        // EXPLORE (Existence Search: Short-circuit if true)
        if (backtrack(board, r, c + 1, rows, cols, boxes)) {
            return true; 
        }

        // UNCHOOSE (Don't forget to undo the tracking arrays!)
        board[r][c] = '.';
        rows[r][d] = cols[c][d] = boxes[box][d] = false;
    }
    return false; // No digit worked, trigger backtrack
}
```
