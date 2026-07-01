---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, top-down, memoization]
---

# Word Break Pattern (Top-Down DP)

## Intuition
Given a string `s` and a dictionary of words, return true if `s` can be fully segmented into dictionary words.

This is a classic problem for **Top-Down DP (Memoization)**.
Define `canBreak(start)` = true if `s[start..]` can be fully segmented.
We try every possible end position for the first word. If that prefix is a dictionary word *and* `canBreak(end)` is true, we succeed.

**Why memoization is essential:** Different recursive paths can reach the *same* starting position multiple times. Without a memo, the time complexity blows up exponentially ($O(2^n)$) on adversarial inputs.

## Template
```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> wordSet = new HashSet<>(wordDict);
    Map<Integer, Boolean> memo = new HashMap<>(); // Cache for `start` index
    return canBreak(s, 0, wordSet, memo);
}

private boolean canBreak(String s, int start, Set<String> wordSet, Map<Integer, Boolean> memo) {
    if (start == s.length()) return true;
    if (memo.containsKey(start)) return memo.get(start);

    for (int end = start + 1; end <= s.length(); end++) {
        String prefix = s.substring(start, end);
        if (wordSet.contains(prefix) && canBreak(s, end, wordSet, memo)) {
            memo.put(start, true);
            return true;
        }
    }
    
    memo.put(start, false);
    return false;
}
```
**Complexity:** $O(n^3)$ worst-case time with memoization. (Where $n$ is string length: $O(n)$ start states $\times$ $O(n)$ end positions $\times$ $O(n)$ substring cost). Space $O(n)$ for memo map and recursion stack.
