---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, bfs, graphs, multi-source-bfs]
---

# Multi-Source BFS Pattern

## Intuition
Instead of starting a BFS from one node, seed the queue with **multiple** starting nodes simultaneously, all at distance 0. 

BFS's level-by-level guarantee still holds: it finds the distance to the *nearest* source for every node, because the frontier expands from all sources in lockstep. This finds distances in one $O(V + E)$ pass, instead of running $N$ separate single-source searches.

## Problem: Pacific Atlantic Water Flow
Find every cell that can reach *both* the Pacific and Atlantic oceans. 
**The Trick:** Reverse the problem. Run Multi-Source BFS from all Pacific borders, stepping *uphill* (`height[neighbor] >= height[curr]`). This finds all cells that flow into the Pacific. Do the same for the Atlantic. The answer is the intersection of both sets.

```java
// Simplified core logic:
Queue<int[]> queue = new ArrayDeque<>();
// 1. Enqueue all border cells of the target ocean
for (int[] borderCell : oceanBorders) {
    queue.offer(borderCell);
    reachable[borderCell[0]][borderCell[1]] = true;
}

// 2. Multi-source BFS (stepping UPHILL)
while (!queue.isEmpty()) {
    int[] curr = queue.poll();
    for (int[] dir : dirs) {
        int nr = curr[0] + dir[0], nc = curr[1] + dir[1];
        if (outOfBounds(nr, nc) || reachable[nr][nc]) continue;
        
        // Reverse flow condition: can water flow FROM nr TO curr?
        if (heights[nr][nc] < heights[curr[0]][curr[1]]) continue; 
        
        reachable[nr][nc] = true;
        queue.offer(new int[]{nr, nc});
    }
}
```
