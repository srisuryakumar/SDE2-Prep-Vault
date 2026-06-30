---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 12 — Advanced Patterns"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, bit-manipulation]
---

# Bit Manipulation Patterns

## XOR Trick (Find Single Number)
Given an array where every element appears twice except one, find the single element.
**Trick:** `x ^ x = 0`. XORing the entire array cancels out all duplicates, leaving only the single element.
```java
public int singleNumber(int[] nums) {
    int result = 0;
    for (int num : nums) result ^= num;
    return result;
}
```

## Popcount (Counting Set Bits) - Brian Kernighan's Algorithm
Count the number of `1` bits in an integer.
**Trick:** `n & (n - 1)` clears the **lowest set bit**. 
Repeating this runs exactly $O(k)$ times, where $k$ is the number of set bits.
```java
public int popcount(int n) {
    int count = 0;
    while (n != 0) {
        n = n & (n - 1);
        count++;
    }
    return count;
}
```

## Power of Two Check
Powers of 2 have exactly ONE set bit (`1=001`, `2=010`, `4=100`, `8=1000`).
If we clear that bit with `n & (n-1)`, the result should be 0.
```java
public boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```
