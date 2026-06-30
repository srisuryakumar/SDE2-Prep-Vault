---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, greedy, jump-game]
---

# Greedy Simplifications of DP (Jump Game)

Not every DP-shaped problem needs the full DP machinery. Sometimes, "tracking every position's state" can be collapsed into a single rolling value using a greedy approach.

## Jump Game I (Reachability)
`nums[i]` is max jump length. Can you reach the last index?
- **Naive DP:** $O(n^2)$. `dp[i]` is true if some `j < i` is reachable and `j + nums[j] >= i`.
- **Greedy Collapse:** $O(n)$. Track the *farthest* reachable position seen so far. If your current index `i` exceeds `farthest`, you are trapped.

```java
public boolean canJump(int[] nums) {
    int farthest = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > farthest) return false; // Stuck!
        farthest = Math.max(farthest, i + nums[i]);
    }
    return true;
}
```

## Jump Game II (Minimum Jumps)
Minimize jumps to reach the last index.
- **Greedy Collapse:** Think in terms of "jump levels" (like BFS). Keep track of the `currentEnd` (boundary of the current jump level). Once your scan reaches `currentEnd`, the level is exhausted—increment your jump count and set the boundary to the `farthest` reach found within that level.

```java
public int jump(int[] nums) {
    int jumps = 0, currentEnd = 0, farthest = 0;
    for (int i = 0; i < nums.length - 1; i++) { // No need to jump FROM the last index
        farthest = Math.max(farthest, i + nums[i]);
        if (i == currentEnd) {
            jumps++;
            currentEnd = farthest;
        }
    }
    return jumps;
}
```
