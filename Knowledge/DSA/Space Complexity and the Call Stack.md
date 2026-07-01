---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 1 — Algorithmic Thinking and Complexity Analysis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, complexity, space-complexity]
---

# Space Complexity and the Call Stack

Space complexity asks how memory scales with input size $n$.
We almost always care about **auxiliary space**: extra memory your algorithm allocates, *not counting the input itself*.

## The Silent Memory Hog: The Call Stack
The most commonly forgotten contributor to space complexity is the recursion stack. A recursive function that recurses to depth $d$ uses **$O(d)$** space for stack frames, even if it never explicitly allocates a single array or object.

```java
public int depth(TreeNode node) {
    if (node == null) return 0;
    return 1 + Math.max(depth(node.left), depth(node.right));
}
```
This is $O(h)$ space, where $h$ is the tree's height. 
- For a balanced tree, $h = O(\log n)$.
- For a degenerate tree (a linked list in disguise), $h = O(n)$.

**Rule of Thumb:** A recursive solution is almost never $O(1)$ space. State the stack space explicitly during interviews.
