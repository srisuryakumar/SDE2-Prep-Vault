---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, shortest-path, dijkstra, graphs]
---

# Dijkstra's Algorithm Pattern

## Intuition
Finds the shortest path from a single source to all other nodes in a **weighted graph**.
It works by exploring nodes greedily, always choosing the node with the smallest known tentative distance next. This requires a **Min-Heap**.

**CRITICAL REQUIREMENT:** All edge weights must be non-negative. If there are negative edge weights, Dijkstra's greedy assumption breaks (use Bellman-Ford instead).

## Template
```java
public int[] dijkstra(int n, List<int[]>[] graph, int source) {
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[source] = 0;

    // Min-Heap stores [node, tentative_distance]
    PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
    minHeap.offer(new int[]{source, 0});
    
    boolean[] visited = new boolean[n];

    while (!minHeap.isEmpty()) {
        int[] curr = minHeap.poll();
        int node = curr[0], d = curr[1];
        
        if (visited[node]) continue; // STALE ENTRY: already finalized a better distance
        visited[node] = true;

        for (int[] edge : graph[node]) {
            int neighbor = edge[0], weight = edge[1];
            if (d + weight < dist[neighbor]) {
                dist[neighbor] = d + weight;
                minHeap.offer(new int[]{neighbor, dist[neighbor]});
            }
        }
    }
    return dist;
}
```
**Complexity:** $O((V + E) \log V)$ time with a binary heap. Space $O(V + E)$.
