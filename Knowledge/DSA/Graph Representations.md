---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, graphs, representation]
---

# Graph Representations

## 1. Adjacency List
A map (or array) of lists, where `graph[node]` holds that node's neighbors (and edge weights).
- **Preferred for Sparse Graphs** (most real-world graphs).
- **Space:** $O(V + E)$
- **Neighbor lookup:** $O(\text{degree})$

```java
// Building an undirected adjacency list from an edge list
public List<List<Integer>> buildAdjacencyList(int n, int[][] edges) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    
    for (int[] edge : edges) {
        int u = edge[0], v = edge[1];
        graph.get(u).add(v);
        graph.get(v).add(u); // omit for directed graphs
    }
    return graph;
}
```

## 2. Adjacency Matrix
A $V \times V$ grid where `matrix[i][j]` holds the edge weight between $i$ and $j$ (or $0/\infty$ for no edge).
- **Preferred for Dense Graphs** or algorithms querying edge existence constantly.
- **Space:** $O(V^2)$ regardless of edge count (wasteful for sparse graphs).
- **Edge lookup:** $O(1)$
