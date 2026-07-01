---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 4 — Stacks and Queues"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, monotonic-stack]
---

# Monotonic Stack Pattern

## Intuition
A monotonic stack keeps its elements in sorted order (either increasing or decreasing, read bottom to top) by **popping off anything that would violate that order** when a new element arrives.
Every pop is informative: when element X is popped because new element Y broke the order, Y is the answer for X (either the next greater or next smaller element).

**Why it's $O(n)$:** A `while` loop inside a `for` loop looks $O(n^2)$, but every element is pushed exactly once and popped at most once. Total pops $\le$ total pushes $\le n$.

## Decreasing Stack $\rightarrow$ "Next Greater Element"
Values decrease bottom to top. When a new element is *larger*, order is broken. The new element is the "next greater element" for everything it pops.

```java
// Subroutine for Next Greater Element array
public int[] nextGreaterElement(int[] arr) {
    int[] result = new int[arr.length];
    Arrays.fill(result, -1);
    Deque<Integer> stack = new ArrayDeque<>(); // stores indices
    
    for (int i = 0; i < arr.length; i++) {
        while (!stack.isEmpty() && arr[stack.peek()] < arr[i]) {
            int idx = stack.pop();
            result[idx] = arr[i]; // arr[i] is the next greater element!
        }
        stack.push(i);
    }
    return result;
}
```
**Problems:** Next Greater Element, Daily Temperatures.

## Increasing Stack $\rightarrow$ "Next Smaller Element"
Values increase bottom to top. When a new element is *smaller*, order is broken. The new element is the "next smaller element".

**Problem: Largest Rectangle in Histogram.**
An increasing stack of indices finds both the left and right boundaries for the largest rectangle using each bar as the limiting height.
- **Right boundary:** The new shorter bar that causes the pop.
- **Left boundary:** The new top of the stack *after* the pop.
- **CRITICAL:** Add a sentinel bar of height 0 at the end (index $n$) to force the stack to flush and resolve all remaining bars.
