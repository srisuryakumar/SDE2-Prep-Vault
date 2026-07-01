---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 5 — Hash Maps and Hash Sets"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, hash-map, complement-lookup]
---

# Complement Lookup Pattern

## Intuition
For "find two elements that sum to a target", a brute force check takes $O(n^2)$. 
The complement-lookup insight is to ask: "For the current element $x$, have I already seen `target - x`?" 
If yes, you found the pair in $O(1)$. 
One pass, building the seen-set **incrementally**, turns $O(n^2)$ into $O(n)$.

**Why incrementally?** If you build the entire seen-set first, you risk matching an element against itself when `target = 2x`, or using values from the future. Checking the map *before* inserting naturally avoids this.

## Template
```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>(); // value -> index
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{-1, -1};
}
```

## The Prefix Sum Connection
**Subarray Sum Equals K** is exactly the Complement Lookup pattern, just applied to running prefix sums instead of raw array elements!
`prefix[i] = prefix[j+1] - k` is structurally identical to `complement = target - nums[i]`. Recognizing this connection allows you to solve a whole family of problems using the exact same HashMap template.
