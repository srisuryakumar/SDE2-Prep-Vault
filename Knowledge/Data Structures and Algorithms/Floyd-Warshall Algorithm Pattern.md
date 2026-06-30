---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [dsa, pattern, shortest-path, floyd-warshall, graphs]
---

# Floyd-Warshall Algorithm Pattern

## Intuition
Finds the shortest paths between **every pair of nodes** at once.
It uses dynamic programming over "which nodes are allowed as intermediate stops."

If `dist[i][j]` is the shortest path from $i$ to $j$, we consider whether node $k$ helps.
`dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.
Iterate $k$ from $0$ to $V-1$. After $k$ has swept through every node, the matrix holds the true shortest paths.

## Template
```java
public int[][] floydWarshall(int n, int[][] edges) {
    int[][] dist = new int[n][n];
    final int INF = Integer.MAX_VALUE / 2; // Avoid overflow when adding
    
    for (int i = 0; i < n; i++) {
        Arrays.fill(dist[i], INF);
        dist[i][i] = 0;
    }
    
    for (int[] edge : edges) {
        dist[edge[0]][edge[1]] = edge[2];
        // dist[edge[1]][edge[0]] = edge[2]; // uncomment for undirected
    }

    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
    return dist;
}
```
**Complexity:** Time $O(V^3)$. Space $O(V^2)$.
- Worse than Dijkstra from every source ($O(V \cdot (V+E) \log V)$) on sparse graphs.
- Simpler to implement, handles negative edges natively, and becomes competitive on dense graphs ($E \approx V^2$).
