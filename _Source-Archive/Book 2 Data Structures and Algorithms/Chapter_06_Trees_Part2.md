# Chapter 6: Trees
## Part 2 — BST Properties · Construction · Serialization · Maximum Path Sum

## 6.6 BST Properties and Operations

**The BST invariant.** For every node, every value in its left subtree is less than the node's value, and every value in its right subtree is greater. The direct consequence: **inorder traversal of a BST always visits nodes in sorted order.** This follows by induction from the traversal itself — `inorder(left)` visits everything less than the current node, then the node's own value is visited, then `inorder(right)` visits everything greater. If that holds recursively for every subtree (and the base case, an empty tree, is trivially "sorted"), it holds for the whole tree.

**Search:**

```java
public TreeNode search(TreeNode node, int target) {
    if (node == null || node.val == target) return node;
    return target < node.val ? search(node.left, target) : search(node.right, target);
}
```

**Insert** — follow the same invariant down to the correct empty spot, and attach there:

```java
public TreeNode insert(TreeNode node, int val) {
    if (node == null) return new TreeNode(val);
    if (val < node.val) {
        node.left = insert(node.left, val);
    } else {
        node.right = insert(node.right, val);
    }
    return node;
}
```

Both operations are **O(log n) average** (balanced tree, height ~log n) and **O(n) worst case** (a degenerate tree — Section 6.2's "linked list in disguise" — where height is n). This is precisely why height, not node count, is the number that actually determines performance.

---

## Problem — Validate Binary Search Tree (LeetCode 98)

**Statement.** Determine whether a given binary tree is a valid BST.

**Why "check each node against only its immediate parent" is wrong.** Consider root `5`, left child `3`, and `3`'s right child `6`. Locally, every parent-child pair looks fine: `3 < 5` ✓ at the root; `6 > 3` ✓ at node `3`. But `6` sits in the **left** subtree of `5`, so it's required to be less than `5` — and `6 > 5`. A check that only ever compares a node to its immediate parent never sees this violation, because the violation is against an *ancestor*, not the parent.

**The correct approach.** Pass a valid `(lower, upper)` bound down through the recursion. Every node must fall strictly inside its inherited bound. Going left tightens the *upper* bound to the current node's value (everything in a left subtree must be less than it); going right tightens the *lower* bound.

```java
public boolean isValidBST(TreeNode root) {
    return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
}

private boolean validate(TreeNode node, long lower, long upper) {
    if (node == null) return true;
    if (node.val <= lower || node.val >= upper) return false;
    return validate(node.left, lower, node.val) && validate(node.right, node.val, upper);
}
```

(Bounds are `long`, not `int`, specifically so a node value sitting at `Integer.MIN_VALUE` or `MAX_VALUE` doesn't collide with the sentinel bounds themselves.)

**Trace** on the broken example (`5` root, left `3`, `3`'s right child `6`):

```
validate(5, -∞, +∞): 5 is within bounds.
  validate(3, -∞, 5): 3 is within bounds (< 5).
    validate(3.left=null, -∞, 3): true (empty).
    validate(6, 3, 5):  is 6 <= 3? No.  is 6 >= 5? YES → return false.
  3's right branch returned false → validate(3,...) returns false.
validate(5,...) returns false.

Final: INVALID — correctly catches the violation a parent-only check would have missed.
```

**Complexity:** Time O(n). Space O(h).

---

## Problem — Kth Smallest Element in a BST (LeetCode 230)

**Statement.** Find the kth smallest value in a BST.

**Approach.** Since inorder traversal of a BST visits nodes in sorted order (just proven above), the kth smallest is simply the kth node visited by an inorder traversal. Reuse the iterative inorder template from Section 6.4 verbatim, adding one early-exit counter — no need to walk the rest of the tree once the answer is found.

```java
public int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode curr = root;
    int count = 0;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        count++;
        if (count == k) return curr.val;   // stop the moment we've found it
        curr = curr.right;
    }
    return -1;   // unreachable given valid input
}
```

Notice how little of this is actually new — it's Section 6.4's iterative inorder traversal with a single `if` added. That's the payoff of internalizing the traversal templates properly: many "new" tree problems are a small delta on top of something you've already written.

**Complexity:** Time O(h + k) — descend to the leftmost node, then visit k nodes. Worst case O(n). Space O(h).

---

## Problem — Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105)

**Statement.** Given a tree's preorder and inorder traversal arrays (values unique), reconstruct the original tree.

**Why these two traversals together are enough.** Preorder's first element is *always* the root — root-left-right means root comes first, no exceptions. Once the root's value is known, find that same value in the inorder array: everything to its left in the inorder array belongs entirely to the left subtree, and everything to its right belongs entirely to the right subtree (because inorder is left-root-right, the root is exactly the dividing line). Apply the same logic recursively to each side.

**Approach.** A `HashMap<value, indexInInorder>` makes finding the split point O(1) instead of an O(n) scan every time. A shared, mutating pointer into the preorder array tracks which preorder value is the "next root" to consume.

```java
private int preorderIndex;
private Map<Integer, Integer> inorderIndexMap;

public TreeNode buildTree(int[] preorder, int[] inorder) {
    preorderIndex = 0;
    inorderIndexMap = new HashMap<>();
    for (int i = 0; i < inorder.length; i++) {
        inorderIndexMap.put(inorder[i], i);
    }
    return build(preorder, 0, inorder.length - 1);
}

private TreeNode build(int[] preorder, int inorderLeft, int inorderRight) {
    if (inorderLeft > inorderRight) return null;            // empty range — no subtree here

    int rootVal = preorder[preorderIndex++];                 // next unused preorder value IS the root
    TreeNode root = new TreeNode(rootVal);

    int mid = inorderIndexMap.get(rootVal);                   // where the root splits the inorder range
    root.left = build(preorder, inorderLeft, mid - 1);         // must fully finish before root.right runs
    root.right = build(preorder, mid + 1, inorderRight);
    return root;
}
```

**Why `root.left` must be fully built before `root.right` begins:** preorder lists root, then the *entire* left subtree, then the *entire* right subtree, in that order. `preorderIndex` is a single shared pointer — as long as the left subtree's recursive call consumes exactly its own share of preorder values before returning, the right subtree's call automatically starts at the correct next index. Evaluate them out of order, and values get assigned to the wrong nodes.

**Trace** on `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`:

```
build(0, 4):  rootVal = preorder[0] = 3.  mid = index of 3 in inorder = 1.
  root.left  = build(0, 0):   [inorder slice left of mid: just index 0 → value 9]
      rootVal = preorder[1] = 9.  empty children on both sides.  → TreeNode(9)
  root.right = build(2, 4):   [inorder slice right of mid: indices 2..4 → 15, 20, 7]
      rootVal = preorder[2] = 20.  mid = index of 20 in inorder = 3.
      root.left  = build(2, 2):  rootVal = preorder[3] = 15.  → TreeNode(15)
      root.right = build(4, 4):  rootVal = preorder[4] = 7.   → TreeNode(7)
      → TreeNode(20, left=15, right=7)
  → TreeNode(3, left=9, right=TreeNode(20,15,7))

Final tree:
        3
       / \
      9   20
         /  \
        15   7

Verify: preorder of this tree = 3,9,20,15,7  ✓   inorder = 9,3,15,20,7  ✓
```

**Complexity:** Time O(n) — the HashMap makes every split-point lookup O(1); each node is built exactly once. Space O(n) for the map and the recursion stack.

---

## Problem — Serialize and Deserialize Binary Tree (LeetCode 297)

**Statement.** Design an encoding from a binary tree to a string, and a matching decoder back to the original structure.

**Approach.** Use preorder traversal, but — this is the part that makes it work — explicitly record a `null` marker for every missing child. Without null markers, a bare preorder sequence is ambiguous: you can't tell where one subtree ends and the next begins (unlike the previous problem, which had a *second* traversal — inorder — to disambiguate). Recording nulls makes preorder self-sufficient: deserializing just reads tokens in the exact root-left-right order they were written, with each `null` token immediately closing off that branch.

```java
public String serialize(TreeNode root) {
    StringBuilder sb = new StringBuilder();
    serializeHelper(root, sb);
    return sb.toString();
}

private void serializeHelper(TreeNode node, StringBuilder sb) {
    if (node == null) {
        sb.append("null,");
        return;
    }
    sb.append(node.val).append(",");
    serializeHelper(node.left, sb);
    serializeHelper(node.right, sb);
}

public TreeNode deserialize(String data) {
    Queue<String> tokens = new ArrayDeque<>(Arrays.asList(data.split(",")));
    return deserializeHelper(tokens);
}

private TreeNode deserializeHelper(Queue<String> tokens) {
    String token = tokens.poll();
    if (token.equals("null")) {
        return null;
    }
    TreeNode node = new TreeNode(Integer.parseInt(token));
    node.left = deserializeHelper(tokens);     // consumed in the SAME order they were written
    node.right = deserializeHelper(tokens);
    return node;
}
```

**Trace** on a tree with root `1`, left leaf `2`, right leaf `3`:

```
serialize(1) = "1," + serialize(2) + serialize(3)
             = "1," + "2,null,null," + "3,null,null,"
             = "1,2,null,null,3,null,null,"

deserialize("1,2,null,null,3,null,null,"):
  tokens = [1, 2, null, null, 3, null, null]
  poll "1" → node(1)
    node.left  = deserialize: poll "2" → node(2); its left/right both poll "null" → null, null.
    node.right = deserialize: poll "3" → node(3); its left/right both poll "null" → null, null.
  → node(1) with left=node(2), right=node(3)   ✓ exact reconstruction
```

**Complexity:** Time O(n) for both directions. Space O(n) for the string/queue, plus O(h) recursion stack.

---

## Problem — Binary Tree Maximum Path Sum (LeetCode 124) — Hardest Tree Problem, Full Explanation

**Statement.** Find the maximum sum of any path in a binary tree. A path is any connected sequence of parent-child edges — it does **not** need to pass through the root, and does **not** need to end at a leaf. It can start and end anywhere.

**Why this is hard.** Two ideas pull in opposite directions. First: whatever value a node returns to its parent must represent a path that can still be *extended upward* — which means it can only include the current node plus the better of its **two** children, since the parent can only attach to one side, not both. Second: the actual best path in the whole tree might be exactly the shape that fact forbids — a "V," going down the left child, through the current node, and back down the right child. That V is a perfectly valid path; it simply can never be extended any further. This is the same return-value-vs-global-tracking tension from Diameter of Binary Tree (Part 1, Application 3), pushed to its hardest form.

**The two values computed at every node:**

- **What gets returned to the parent:** the best path starting at this node and extending downward into *at most one* child — `node.val + max(0, leftGain, rightGain)`. The `max(0, ...)` matters: if both children would only drag the sum down (all-negative subtrees below), the best this node can offer upward is just its own value, extending into neither child.
- **What gets compared against the global answer:** the best path *through* this node, allowed to use **both** children at once — `node.val + max(0, leftGain) + max(0, rightGain)`. This is only ever a candidate for the global maximum; it is never returned to the parent, because a path using both children can't be extended past this node.

```java
private int maxSum = Integer.MIN_VALUE;

public int maxPathSum(TreeNode root) {
    maxGain(root);
    return maxSum;
}

private int maxGain(TreeNode node) {
    if (node == null) return 0;

    // Negative gains are worthless to carry forward — clamp to 0 ("don't extend into this child")
    int leftGain = Math.max(maxGain(node.left), 0);
    int rightGain = Math.max(maxGain(node.right), 0);

    // Candidate for the GLOBAL best — a path using BOTH children at once
    int throughNode = node.val + leftGain + rightGain;
    maxSum = Math.max(maxSum, throughNode);

    // What gets RETURNED to the parent — only ONE side, since a path can't fork upward
    return node.val + Math.max(leftGain, rightGain);
}
```

**Trace** on a tree deliberately including a negative root, to show the clamping in action:

```
        -10
        /  \
       9    20
           /  \
          15    7
```

```
maxGain(9):    leaf. leftGain=0, rightGain=0.
               throughNode = 9.  maxSum = max(-∞, 9) = 9.
               return 9.

maxGain(15):   leaf. throughNode = 15.  maxSum = max(9, 15) = 15.
               return 15.

maxGain(7):    leaf. throughNode = 7.  maxSum stays 15.
               return 7.

maxGain(20):   leftGain = max(15, 0) = 15.   rightGain = max(7, 0) = 7.
               throughNode = 20+15+7 = 42.  maxSum = max(15, 42) = 42.
               return 20 + max(15,7) = 35.        ← only ONE side carried upward

maxGain(-10):  leftGain = max(9, 0) = 9.   rightGain = max(35, 0) = 35.
               throughNode = -10+9+35 = 34.  maxSum = max(42, 34) = 42 (unchanged —
                                                       the root's own path actually loses).
               return -10 + max(9,35) = 25.       (irrelevant — root has no parent)

Final maxSum = 42   — the path 15 → 20 → 7, entirely inside the right subtree,
                       never touching the root at all.   ✓
```

This trace **is** the point of the problem, made concrete: the best path doesn't pass through the root — including the root would have actively *reduced* the sum (`-10 + 9 + 35 = 34 < 42`). That's exactly why `maxSum` has to be tracked as a side effect across every node visited, not derived from whatever the top-level call happens to return.

**Complexity:** Time O(n). Space O(h).

---

## Common Mistakes — Chapter-Wide

- **Checking BST validity against only the immediate parent.** Misses violations against more distant ancestors. Always pass an inherited `(lower, upper)` bound down through the recursion instead.
- **Forgetting the early-exit in Kth Smallest in BST.** Without it, the answer is still correct, but the traversal needlessly continues through the rest of the tree after already finding it.
- **Letting the right subtree start building before the left subtree finishes**, in Construct from Preorder/Inorder. `preorderIndex` is one shared, mutating pointer; build order has to match consumption order exactly.
- **Serializing without null markers.** A bare preorder sequence alone is ambiguous about where one subtree ends — you need either explicit nulls or a second traversal (as in the Construct problem) to disambiguate.
- **Returning the "through this node" value instead of the "extend into one child" value**, in Diameter and Max Path Sum. The value handed to the parent must represent something that can still be extended by one more edge — a node cannot pass a V-shaped, both-children path up to its parent.
- **Forgetting to clamp negative gains to zero in Max Path Sum.** Without `Math.max(maxGain(child), 0)`, an all-negative subtree would actively subtract from a path that would have been better off ignoring that child entirely.

## Pattern Recognition Guide

- "Compute something that depends on a node's children" (depth, balance, diameter, any bottom-up aggregate) → the recursive DFS template: base case, recurse left, recurse right, combine.
- "A property that involves both children but can't be reported upward as-is" → track a global/instance-variable best *separately* from the value returned to the parent (Diameter, Max Path Sum).
- "Compare against ancestors, not just the immediate parent" → pass bounds down through the recursion (Validate BST).
- "The kth something, in sorted order, from a BST" → inorder traversal with an early-exit counter; the BST invariant guarantees inorder is already sorted.
- "Reconstruct a tree from traversal arrays" → preorder (or postorder) gives you the root; inorder tells you how to split into left/right subtrees around it.
- "Convert a tree to a string and back" → preorder with explicit null markers — nulls are what make the encoding unambiguous without a second traversal.
- "Process level by level," "shortest depth," "leftmost/rightmost node per depth" → BFS with a queue, snapshotting `queue.size()` before each level's inner loop.

## Chapter Summary

- A tree's height — not its node count — determines whether operations are O(log n) (balanced) or O(n) (degenerate). This single fact is the entire justification for self-balancing trees existing.
- Four DFS orders, two implementations each: inorder (sorted output for BSTs), preorder (root-first — the basis for serialization and reconstruction), postorder (children-before-parent — for deletion and expression evaluation), and BFS-with-a-queue for level order.
- The recursive DFS template — base case, recurse left, recurse right, combine — solved six different problems in this chapter (Max Depth, Balanced Tree, Diameter, Path Sum, Lowest Common Ancestor, Max Path Sum) using the identical skeleton; only the base case and the combine step ever changed.
- When a node's answer can't simultaneously be "extendable upward" and "the best possible global answer," track the global best as a side effect while still returning the parent-compatible value from the function itself — first seen in Diameter, pushed to its hardest form in Max Path Sum.
- The BST invariant (inorder is sorted) underlies Kth Smallest; the danger of comparing only to the immediate parent (instead of inherited bounds) underlies the Validate BST trap.
- Reconstructing and serializing a tree both reduce to the same fact: preorder always gives you the root first, and you need *some* second source of information — an inorder array, or explicit null markers — to know where each subtree ends.
