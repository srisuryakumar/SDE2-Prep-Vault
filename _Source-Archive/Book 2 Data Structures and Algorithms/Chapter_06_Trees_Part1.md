# Chapter 6: Trees
## Part 1 — Traversals · The Recursive DFS Template

*This chapter has one big idea underneath all nine of its problems: ask "what does this node need from its children, and what does it hand back to its parent?" Answer that once per problem, and the rest of the code writes itself.*

## 6.1 Binary Tree Structure

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

```
                4
              /   \
             2     7
            / \   / \
           1   3 6   9
```

## 6.2 Tree Terminology

- **Root** — the topmost node (`4` above); the only node with no parent.
- **Leaf** — a node with no children (`1, 3, 6, 9` above).
- **Depth of a node** — number of edges from the root down to that node. Root has depth 0; `2` and `7` have depth 1; the leaves have depth 2.
- **Height of a node** — number of edges on the longest downward path from that node to a leaf. The root's height is 2; every leaf's height is 0. **Height of the tree** = height of the root.
- **Perfect** — every level is completely full, every leaf at the same depth.
  ```
          1
        /   \
       2     3
      / \   / \
     4   5 6   7
  ```
- **Complete** — every level full except possibly the last, and the last level fills left to right.
  ```
          1
        /   \
       2     3
      / \   /
     4   5 6
  ```
