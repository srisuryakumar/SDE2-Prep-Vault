---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, string-dp]
---

# String DP Pattern

## Intuition
String DP compares two strings `word1` and `word2`. 
- **State:** `dp[i][j]` represents the answer for the prefixes `word1[0..i-1]` and `word2[0..j-1]`.
- **Recurrence:** If `word1[i-1] == word2[j-1]`, we generally inherit from `dp[i-1][j-1]` (the diagonal). Otherwise, we look at `dp[i-1][j]` (drop from word1) and `dp[i][j-1]` (drop from word2).
- **Base cases:** `dp[0][j]` and `dp[i][0]` handle comparisons with an empty string.

## 1. Longest Common Subsequence
Return the length of the longest common subsequence between `text1` and `text2`.
- **Recurrence:**
  If match: `dp[i][j] = dp[i-1][j-1] + 1`
  If mismatch: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

```java
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}
```

## 2. Edit Distance
Minimum operations (insert, delete, replace) to convert `word1` into `word2`.
- **Base cases:** `dp[0][j] = j` (insert $j$ times), `dp[i][0] = i` (delete $i$ times).
- **Recurrence:**
  If match: `dp[i][j] = dp[i-1][j-1]` (0 cost)
  If mismatch: `dp[i][j] = 1 + min(dp[i-1][j-1] /*replace*/, dp[i-1][j] /*delete*/, dp[i][j-1] /*insert*/)`

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));
            }
        }
    }
    return dp[m][n];
}
```
