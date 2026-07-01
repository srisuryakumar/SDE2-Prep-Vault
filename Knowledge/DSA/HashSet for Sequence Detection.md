---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 5 — Hash Maps and Hash Sets"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, hash-set, sequence-detection]
---

# HashSet for Sequence Detection

## Problem: Longest Consecutive Sequence
Given an unsorted array of integers, find the length of the longest run of consecutive integers in $O(n)$ time. Sorting takes $O(n \log n)$, which is too slow.

## Intuition
Drop every number into a `HashSet` ($O(n)$). This automatically collapses duplicates.
For each number, only **start** counting a run if `num - 1` is *not* in the set (i.e., it is genuinely the start of a sequence).
If `num - 1` *is* in the set, some earlier number owns this run and will count it later.

For each true start, walk forward checking set membership to count the run length.

```java
public int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int num : nums) set.add(num);

    int longest = 0;
    for (int num : set) {
        if (!set.contains(num - 1)) {   // ONLY count forward from a true start
            int length = 1;
            int curr = num;
            while (set.contains(curr + 1)) {
                curr++;
                length++;
            }
            longest = Math.max(longest, length);
        }
    }
    return longest;
}
```

## Why this is $O(n)$
Every number is only ever the start of a count-forward walk once. Non-starts are skipped entirely. Every number is visited by the inner `while` loop at most once across the entire algorithm. The total work is $O(n)$, not $O(n^2)$.

**Common Mistake:** Forgetting the `!set.contains(num - 1)` start check. The algorithm still produces the correct answer, but degrades to $O(n^2)$ if there is a single long consecutive run, causing timeouts on large tests.
