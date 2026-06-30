---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, topological-sort, kahn]
---

# Topological Sort Pattern

## Intuition
Orders nodes in a Directed Acyclic Graph (DAG) such that for every directed edge $u \rightarrow v$, $u$ comes before $v$. Used for task scheduling, dependency resolution, and course prerequisites.

## Kahn's Algorithm (BFS with In-Degree)
A node with in-degree 0 has no unmet dependencies and is safe to schedule.
1. Calculate in-degrees for all nodes.
2. Enqueue all nodes with in-degree 0.
3. Poll a node, add to order, and decrement the in-degree of all its neighbors.
4. If a neighbor's in-degree hits 0, enqueue it.
5. If the final order length $< n$, a cycle exists (no valid order).

```java
public int[] findOrder(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    int[] inDegree = new int[numCourses];
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    
    for (int[] pre : prerequisites) {
        graph.get(pre[1]).add(pre[0]); // pre[1] must come before pre[0]
        inDegree[pre[0]]++;
    }

    Queue<Integer> queue = new ArrayDeque<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) queue.offer(i);
    }

    int[] order = new int[numCourses];
    int idx = 0;
    
    while (!queue.isEmpty()) {
        int course = queue.poll();
        order[idx++] = course;
        for (int next : graph.get(course)) {
            inDegree[next]--;
            if (inDegree[next] == 0) queue.offer(next);
        }
    }
    
    // If idx == numCourses, a valid topological sort was found. Otherwise, a cycle exists.
    return idx == numCourses ? order : new int[]{};
}
```

## DFS-Based Topological Sort
Run DFS. When a node **finishes** (all its descendants are fully explored), push it onto a stack. Popping the stack at the end yields the topological order. 
To detect cycles with DFS, use 3 states: UNVISITED, IN_PROGRESS, VISITED. A back-edge to an IN_PROGRESS node indicates a cycle.
