---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 11 — Backtracking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, backtracking, subsets, duplicates]
---

# Subsets Pattern (I & II)

## Subsets I (No Duplicates)
Build subsets by choosing a starting index and deciding, for each index from there onward, whether to add it.
**Notice:** Every recursive call represents a valid subset, so add it to the result at the *start* of the function.

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current)); // Record every state

    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

## Subsets II (With Duplicates)
If the input has duplicates, we want to return unique subsets only.
**The Fix:**
1. **Sort** the input array first.
2. In the `for` loop, if `i > start && nums[i] == nums[i-1]`, **skip it**.
This treats identical values at the *same recursive depth* as interchangeable, preventing redundant branches, while still allowing duplicates to be picked sequentially across *different depths* (e.g., forming `[2, 2]`).

```java
public List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums); // Crucial!
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current));

    for (int i = start; i < nums.length; i++) {
        if (i > start && nums[i] == nums[i - 1]) continue; // Skip duplicate at THIS LEVEL

        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```
