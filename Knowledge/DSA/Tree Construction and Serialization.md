---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 6 — Trees"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, trees, serialization, pattern]
---

# Tree Construction and Serialization

## Construct from Preorder and Inorder
**Why two traversals?** Preorder's first element is *always* the root. Inorder tells you how to split into left/right subtrees (everything to the left of the root in the inorder array belongs to the left subtree).

**Approach:**
1. A `HashMap` mapping value to its index in the inorder array makes finding the split point $O(1)$.
2. A shared, mutating `preorderIndex` tracks the "next root".
3. **CRITICAL:** `root.left` must be fully built before `root.right` begins, because preorder lists the *entire* left subtree before the right subtree.

```java
private int preorderIndex;
private Map<Integer, Integer> inorderIndexMap;

public TreeNode buildTree(int[] preorder, int[] inorder) {
    preorderIndex = 0;
    inorderIndexMap = new HashMap<>();
    for (int i = 0; i < inorder.length; i++) inorderIndexMap.put(inorder[i], i);
    return build(preorder, 0, inorder.length - 1);
}

private TreeNode build(int[] preorder, int inorderLeft, int inorderRight) {
    if (inorderLeft > inorderRight) return null;
    int rootVal = preorder[preorderIndex++];
    TreeNode root = new TreeNode(rootVal);
    int mid = inorderIndexMap.get(rootVal);
    root.left = build(preorder, inorderLeft, mid - 1);
    root.right = build(preorder, mid + 1, inorderRight);
    return root;
}
```

## Serialize and Deserialize Binary Tree
Use **preorder traversal with explicit `null` markers**.
Without null markers, a preorder sequence is ambiguous. With them, it becomes self-sufficient. Deserializing just reads tokens in the exact root-left-right order they were written.

```java
public String serialize(TreeNode root) {
    StringBuilder sb = new StringBuilder();
    serializeHelper(root, sb);
    return sb.toString();
}

private void serializeHelper(TreeNode node, StringBuilder sb) {
    if (node == null) { sb.append("null,"); return; }
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
    if (token.equals("null")) return null;
    TreeNode node = new TreeNode(Integer.parseInt(token));
    node.left = deserializeHelper(tokens); // consumed in SAME order as written
    node.right = deserializeHelper(tokens);
    return node;
}
```
