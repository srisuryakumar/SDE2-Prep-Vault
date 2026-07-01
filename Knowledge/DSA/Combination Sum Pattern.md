---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 11 — Backtracking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, backtracking, combinations]
---

# Combination Sum Pattern

## Combination Sum I (Unlimited Reuse)
Given distinct positive integers and a target, find all unique combinations summing to target. The same number may be reused unlimited times.
**The Trick:** Recurse while staying at the *same* index `i` (because reuse is unlimited).

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, target, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] candidates, int remaining, int start, List<Integer> current, List<List<Integer>> result) {
    if (remaining == 0) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = start; i < candidates.length; i++) {
        if (candidates[i] > remaining) continue; // Prune
        
        current.add(candidates[i]);
        backtrack(candidates, remaining - candidates[i], i, current, result); // SAME i (reuse allowed)
        current.remove(current.size() - 1);
    }
}
```

## Combination Sum II (No Reuse, Contains Duplicates)
Each number used *at most once*.
**The Trick:** 
1. Sort the array.
2. If `candidates[i] > remaining`, `break` (since it's sorted, all subsequent will also overshoot).
3. Add duplicate check: `if (i > start && candidates[i] == candidates[i - 1]) continue;`
4. Recurse with `i + 1` (no reuse).

## Combination Sum III (Fixed Count and Range)
Find combinations of exactly $k$ numbers, using only 1–9, summing to $n$.
**The Trick:** The success check needs *both* `remaining == 0` AND `current.size() == k`.
**Pruning:** `if (current.size() == k || remaining <= 0) return;` stops a branch the instant *either* constraint is violated.

```java
private void backtrack(int k, int remaining, int start, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == k && remaining == 0) {
        result.add(new ArrayList<>(current));
        return;
    }
    if (current.size() == k || remaining <= 0) return; // PRUNE early
    
    for (int i = start; i <= 9; i++) {
        current.add(i);
        backtrack(k, remaining - i, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```
