---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, decoding]
---

# Decode Ways Pattern

## Intuition
Given a string of digits representing letters (`A=1`...`Z=26`), count the number of ways to decode it.
This is another Linear DP, but the validity of combinations determines whether `dp[i-1]` or `dp[i-2]` get added.

- **State:** `dp[i]` = ways to decode first $i$ characters.
- **Recurrence:** `dp[i]` accumulates from two sources:
  1. The single last digit (`s[i-1]`) can stand alone if it's not `'0'` $\rightarrow$ add `dp[i-1]`.
  2. The last two digits can stand together if they form a number from $10$ to $26$ $\rightarrow$ add `dp[i-2]`.
- **Base cases:** `dp[0]=1` (empty string). `dp[1] = 1` if `s[0] != '0'` else `0`.

```java
public int numDecodings(String s) {
    int n = s.length();
    if (s.charAt(0) == '0') return 0;
    int[] dp = new int[n + 1];
    dp[0] = 1; dp[1] = 1;

    for (int i = 2; i <= n; i++) {
        char first = s.charAt(i - 2), second = s.charAt(i - 1);

        if (second != '0') {
            dp[i] += dp[i - 1]; // Single digit
        }
        
        int twoDigit = (first - '0') * 10 + (second - '0');
        if (twoDigit >= 10 && twoDigit <= 26) {
            dp[i] += dp[i - 2]; // Double digit
        }
    }
    return dp[n];
}
```
**Common Mistakes:** Forgetting that `twoDigit >= 10` is essential to prevent treating `06` as a valid letter `F`.

**Space Optimization:** This can be optimized to $O(1)$ space using `prev1` and `prev2`, just like Fibonacci.
