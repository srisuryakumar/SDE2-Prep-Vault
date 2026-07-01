---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 1 — Algorithmic Thinking and Complexity Analysis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, complexity, big-o, derivation]
---

# Deriving Complexity From Code

You must be able to read code and output its complexity in seconds.

## 1. Single Loop → $O(n)$
A loop running $n$ times doing $O(1)$ work per iteration is $O(n)$.
```java
for (int i = 0; i < arr.length; i++) { total += arr[i]; }
```

## 2. Nested Loops → $O(n^2)$ (Usually)
**Trap:** "Nested" doesn't automatically mean quadratic. It's quadratic only if the inner loop's bound depends on $n$.
- **Classic:** `for(i=0..n) for(j=0..n)` → $O(n^2)$
- **Shrinking:** `for(i=0..n) for(j=i+1..n)` → $O(n^2)$ (triangular number $n(n-1)/2$ is still quadratic).
- **Constant Bound:** `for(i=0..n) for(j=i..min(i+3, n))` → $O(n)$ (inner loop runs max 3 times!).

## 3. Halving Each Step → $O(\log n)$
If you throw away half the search space every iteration (e.g., Binary Search), it takes $\log_2(n)$ steps to reach 1 element.
```java
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    // ... update lo or hi to mid
}
```

## 4. Branching Recursion → $O(2^n)$
If each recursive call spawns two more calls (e.g., naive Fibonacci), the call tree doubles at each level. Total nodes in a tree of depth $n$ is roughly $2^n$.

## 5. Sort Then Scan → $O(n \log n)$
Sorting costs $O(n \log n)$. A linear scan after costs $O(n)$. 
$O(n \log n) + O(n) = O(n \log n)$ (larger wins).
