---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 11 — Backtracking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, backtracking, word-search, grids]
---

# Word Search Pattern

## Intuition
Given a grid and a target word, return true if the word can be built from sequentially adjacent cells (no cell reused).
This is the purest form of **Mark $\rightarrow$ Explore $\rightarrow$ Restore** backtracking.

## Template
```java
public boolean exist(char[][] board, String word) {
    for (int r = 0; r < board.length; r++) {
        for (int c = 0; c < board[0].length; c++) {
            if (dfs(board, r, c, word, 0)) return true;
        }
    }
    return false;
}

private boolean dfs(char[][] board, int r, int c, String word, int index) {
    if (index == word.length()) return true; // Success!
    if (r < 0 || r >= board.length || c < 0 || c >= board[0].length) return false;
    if (board[r][c] != word.charAt(index)) return false;

    char original = board[r][c];
    board[r][c] = '#'; // Mark visited FOR THIS PATH ONLY

    // Explore 4 directions, short-circuiting on success
    boolean found = dfs(board, r + 1, c, word, index + 1)
                 || dfs(board, r - 1, c, word, index + 1)
                 || dfs(board, r, c + 1, word, index + 1)
                 || dfs(board, r, c - 1, word, index + 1);

    // RESTORE UNCONDITIONALLY
    board[r][c] = original; 

    return found;
}
```

**Common Mistake:** Restoring the cell *only* inside the failure branch. It must be restored unconditionally, regardless of outcome, so that other searches starting from different locations can properly reuse the cell.