- **Balanced** — for every node, the heights of its left and right subtrees differ by at most 1. (This is the strict per-node definition; Section 6.5's Application 2 uses exactly this.)
- **Degenerate / unbalanced** — a tree that's really a linked list wearing a disguise:
  ```
  1
   \
    2
     \
      3
       \
        4
  ```
  Height 3 for only 4 nodes. This is precisely why an unbalanced BST's operations degrade to O(n) — see Section 6.6.

## 6.3 Why Trees

Hierarchical relationships are everywhere — file systems, org charts, parsers, the DOM — and trees are the natural structure for them. The practical payoff: a **balanced** tree gives O(log n) search, insert, and delete, because height (not node count) is what determines how many comparisons those operations need, and a balanced tree's height is O(log n). An unbalanced tree gives no better than O(n) — no improvement at all over a plain linked list. Balance isn't a nice-to-have refinement; it's the entire reason self-balancing trees (red-black trees, AVL trees — what `TreeMap`/`TreeSet` use internally in Java) exist.

## 6.4 DFS Traversals — Recursive and Iterative

### Inorder (Left → Root → Right)

```java
public void inorder(TreeNode node, List<Integer> result) {
    if (node == null) return;
    inorder(node.left, result);
    result.add(node.val);
    inorder(node.right, result);
}
```

On the example tree: `1, 2, 3, 4, 6, 7, 9` — sorted order. That's not a coincidence for this particular tree; it's a BST, and inorder traversal of any BST always produces sorted output (proven in Section 6.6).

**Iterative inorder** — go as far left as possible (pushing along the way), pop, visit, then move right:

```java
public List<Integer> inorderIterative(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {            // dive as far left as possible
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();               // leftmost unvisited node
        result.add(curr.val);
        curr = curr.right;                // then explore its right subtree
    }
    return result;
}
```

**Condensed trace** on the example tree: dive left pushing `[4, 2, 1]`, pop `1` (visit, no right child) → pop `2` (visit, go right to `3`) → push `3`, pop `3` (visit) → pop `4` (visit, go right to `7`) → push `7, 6`, pop `6` (visit) → pop `7` (visit, go right to `9`) → push `9`, pop `9` (visit). Result: `1, 2, 3, 4, 6, 7, 9` — identical to the recursive version, confirming the mechanics.

### Preorder (Root → Left → Right)

```java
public void preorder(TreeNode node, List<Integer> result) {
    if (node == null) return;
    result.add(node.val);
    preorder(node.left, result);
    preorder(node.right, result);
}
```

On the example tree: `4, 2, 1, 3, 7, 6, 9`. Because preorder visits the root *before* either child, reading the sequence left to right tells you the root immediately — this is exactly why preorder is the basis for tree serialization and reconstruction later in this chapter.

**Iterative preorder** — push right before left, so left pops (and is processed) first:

```java
public List<Integer> preorderIterative(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    if (root == null) return result;
    Deque<TreeNode> stack = new ArrayDeque<>();
    stack.push(root);
    while (!stack.isEmpty()) {
        TreeNode node = stack.pop();
        result.add(node.val);
        if (node.right != null) stack.push(node.right);   // pushed first
        if (node.left != null) stack.push(node.left);      // pushed second → popped first
    }
    return result;
}
```

### Postorder (Left → Right → Root)

```java
public void postorder(TreeNode node, List<Integer> result) {
    if (node == null) return;
    postorder(node.left, result);
    postorder(node.right, result);
    result.add(node.val);
}
```

On the example tree: `1, 3, 2, 6, 9, 7, 4`. Postorder visits both children fully before the node itself — exactly the dependency order needed for deleting a tree (children must be freed before their parent) or evaluating an expression tree (operands must be computed before the operator combining them).

**Iterative postorder** is the trickiest of the three. The cleanest approach: do preorder with left and right *swapped* (push left before right, so right pops first), which produces Root→Right→Left order — then reverse the whole result at the end. Reversed Root-Right-Left is exactly Left-Right-Root.

```java
public List<Integer> postorderIterative(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    if (root == null) return result;
    Deque<TreeNode> stack = new ArrayDeque<>();
    stack.push(root);
    while (!stack.isEmpty()) {
        TreeNode node = stack.pop();
        result.add(node.val);
        if (node.left != null) stack.push(node.left);     // swapped vs. preorder
        if (node.right != null) stack.push(node.right);
    }
    Collections.reverse(result);   // Root-Right-Left, reversed, = Left-Right-Root
    return result;
}
```

**Trace** on the example tree: visiting in Root-Right-Left order produces `4, 7, 9, 6, 2, 3, 1`. Reversed: `1, 3, 2, 6, 9, 7, 4` — exactly matching the recursive postorder above.

### Level-Order (BFS with a Queue)

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int levelSize = queue.size();    // snapshot — exactly how many nodes belong to THIS level
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

**The one line that matters:** `int levelSize = queue.size();` captured *before* the inner loop starts. Children get enqueued during that loop, so without snapshotting the count first, you'd lose track of exactly where one level ends and the next begins.

**Trace** on the example tree:

```
queue=[4], levelSize=1 → poll 4, enqueue 2,7.                     level=[4]
queue=[2,7], levelSize=2 → poll 2 (enqueue 1,3), poll 7 (enqueue 6,9).   level=[2,7]
queue=[1,3,6,9], levelSize=4 → poll all four, no children to enqueue.    level=[1,3,6,9]

Final: [[4], [2,7], [1,3,6,9]]   ✓
```

This *is* the solution to **Binary Tree Level Order Traversal (LeetCode 102)** — there's no additional step needed beyond what's shown here.

---

## 6.5 The Recursive DFS Template

**The key question, asked at every node:** what information does this node need *from* its children to compute its own answer, and what does it *return* to its parent? Answer that once, and the code follows a fixed shape:

```java
ReturnType solve(TreeNode node) {
    if (node == null) return /* base case value */;
    ReturnType leftResult = solve(node.left);
    ReturnType rightResult = solve(node.right);
    // combine leftResult, rightResult, and node.val into this node's answer
    return /* combined result */;
}
```

This is Chapter 3's "trust the recursion" lesson, applied to trees: assume the recursive calls already correctly answer the question for the left and right subtrees. Your only job at the current node is combining those two answers with the node's own value. Four applications below change only the base case and the combine step — the skeleton itself never moves.

### Application 1 — Max Depth of Binary Tree (LeetCode 104)

**What does a node need from its children? What does it return?** The depth of each subtree; it returns 1 + the larger of the two (the `+1` is the edge connecting this node down to its taller child).

```java
public int maxDepth(TreeNode node) {
    if (node == null) return 0;
    int left = maxDepth(node.left);
    int right = maxDepth(node.right);
    return 1 + Math.max(left, right);
}
```

On the example tree: leaves return 1; nodes `2` and `7` return `1 + max(1,1) = 2`; the root returns `1 + max(2,2) = 3`.

**Complexity:** Time O(n). Space O(h) for the call stack.

### Application 2 — Balanced Binary Tree (LeetCode 110)

**What does a node need?** Whether each subtree is itself balanced, *and* each subtree's height (needed to check this node's own balance: `|leftHeight − rightHeight| ≤ 1`). **What does it return?** Its height — but it also needs to signal "already found unbalanced below," and folding that into the same return value (rather than a separate pass) is what keeps this O(n) instead of O(n²).

```java
public boolean isBalanced(TreeNode root) {
    return checkHeight(root) != -1;
}

private int checkHeight(TreeNode node) {
    if (node == null) return 0;
    int left = checkHeight(node.left);
    if (left == -1) return -1;                  // already unbalanced below — short-circuit upward
    int right = checkHeight(node.right);
    if (right == -1) return -1;
    if (Math.abs(left - right) > 1) return -1;   // this node itself is unbalanced
    return 1 + Math.max(left, right);            // otherwise, the real height
}
```

