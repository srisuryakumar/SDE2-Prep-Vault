---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 6 — Trees"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, trees, lca, pattern]
---

# Lowest Common Ancestor Pattern

## Intuition
Given a tree and two nodes `p` and `q`, find their lowest common ancestor (the deepest node having both as descendants — a node can be a descendant of itself).

Apply the recursive DFS template.
- If the current node is `null`, `p`, or `q`, return it immediately.
- Otherwise, recurse into both children.
- If *both* children return non-null, it means `p` and `q` live in different subtrees. Therefore, **this node is the LCA**.
- If only *one* side returns non-null, propagate it upward. This means either the LCA is further up, or that side already found both targets and is passing the LCA up.
- If neither side finds anything, return `null`.

## Template
```java
public TreeNode lowestCommonAncestor(TreeNode node, TreeNode p, TreeNode q) {
    // Base case: null, or found one of the targets
    if (node == null || node == p || node == q) {
        return node;
    }
    
    TreeNode left = lowestCommonAncestor(node.left, p, q);
    TreeNode right = lowestCommonAncestor(node.right, p, q);

    // If both left and right found a target, this node is the LCA!
    if (left != null && right != null) {
        return node;                              
    }
    
    // Otherwise, propagate whichever side found something
    return (left != null) ? left : right;          
}
```
**Complexity:** $O(n)$ time worst case, $O(h)$ space for the recursion stack.
