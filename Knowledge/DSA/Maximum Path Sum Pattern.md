---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 6 — Trees"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, trees, pattern, path-sum, hard]
---

# Maximum Path Sum Pattern

## Intuition
Find the maximum sum of any path in a binary tree. The path does not need to pass through the root and doesn't need to end at a leaf.

**Why this is hard:** Two ideas pull in opposite directions:
1. **What gets returned to the parent:** A path that can still be *extended upward*. This can only include the current node plus the better of its **two** children (a path cannot fork upward).
2. **The global best path:** Might be a "V" shape (left child $\rightarrow$ node $\rightarrow$ right child). This is perfectly valid, but it can never be extended any further up.

## The Two Values Computed at Every Node
- **Returned to parent:** `node.val + max(0, leftGain, rightGain)`. The `max(0, ...)` clamps negative gains to 0 (meaning "don't extend into this child").
- **Global best candidate:** `node.val + max(0, leftGain) + max(0, rightGain)`. This uses **both** children at once.

## Template
```java
private int maxSum = Integer.MIN_VALUE;

public int maxPathSum(TreeNode root) {
    maxGain(root);
    return maxSum;
}

private int maxGain(TreeNode node) {
    if (node == null) return 0;

    // Negative gains are worthless to carry forward — clamp to 0
    int leftGain = Math.max(maxGain(node.left), 0);
    int rightGain = Math.max(maxGain(node.right), 0);

    // Candidate for the GLOBAL best — a path using BOTH children at once
    int throughNode = node.val + leftGain + rightGain;
    maxSum = Math.max(maxSum, throughNode);

    // What gets RETURNED to the parent — only ONE side, since a path can't fork upward
    return node.val + Math.max(leftGain, rightGain);
}
```
**Complexity:** $O(n)$ time, $O(h)$ space.
