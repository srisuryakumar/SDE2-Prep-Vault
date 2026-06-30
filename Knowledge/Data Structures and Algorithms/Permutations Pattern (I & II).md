---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 11 — Backtracking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, backtracking, permutations, duplicates, hard]
---

# Permutations Pattern (I & II)

## Permutations I (No Duplicates)
Unlike Subsets (which only moves a starting index forward), a permutation needs every element available at *every* position—just not reused within the same permutation. Use a `boolean[] used` array.

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, new boolean[nums.length], new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue; // Skip if already in the permutation

        used[i] = true;
        current.add(nums[i]);
        backtrack(nums, used, current, result);
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```

## Permutations II (With Duplicates)
If the input has duplicates, we must avoid generating identical permutations.
**The Fix:**
1. **Sort** the input array first.
2. The trickiest check in Backtracking: `if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;`

**Why `!used[i - 1]`?** 
Think of duplicate values having a strict left-to-right priority. Only use the leftmost *unused* occurrence of a repeated value at the same recursive depth. 
If `nums[i] == nums[i-1]` and `!used[i-1]` is true, it means the earlier identical value is sitting available *at this exact depth level*. Choosing the *later* occurrence instead generates the exact same subtree redundantly. Skip it!

```java
public List<List<Integer>> permuteUnique(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, new boolean[nums.length], new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        // The Key Skip Condition
        if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue; 

        used[i] = true;
        current.add(nums[i]);
        backtrack(nums, used, current, result);
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```
