---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 6 — Trees"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, trees, bst, properties]
---

# Binary Search Tree Properties

## The BST Invariant
For every node, every value in its left subtree is less than the node's value, and every value in its right subtree is greater.

**Direct consequence:** An inorder traversal (Left $\rightarrow$ Root $\rightarrow$ Right) of a BST *always* visits nodes in sorted order.

## Search and Insert
- **Search:** Compare target with root. If smaller, go left. If larger, go right.
- **Insert:** Follow the same invariant down to the correct empty spot, and attach there.

**Complexity:** $O(\log n)$ average case (balanced tree). $O(n)$ worst case (degenerate tree / linked list in disguise).

## Problem: Kth Smallest Element in a BST
Since an inorder traversal visits nodes in sorted order, the $k$-th smallest is simply the $k$-th node visited.
Reuse the iterative inorder template and add an early-exit counter to avoid walking the rest of the tree once the answer is found.
**Complexity:** Time $O(h + k)$ (worst case $O(n)$), Space $O(h)$.
