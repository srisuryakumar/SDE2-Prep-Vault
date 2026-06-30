---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 6 — Trees"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, trees, pattern, bst-validation]
---

# Validating a BST Pattern

## Intuition
To determine if a binary tree is a valid BST, **you cannot just check a node against its immediate parent.** 
A node might be valid compared to its parent, but violate the bounds set by a more distant ancestor (e.g., a right child of a left child might be larger than the root).

**The correct approach:** Pass a valid `(lower, upper)` bound down through the recursion. 
- Every node must fall strictly inside its inherited bound. 
- Going left tightens the *upper* bound to the current node's value. 
- Going right tightens the *lower* bound.

## Template
```java
public boolean isValidBST(TreeNode root) {
    // Use Long.MIN_VALUE / MAX_VALUE so that a node with Integer.MIN_VALUE doesn't fail
    return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
}

private boolean validate(TreeNode node, long lower, long upper) {
    if (node == null) return true;
    
    if (node.val <= lower || node.val >= upper) return false;
    
    return validate(node.left, lower, node.val) && validate(node.right, node.val, upper);
}
```
**Complexity:** $O(n)$ time, $O(h)$ space.
