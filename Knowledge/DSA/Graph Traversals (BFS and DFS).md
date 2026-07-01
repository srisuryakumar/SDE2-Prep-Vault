---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, graphs, bfs, dfs]
---

# Graph Traversals (BFS and DFS)

## BFS (Breadth-First Search)
Explores nodes in strictly increasing order of distance from the start. **Guarantees shortest paths in unweighted graphs.** (Does *not* guarantee shortest paths in weighted graphs—use Dijkstra's instead).

```java
public void bfs(int start, List<List<Integer>> graph) {
    Set<Integer> visited = new HashSet<>();
    Queue<Integer> queue = new ArrayDeque<>();
    queue.offer(start);
    visited.add(start); // Mark visited BEFORE enqueueing

    while (!queue.isEmpty()) {
        int node = queue.poll();
        // process node
        for (int neighbor : graph.get(node)) {
            if (!visited.contains(neighbor)) {
                visited.add(neighbor);
                queue.offer(neighbor);
            }
        }
    }
}
```

## DFS (Depth-First Search)
Explores one path to its end before backtracking. Used for connected components, cycle detection, and path finding/enumeration.

**Iterative DFS using a stack:**
```java
public void dfsIterative(int start, List<List<Integer>> graph) {
    Set<Integer> visited = new HashSet<>();
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(start);

    while (!stack.isEmpty()) {
        int node = stack.pop();
        if (visited.contains(node)) continue; // May have been pushed >1 time
        visited.add(node); // Mark visited AFTER popping
        
        // process node
        for (int neighbor : graph.get(node)) {
            if (!visited.contains(neighbor)) {
                stack.push(neighbor);
            }
        }
    }
}
```
**CRITICAL DIFFERENCE:** BFS marks a node visited *before* enqueueing to prevent duplicates. Iterative DFS typically marks visited *after* popping, requiring a `continue` guard.
