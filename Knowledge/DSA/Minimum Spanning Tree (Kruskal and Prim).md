---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [dsa, pattern, graphs, mst, kruskal, prim]
---

# Minimum Spanning Tree (Kruskal and Prim)

## Intuition
Given a connected, undirected, weighted graph, the Minimum Spanning Tree (MST) connects all $V$ vertices using exactly $V-1$ edges with the smallest possible total edge weight. No cycles are allowed.

## Kruskal's Algorithm (Greedy by Edge)
1. Sort all edges by weight, ascending.
2. Process them in order. Add an edge to the MST if its two endpoints are **not already connected**. Check this using Union-Find.
3. Stop when $V-1$ edges are added.
- **Best for:** Sparse graphs given as an edge list.
- **Complexity:** $O(E \log E)$ due to sorting.

```java
public int kruskalMST(int n, int[][] edges) {
    Arrays.sort(edges, (a, b) -> a[2] - b[2]); // Sort by weight
    UnionFind uf = new UnionFind(n);
    int totalWeight = 0, edgesUsed = 0;

    for (int[] edge : edges) {
        if (uf.union(edge[0], edge[1])) { // true = no cycle created
            totalWeight += edge[2];
            edgesUsed++;
            if (edgesUsed == n - 1) break;
        }
    }
    return totalWeight;
}
```

## Prim's Algorithm (Greedy by Frontier)
1. Start from any node.
2. Maintain a `visited` set (the MST grown so far).
3. Repeatedly add the **cheapest edge** connecting a visited node to an unvisited one using a Min-Heap.
- **Best for:** Dense graphs given as an adjacency list/matrix.
- **Complexity:** $O(E \log V)$ with a binary heap.

```java
public int primMST(int n, List<int[]>[] graph) {
    boolean[] visited = new boolean[n];
    PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
    minHeap.offer(new int[]{0, 0}); // Start at node 0
    int totalWeight = 0, nodesAdded = 0;

    while (!minHeap.isEmpty() && nodesAdded < n) {
        int[] curr = minHeap.poll();
        int node = curr[0], weight = curr[1];
        
        if (visited[node]) continue; // Stale entry
        visited[node] = true;
        totalWeight += weight;
        nodesAdded++;

        for (int[] edge : graph[node]) {
            int neighbor = edge[0], edgeWeight = edge[1];
            if (!visited[neighbor]) {
                minHeap.offer(new int[]{neighbor, edgeWeight});
            }
        }
    }
    return totalWeight;
}
```
