---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 12 — Advanced Patterns"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, monotonic-deque, sliding-window, hard]
---

# Monotonic Deque Pattern

## Intuition
Used for problems like **Sliding Window Maximum**, where you need the max/min of a sliding window in $O(n)$ time.
A plain monotonic stack can only pop from one end, which is insufficient because elements in a sliding window can expire for two reasons:
1. A bigger element arrives (invalidating smaller elements).
2. An element simply **ages out** of the window.

A **Monotonic Deque** (Double-ended queue) solves this by allowing $O(1)$ pops from both ends. We store *indices*, keeping the values strictly decreasing from front to back. The front is always the current window's maximum.

## Template (Sliding Window Maximum)
```java
public int[] maxSlidingWindow(int[] nums, int k) {
    Deque<Integer> deque = new ArrayDeque<>(); // stores INDICES
    int[] result = new int[nums.length - k + 1];
    int resultIdx = 0;

    for (int i = 0; i < nums.length; i++) {
        // 1. Pop from BACK if current element is larger (they can never be the max again)
        while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[i]) {
            deque.pollLast();
        }
        deque.offerLast(i);

        // 2. Pop from FRONT if the max element has aged out of the window
        if (deque.peekFirst() <= i - k) {
            deque.pollFirst();
        }

        // 3. Record max when window is full
        if (i >= k - 1) {
            result[resultIdx++] = nums[deque.peekFirst()];
        }
    }
    return result;
}
```
**Complexity:** $O(n)$ time since each index is pushed and popped at most once. $O(k)$ space for the deque.
