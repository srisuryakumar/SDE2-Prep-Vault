---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 6 — Trees"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, trees, traversals, dfs, bfs]
---

# Tree Traversals (DFS and BFS)

## DFS Traversals (Recursive)
1. **Inorder (Left $\rightarrow$ Root $\rightarrow$ Right):** Produces sorted output for a Binary Search Tree (BST).
2. **Preorder (Root $\rightarrow$ Left $\rightarrow$ Right):** Visits the root first. Useful for tree serialization and reconstruction.
3. **Postorder (Left $\rightarrow$ Right $\rightarrow$ Root):** Visits children before their parent. Useful for deleting a tree or evaluating an expression tree.

## DFS Traversals (Iterative)
To do it iteratively, manage an explicit stack (`Deque`).
- **Inorder:** Push all the way left. Pop, visit, go right.
- **Preorder:** Push root. Pop, visit, push **right child**, push **left child** (so left pops first).
- **Postorder:** Do preorder with left and right swapped (Root $\rightarrow$ Right $\rightarrow$ Left), then reverse the output list at the end.

## BFS Traversal (Level-Order)
Use a Queue. The key is snapshotting the `queue.size()` at the start of each level loop.

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);
    
    while (!queue.isEmpty()) {
        int levelSize = queue.size();  // CRITICAL: Snapshot size before inner loop
        List<Integer> level = new ArrayList<>();
        
        for (int i = 0; i < levelSize; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}
```
