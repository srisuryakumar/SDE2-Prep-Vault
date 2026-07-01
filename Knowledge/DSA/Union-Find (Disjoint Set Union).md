---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, graphs, union-find, dsu]
---

# Union-Find (Disjoint Set Union)

## Intuition
Solves dynamic connectivity queries efficiently: "Are these two nodes in the same component?" and "Merge these two components".
Use this when a graph is built incrementally edge by edge, and you need to check connectivity or cycle formation *as you go*.

## Optimizations
1. **Path Compression:** During `find()`, make every node along the path point directly to the root. This permanently flattens the tree.
2. **Union by Rank:** When merging, attach the *smaller* tree under the *larger* tree's root to prevent the height from growing unnecessarily.

With both optimizations, operations are $O(\alpha(n))$ amortized, which is effectively **$O(1)$ amortized**.

## Template
```java
class UnionFind {
    int[] parent;
    int[] rank;

    UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);   // path compression
        }
        return parent[x];
    }

    boolean union(int x, int y) {
        int rootX = find(x), rootY = find(y);
        if (rootX == rootY) return false;   // ALREADY CONNECTED (Cycle detected if adding an edge!)

        // Union by rank
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
        return true;
    }
}
```

## Classic Problems
- **Redundant Connection:** If `union(u, v)` returns false, that edge just closed a cycle.
- **Number of Connected Components:** Start with $n$ components. Every time `union` returns true (a genuine merge happened), decrement the components count.
