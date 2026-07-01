---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 12 — Advanced Patterns"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [dsa, pattern, strings, kmp, hard]
---

# KMP String Matching Pattern

## Intuition
Find every occurrence of a pattern string in a text string.
The naive approach takes $O(n \cdot m)$ by resetting the comparison on every mismatch.
**Knuth-Morris-Pratt (KMP)** uses a failure function (LPS array) to skip redundant comparisons, bringing the time down to **$O(n + m)$**.

## LPS Array (Longest Prefix Suffix)
The LPS array precomputes: `lps[i]` = length of the longest proper prefix of `pattern[0..i]` that is also a suffix of it.
If we mismatch at `pattern[j]`, we know the characters before $j$ matched perfectly. The LPS array tells us where to jump the $j$ pointer back to, *without moving the $i$ pointer in the text backwards*.

## Template (Find First Occurrence)
```java
public int strStr(String haystack, String needle) {
    if (needle.isEmpty()) return 0;
    int n = haystack.length(), m = needle.length();
    
    int[] lps = buildLPS(needle);
    
    int i = 0; // haystack pointer
    int j = 0; // needle pointer
    
    while (i < n) {
        if (haystack.charAt(i) == needle.charAt(j)) {
            i++; j++;
            if (j == m) return i - m; // Found!
        } else if (j > 0) {
            j = lps[j - 1]; // Mismatch: fallback via LPS. Note `i` does NOT move.
        } else {
            i++; // Fallback exhausted, advance `i`
        }
    }
    return -1;
}

private int[] buildLPS(String pattern) {
    int m = pattern.length();
    int[] lps = new int[m];
    int len = 0;
    int i = 1;
    
    while (i < m) {
        if (pattern.charAt(i) == pattern.charAt(len)) {
            lps[i++] = ++len;
        } else if (len > 0) {
            len = lps[len - 1]; // fallback
        } else {
            lps[i++] = 0;
        }
    }
    return lps;
}
```
