---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 6 — Trees"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, trees, terminology, fundamentals]
---

# Tree Terminology and Properties

Trees are the natural structure for hierarchical relationships. A **balanced** tree gives $O(\log n)$ search, insert, and delete. An unbalanced tree degrades to $O(n)$ — effectively a linked list.

## Terminology
- **Root:** The topmost node; the only node with no parent.
- **Leaf:** A node with no children.
- **Depth:** Number of edges from the root *down* to a node. (Root depth = 0).
- **Height:** Number of edges on the longest *downward* path from a node to a leaf. (Leaf height = 0, Tree height = Root height).

## Structural Properties
- **Perfect:** Every level is completely full, and every leaf is at the same depth.
- **Complete:** Every level is full except possibly the last, and the last level fills from left to right.
- **Balanced:** For every node, the heights of its left and right subtrees differ by at most 1.
- **Degenerate:** A tree where each parent has only one child. It performs like a linked list (Height is $O(n)$).
