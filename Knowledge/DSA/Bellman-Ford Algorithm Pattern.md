---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, shortest-path, bellman-ford, graphs]
---

# Bellman-Ford Algorithm Pattern

## Intuition
Finds single-source shortest paths. Unlike Dijkstra, **it handles negative edge weights** and can **detect negative cycles**.
A shortest path in a graph without negative cycles uses at most $V-1$ edges. Bellman-Ford simply relaxes *every* edge $V-1$ times.

**Negative Cycle Detection:** Run one *additional* pass (the $V$-th pass). If any edge can still be relaxed, a negative cycle exists (because a valid shortest path would have stabilized by $V-1$).

## Template
```java
public int[] bellmanFord(int n, int[][] edges, int source) {
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[source] = 0;

    // Relax all edges V-1 times
    for (int i = 0; i < n - 1; i++) {
        for (int[] edge : edges) {
            int u = edge[0], v = edge[1], weight = edge[2];
            if (dist[u] != Integer.MAX_VALUE && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
            }
        }
    }

    // Extra pass for negative cycle detection
    for (int[] edge : edges) {
        int u = edge[0], v = edge[1], weight = edge[2];
        if (dist[u] != Integer.MAX_VALUE && dist[u] + weight < dist[v]) {
            throw new IllegalStateException("Graph contains a negative cycle");
        }
    }
    return dist;
}
```

## Problem Variant: Cheapest Flights Within K Stops
If you want to find the shortest path using at most $K$ stops ($K+1$ edges), run Bellman-Ford for exactly $K+1$ iterations.
**CRITICAL:** You must copy the `dist` array at the start of each iteration to ensure you only use paths of length $i$ when calculating paths of length $i+1$, preventing multiple hops in a single iteration.
**Complexity:** $O(V \cdot E)$ time. Space $O(V)$.
