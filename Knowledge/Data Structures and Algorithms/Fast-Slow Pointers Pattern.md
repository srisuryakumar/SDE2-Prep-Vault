---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 3 — Linked Lists"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, linked-lists, pattern, fast-slow-pointers, cycle-detection]
---

# Fast-Slow Pointers Pattern

## 1. Find the Middle
Move `slow` one step and `fast` two steps. When `fast` reaches the end, `slow` is at the middle.
```java
ListNode slow = head, fast = head;
// To land on the SECOND middle (e.g., node 3 of 1-2-3-4):
while (fast != null && fast.next != null) { ... }
// To land on the FIRST middle (e.g., node 2 of 1-2-3-4):
while (fast.next != null && fast.next.next != null) { ... }
```

## 2. Detect a Cycle (Floyd's Algorithm)
If a cycle exists, `fast` is guaranteed to land exactly on `slow`. The gap between them increases by exactly 1 (mod cycle length) each step, so it cannot skip over 0.
```java
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow == fast) return true;
}
return false;
```

## 3. Find the Cycle Entry Point
When `slow` and `fast` meet in Floyd's algorithm, let `a` be the distance to the cycle start, `b` be the meeting point distance inside the cycle, and `C` be the cycle length.
Algebra proves: `a ≡ (C - b) (mod C)`.
This means if you put a new pointer at `head` (needs `a` steps) and leave one at the meeting point (needs `C - b` steps to finish the lap), moving both one step at a time guarantees they will meet exactly at the cycle start.

```java
// After slow == fast:
ListNode ptr1 = head;
ListNode ptr2 = slow;
while (ptr1 != ptr2) {
    ptr1 = ptr1.next;
    ptr2 = ptr2.next;
}
return ptr1; // Cycle entry point
```
