---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, graphs, dfs, connected-components, cloning]
---

# DFS for Connected Components and Graph Cloning

## Connected Components (Number of Islands)
To find disjoint connected components, iterate over all nodes (or grid cells). For every unvisited node, increment your component count and run DFS/BFS to mark the entire component as visited.

```java
public int numIslands(char[][] grid) {
    int islands = 0;
    for (int r = 0; r < grid.length; r++) {
        for (int c = 0; c < grid[0].length; c++) {
            if (grid[r][c] == '1') {
                islands++;
                sink(grid, r, c); // DFS to mark all connected '1's as '0'
            }
        }
    }
    return islands;
}

private void sink(char[][] grid, int r, int c) {
    if (r < 0 || c < 0 || r >= grid.length || c >= grid[0].length || grid[r][c] != '1') return;
    grid[r][c] = '0'; // mark visited
    sink(grid, r + 1, c); sink(grid, r - 1, c);
    sink(grid, r, c + 1); sink(grid, r, c - 1);
}
```

## Graph Cloning (Clone Graph)
To deep copy a graph with cycles, use DFS with a `HashMap<OriginalNode, ClonedNode>`.
**CRITICAL:** Register the clone in the map *before* recursing into its neighbors, to break infinite recursion on cycles.

```java
private Node dfs(Node node, Map<Node, Node> visited) {
    if (visited.containsKey(node)) return visited.get(node); // Break cycles
    
    Node clone = new Node(node.val);
    visited.put(node, clone); // Register BEFORE recursing
    
    for (Node neighbor : node.neighbors) {
        clone.neighbors.add(dfs(neighbor, visited));
    }
    return clone;
}
```
