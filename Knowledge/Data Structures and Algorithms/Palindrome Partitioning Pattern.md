---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 11 — Backtracking"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, backtracking, palindromes, memoization]
---

# Palindrome Partitioning Pattern

## Intuition
Partition a string so every piece is a palindrome. Return every possible partitioning.
This requires Backtracking to try every cut point, plus **Memoization (DP)** to precompute the palindrome status of every substring in $O(1)$ time, avoiding an $O(n)$ check on every recursive branch.

## Template
```java
public List<List<String>> partition(String s) {
    int n = s.length();
    // Precompute palindrome status for all substrings in O(n^2)
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
        if (isPalin[start][end]) { // O(1) lookup!
            current.add(s.substring(start, end + 1));
            backtrack(s, end + 1, isPalin, current, result);
            current.remove(current.size() - 1);
        }
    }
}
```

**Why `j - i < 2` guards the DP recurrence:** For a length-1 or length-2 substring, there's no valid "inner" substring to check. `isPalin[i+1][j-1]` would mean an index where row exceeds column, reading uninitialized default `false` data.
