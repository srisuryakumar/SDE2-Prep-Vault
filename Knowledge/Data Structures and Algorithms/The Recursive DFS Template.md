---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 6 — Trees"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, trees, pattern, dfs, recursion]
---

# The Recursive DFS Template

For recursive tree problems, ask exactly one question at every node: **What information does this node need *from* its children to compute its own answer, and what does it *return* to its parent?**

## Template Shape
Assume the recursive calls already correctly answer the question for the subtrees.
```java
ReturnType solve(TreeNode node) {
    if (node == null) return /* base case */;
    ReturnType leftResult = solve(node.left);
    ReturnType rightResult = solve(node.right);
    return /* combination of leftResult, rightResult, and node.val */;
}
```

## Application 1: Max Depth
- **Needs from children:** Depth of each subtree.
- **Returns:** `1 + Math.max(left, right)`.

## Application 2: Balanced Binary Tree
- **Needs from children:** Is it balanced? What is its height?
- **Returns:** The height, OR a sentinel value (`-1`) to short-circuit upward if unbalanced. Folding "found unbalanced" into the height return value keeps it $O(n)$ instead of $O(n^2)$.
```java
private int checkHeight(TreeNode node) {
    if (node == null) return 0;
    int left = checkHeight(node.left);
    if (left == -1) return -1; // Short-circuit
    // ... same for right
    if (Math.abs(left - right) > 1) return -1;
    return 1 + Math.max(left, right);
}
```

## Application 3: Diameter of Binary Tree
- **Needs from children:** Height of each subtree.
- **Returns:** Its own height (`1 + Math.max(left, right)`).
- **Side Effect:** Update a global/instance variable `maxDiameter = Math.max(maxDiameter, left + right)` since the true longest path might not pass through the root.

## Application 4: Path Sum (Root-to-Leaf)
- **Needs from children:** Can either child complete the remaining sum?
- **Returns:** Boolean.
- **Combination:** `hasPathSum(node.left, remaining) || hasPathSum(node.right, remaining)`
