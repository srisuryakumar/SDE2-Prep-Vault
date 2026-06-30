---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 9 — Trie"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, trie, backtracking, hard]
---

# Trie with Backtracking Pattern

## Intuition
Used for problems like **Word Search II**, where you need to find every word from a dictionary that can be constructed on a 2D board of letters.
Searching independently for each word is $O(\text{words} \times \text{cells} \times 4^L)$.
**The Fix:** Insert **every** word into a single Trie. Then run **one** combined DFS over the board, walking the board path and the Trie path *simultaneously*. Any path that doesn't match the start of *any* word in the Trie dies immediately (pruned for free).

## Template (Word Search II)
Modify the TrieNode to store the complete string `word` at the end node. This avoids needing to pass a StringBuilder down the recursion stack.

```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    String word = null; // non-null exactly at the node completing a word
}

// DFS Step
private void dfs(char[][] board, int r, int c, TrieNode node, List<String> result) {
    if (r < 0 || r >= board.length || c < 0 || c >= board[0].length) return;
    
    char ch = board[r][c];
    if (ch == '#' || node.children[ch - 'a'] == null) return; // visited or no matching prefix
    
    TrieNode next = node.children[ch - 'a'];
    if (next.word != null) {
        result.add(next.word);
        next.word = null; // prevent adding the same word twice
    }

    board[r][c] = '#'; // Mark visited for THIS path only
    dfs(board, r + 1, c, next, result);
    dfs(board, r - 1, c, next, result);
    dfs(board, r, c + 1, next, result);
    dfs(board, r, c - 1, next, result);
    board[r][c] = ch;  // BACKTRACK - restore so a different search path can reuse this cell
}
```

## Why Backtracking is Essential Here
Unlike simple flood-fill (e.g., Number of Islands) where a visited cell belongs to exactly one component permanently, a cell here can legitimately participate in *multiple different candidate words* starting from different neighbors. You MUST restore `board[r][c] = ch` at the end of the `dfs` call.
