---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["[[Rate Limiting Algorithms]]", ]
tags: [dsa, pattern, sliding-window]
---

# Sliding Window Pattern - Variable Size

## Intuition
Instead of a rigid size $k$, many problems have a *condition*: "longest substring without repeating characters", "smallest subarray summing to target". The window still has a left and right boundary, but they move according to the condition.

**The invariant:** The window always satisfies (or is working toward satisfying) the problem's condition. 
- **Maximizing:** Expand (move right) until the condition breaks, then shrink (move left) until it's restored. Update result *every step*.
- **Minimizing:** Expand until the condition is met, record the current answer, then shrink to see if you can do better while still meeting the condition.

## Template
```java
public static int slidingWindowVariable(int[] arr) {
    int left = 0, result = 0; // or Integer.MAX_VALUE for minimization
    // Window state: e.g., Map<Character, Integer> freq, int sum

    for (int right = 0; right < arr.length; right++) {
        // 1. Expand: include arr[right] in the window state

        // 2. Shrink: while condition is violated, remove arr[left]
        while (/* condition is violated */) {
            // remove arr[left] from window state
            left++;
        }

        // 3. Window [left..right] satisfies the condition
        // Update result
        result = Math.max(result, right - left + 1);
    }
    return result;
}
```

## Why it's O(n)
Each element is added to the window once (when `right` passes it) and removed at most once (when `left` passes it). The inner `while` loop runs at most $n$ times *across all iterations* of the outer loop. Total work = $O(n)$.

## Classic Problems
- **Longest Substring Without Repeating Characters:** Track `lastSeen` index in a HashMap. If `s[right]` was seen inside the current window, jump `left` to `lastSeen[c] + 1`.
- **Minimum Window Substring:** Use a `have` and `need` map/count. Expand until `have == required`, record length, then shrink to minimize.
- **Longest Repeating Character Replacement:** Condition is `(window length) - maxFreq <= k`. If violated, advance `left`. (For this specific problem, an `if` instead of `while` works to shrink because we only care about finding a *larger* window, but `while` is the general pattern).

## Related Concepts
- See also [[Rate Limiting Algorithms]] for the rate limiter implementation behind token bucket.
