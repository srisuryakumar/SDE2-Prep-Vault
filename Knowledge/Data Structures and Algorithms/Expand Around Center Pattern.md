---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, strings, palindromes]
---

# Expand Around Center Pattern

## Intuition
Used for finding the **Longest Palindromic Substring**.
A natural DP exists (`dp[i][j] = true` if `s[i..j]` is palindrome), but it requires $O(n^2)$ space.
Instead, we can exploit the fact that every palindrome has a center, and we can expand outward from it. This achieves the same $O(n^2)$ time with only **$O(1)$ space**.

There are $2n - 1$ possible centers:
- $n$ single-character centers (odd-length palindromes)
- $n - 1$ between-character centers (even-length palindromes)

## Template
```java
public String longestPalindrome(String s) {
    if (s.length() < 1) return "";
    int start = 0, maxLen = 1;

    for (int center = 0; center < s.length(); center++) {
        int len1 = expandFromCenter(s, center, center);       // odd-length center
        int len2 = expandFromCenter(s, center, center + 1);   // even-length center
        int len = Math.max(len1, len2);
        
        if (len > maxLen) {
            maxLen = len;
            start = center - (len - 1) / 2;
        }
    }
    return s.substring(start, start + maxLen);
}

private int expandFromCenter(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return right - left - 1;
}
```
**Common Mistakes:** Forgetting to check even-length centers! A palindrome like "abba" has no single center character, it centers between the 'b's.
