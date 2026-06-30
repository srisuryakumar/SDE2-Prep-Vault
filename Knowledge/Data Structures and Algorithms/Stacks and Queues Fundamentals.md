---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 4 — Stacks and Queues"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, stack, queue, fundamentals]
---

# Stacks and Queues Fundamentals

## Stack — LIFO (Last In, First Out)
- **Use when:** Undoing the most recent action fixes the problem. "What came before", backtracking, matching brackets, explicit DFS.
- **Java Implementation:** Use `ArrayDeque`, not `java.util.Stack`. `Stack` is synchronized and slow. `ArrayDeque` is backed by a resizable circular array (amortized $O(1)$).
```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); // Add to top
stack.pop();   // Remove and return top
stack.peek();  // Look at top without removing
```

## Queue — FIFO (First In, First Out)
- **Use when:** Strict arrival order matters. "First come, first served", Breadth-First Search (BFS), level-order traversal, task scheduling.
- **Java Implementation:** `ArrayDeque` implements both `Deque` and `Queue`.
```java
Deque<Integer> queue = new ArrayDeque<>();
queue.offer(1); // Add to back
queue.poll();   // Remove and return front
queue.peek();   // Look at front without removing
```

## Classic Problem: Valid Parentheses
Push opening brackets onto a stack. When a closing bracket appears, it must match the top of the stack (pop it). At the end, the stack must be completely empty.