**Why the sentinel matters:** without folding "found unbalanced" into the height's own return value, you'd need a separate height computation at every node to check its balance — and since height itself requires visiting the whole subtree, that's O(n) work repeated at every one of O(n) nodes, giving O(n²) overall. The `-1` sentinel keeps everything in one O(n) pass.

**Complexity:** Time O(n). Space O(h).

### Application 3 — Diameter of Binary Tree (LeetCode 543)

**Statement.** The diameter is the length (in edges) of the longest path between *any* two nodes — it may or may not pass through the root.

**What does a node need?** Each subtree's height (to compute the longest path *through* this node: `leftHeight + rightHeight`). **What does it return?** Its own height, same as Application 1 — but along the way, it updates a running global best, because the true longest path in the whole tree might live entirely inside one subtree, never touching the current node or the root at all.

```java
private int maxDiameter = 0;

public int diameterOfBinaryTree(TreeNode root) {
    height(root);
    return maxDiameter;
}

private int height(TreeNode node) {
    if (node == null) return 0;
    int left = height(node.left);
    int right = height(node.right);
    maxDiameter = Math.max(maxDiameter, left + right);   // best path THROUGH this node
    return 1 + Math.max(left, right);                     // height handed UP to the parent
}
```

**Why a side-effect variable, not a return value:** the function's return value is needed by the *parent*, for the parent's own height calculation. It can't simultaneously also carry "the best diameter seen anywhere in the tree so far" — that's a fundamentally different piece of information. An instance variable (or, equivalently, a small wrapper object holding both values) is the standard resolution. This exact tension reappears, in its hardest form, at the end of this chapter in Max Path Sum.

**Complexity:** Time O(n). Space O(h).

### Application 4 — Path Sum (LeetCode 112, Root-to-Leaf)

**Statement.** Given a target sum, return true if some root-to-leaf path sums to exactly that target.

**What does a node need?** Whether *either* child can complete the remaining sum down to a leaf. **What does it return?** A boolean.

```java
public boolean hasPathSum(TreeNode node, int targetSum) {
    if (node == null) return false;
    if (node.left == null && node.right == null) {     // leaf: does it complete the sum?
        return node.val == targetSum;
    }
    int remaining = targetSum - node.val;
    return hasPathSum(node.left, remaining) || hasPathSum(node.right, remaining);
}
```

This is a deliberate variation on the pure template — the "combine" step is a boolean OR across children rather than an arithmetic combination — to make the point that the template is a *shape* (base case → recurse on children → combine), not a rigid formula. "Combine" can be any function of the children's results and the current node's value.

**Complexity:** Time O(n) worst case. Space O(h).

---

## Problem — Lowest Common Ancestor of a Binary Tree (LeetCode 236)

**Statement.** Given a tree and two nodes `p` and `q`, find their lowest common ancestor (the deepest node having both as descendants — a node counts as its own descendant).

**Approach.** Direct application of the template. If the current node *is* `p` or `q`, return it immediately — found one of the two targets. Otherwise recurse into both children. If *both* children return something non-null, `p` and `q` live in different subtrees and this node is exactly where their paths meet — it's the LCA. If only *one* side returns non-null, propagate it upward (either the LCA is further up, or that side already found both targets itself). If neither side finds anything, return null.

```java
public TreeNode lowestCommonAncestor(TreeNode node, TreeNode p, TreeNode q) {
    if (node == null || node == p || node == q) {
        return node;
    }
    TreeNode left = lowestCommonAncestor(node.left, p, q);
    TreeNode right = lowestCommonAncestor(node.right, p, q);

    if (left != null && right != null) {
        return node;                              // found in different subtrees — this IS the LCA
    }
    return (left != null) ? left : right;          // propagate whichever side found something
}
```

**Trace** — finding `LCA(1, 3)` on the example tree (`4` root, `2`/`7` children, `1, 3, 6, 9` leaves):

```
call(4): recurse both sides.
  call(2): recurse both sides.
    call(1): node == p → return 1.
    call(3): node == q → return 3.
    left=1, right=3, both non-null → return 2 (this node IS the LCA for the left subtree's search)
  call(7): neither p nor q found anywhere below → returns null.
left=2 (non-null), right=null → propagate left → return 2.

Final LCA(1, 3) = node 2   ✓  (correct: 2 is the direct parent of both 1 and 3)
```

**Complexity:** Time O(n) worst case. Space O(h).

---

*Part 2 covers BST properties (search, insert, the inorder-is-sorted invariant), Validate BST, Kth Smallest in BST, Construct Binary Tree from Preorder and Inorder, Serialize/Deserialize, and closes with Binary Tree Maximum Path Sum — the hardest tree problem in the book.*
