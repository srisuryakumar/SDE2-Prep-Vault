# Chapter 8: Graphs
## Part 2 — Union-Find · Topological Sort

## Union-Find (Disjoint Set Union)

**What it solves.** Dynamic connectivity queries: "are these two nodes in the same component?" and "merge these two components" — both efficiently, without re-running a full traversal every time the structure changes.

**Structure.** An array `parent[]`, where `parent[i]` is i's parent in a forest of trees; each tree is one connected component, and a tree's **root** (a node that is its own parent) is that component's unique identifier.

**Naive version:**

```java
class UnionFind {
    int[] parent;

    UnionFind(int n) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;   // every node starts as its own root
    }

    int find(int x) {
        while (parent[x] != x) {
            x = parent[x];
        }
        return x;
    }

    void union(int x, int y) {
        int rootX = find(x), rootY = find(y);
        if (rootX != rootY) {
            parent[rootX] = rootY;
        }
    }
}
```

**The problem with the naive version.** Without any balancing, repeated unions can chain nodes into one long line — effectively a linked list — making `find()` degrade to O(n).

**Path compression.** While walking up to find the root, make every node along the way point **directly** to the root, not just to its old immediate parent. This flattens the tree permanently — every future `find()` on those same nodes becomes faster.

```java
int find(int x) {
    if (parent[x] != x) {
        parent[x] = find(parent[x]);   // find the root, then attach x directly to it
    }
    return parent[x];
}
```

**Union by rank.** When merging, always attach the *smaller* tree under the *larger* tree's root (tracked with a `rank` array — an upper bound on tree height). Attaching small-under-big keeps the combined tree's height unchanged (it only grows by 1 when both trees happen to have equal rank); attaching big-under-small would have grown the height every single time.

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
        if (rootX == rootY) return false;   // already connected — nothing to merge

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

**With both optimizations, every operation runs in O(α(n)) amortized**, where α is the inverse Ackermann function — a function that grows so slowly that α(n) ≤ 4 for any n you could ever practically encounter, far beyond the number of atoms in the observable universe. For every practical purpose, that's **O(1) amortized**.

**Trace** — both optimizations working together, on `UnionFind(6)`:

```
Initial: parent=[0,1,2,3,4,5]  rank=[0,0,0,0,0,0]

union(0,1): ranks equal(0) → parent[1]=0, rank[0]++.    parent=[0,0,2,3,4,5]  rank=[1,0,0,0,0,0]
union(2,3): ranks equal(0) → parent[3]=2, rank[2]++.    parent=[0,0,2,2,4,5]  rank=[1,0,1,0,0,0]
union(0,2): ranks equal(1) → parent[2]=0, rank[0]++.    parent=[0,0,0,2,4,5]  rank=[2,0,1,0,0,0]

find(3): parent[3]=2≠3 → recurse find(2): parent[2]=0≠2 → recurse find(0): root, return 0.
          find(2) compresses: parent[2]=0 (already was 0 — no change here).
          find(3) compresses: parent[3]=0  ← DIRECTLY to the root, collapsing the 3→2→0 chain
                                              into a single 3→0 hop for every future lookup.
          parent=[0,0,0,0,4,5]

union(4,5): ranks equal(0) → parent[5]=4, rank[4]++.    parent=[0,0,0,0,4,4]  rank=[2,0,1,0,1,0]
```

**When to reach for Union-Find:** "are these two nodes connected?" queries — especially when the graph is built incrementally, edge by edge, and connectivity needs checking *as you go*, not just once at the end; building a Minimum Spanning Tree via Kruskal's algorithm (Part 3); and detecting a cycle the moment it forms while adding edges one at a time (an edge creates a cycle exactly when its two endpoints are *already* in the same component before that edge is added).

---

## Problem — Redundant Connection (LeetCode 684)

**Statement.** A tree originally had no cycles, but one extra edge was added, creating exactly one cycle. Given the edges in the order they were added, find the one that — if removed — restores a valid tree. If more than one edge would work, return whichever occurs last in the input.

**Approach.** Process edges in order with Union-Find. For each edge `(u, v)`: if `u` and `v` are *already* in the same component before this edge is added, this edge is the one closing the cycle — return it immediately. Because edges are processed in their original order, the first one detected this way is automatically the answer the problem wants.

```java
public int[] findRedundantConnection(int[][] edges) {
    int n = edges.length;
    UnionFind uf = new UnionFind(n + 1);   // 1-indexed, per the problem's convention

    for (int[] edge : edges) {
        int u = edge[0], v = edge[1];
        if (!uf.union(u, v)) {
            return edge;   // union() returned false — u and v were ALREADY connected
        }
    }
    return new int[]{};   // unreachable given the problem's guarantees
}
```

**Trace** on `edges = [[1,2],[1,3],[2,3]]`:

```
union(1,2): different roots → merge. returns true.
union(1,3): different roots → merge. returns true.
union(2,3): find(2) and find(3) both resolve to the SAME root (both now under 1's tree)
            → ALREADY connected → union returns false → this edge is redundant.

Return [2,3]   ✓   (a 1-2-3 triangle; the last edge closes the cycle)
```

**Complexity:** O(n) amortized total. Space O(n).

---

## Problem — Number of Connected Components in an Undirected Graph (LeetCode 323)

**Statement.** Given n nodes and a list of undirected edges, count the connected components.

**Approach.** Start a counter at n (every node begins as its own component). Process every edge with Union-Find; every time `union()` performs a *real* merge (returns true — the two endpoints weren't already connected), decrement the counter by one.

```java
public int countComponents(int n, int[][] edges) {
    UnionFind uf = new UnionFind(n);
    int components = n;
    for (int[] edge : edges) {
        if (uf.union(edge[0], edge[1])) {
            components--;   // a genuine merge happened
        }
    }
    return components;
}
```

**Trace** on `n=5`, `edges=[[0,1],[1,2],[3,4]]`:

```
components=5.
union(0,1): merge → true → components=4.
union(1,2): merge → true → components=3.
union(3,4): merge → true → components=2.

Final components = 2   ✓   (groups {0,1,2} and {3,4})
```

**Complexity:** O(n + E) amortized. Space O(n).

---

## Topological Sort

**What it solves.** Ordering tasks so that for every directed edge u → v ("u must happen before v"), u comes before v in the final order. This requires the graph to be a **DAG** (Directed Acyclic Graph) — a cycle means some task would transitively need to precede itself, and no valid order can exist.

### Kahn's Algorithm (BFS with In-Degree)

**Intuition.** A node with in-degree 0 has no unmet dependencies — it's safe to schedule immediately. Repeatedly take any in-degree-0 node, add it to the output, and "remove" it by decrementing the in-degree of everything it points to (one of their dependencies is now satisfied). Whenever a decrement brings some neighbor's in-degree to 0, it just became available — queue it. This is BFS, except the queue holds "currently available" nodes instead of "currently reachable" ones.

```java
public List<Integer> topologicalSortKahns(int n, int[][] edges) {
    List<List<Integer>> graph = new ArrayList<>();
    int[] inDegree = new int[n];
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    for (int[] edge : edges) {
        int u = edge[0], v = edge[1];   // u must come before v
        graph.get(u).add(v);
        inDegree[v]++;
    }

    Queue<Integer> queue = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        if (inDegree[i] == 0) queue.offer(i);
    }

    List<Integer> order = new ArrayList<>();
    while (!queue.isEmpty()) {
        int node = queue.poll();
        order.add(node);
        for (int neighbor : graph.get(node)) {
            inDegree[neighbor]--;
            if (inDegree[neighbor] == 0) {
                queue.offer(neighbor);
            }
        }
    }

    // Fewer than n nodes in the final order means a cycle exists — no valid order
    return order.size() == n ? order : new ArrayList<>();
}
```

**Trace** on `n=4`, `edges=[[0,1],[0,2],[1,3],[2,3]]` (0 before 1 and 2; both 1 and 2 before 3):

```
graph: 0→[1,2], 1→[3], 2→[3], 3→[]
inDegree: [0, 1, 1, 2]

queue seeded with in-degree-0 nodes: [0]

poll 0 → order=[0].  neighbors 1,2: inDegree[1]→0 (enqueue), inDegree[2]→0 (enqueue).  queue=[1,2]
poll 1 → order=[0,1]. neighbor 3: inDegree[3]→1 (not 0 yet, don't enqueue).            queue=[2]
poll 2 → order=[0,1,2]. neighbor 3: inDegree[3]→0 (enqueue).                          queue=[3]
poll 3 → order=[0,1,2,3]. no neighbors.

order.size()=4=n → valid.  Final order: [0, 1, 2, 3]   ✓
```

**Complexity:** O(V + E).

### DFS-Based Topological Sort

**Intuition.** Run DFS from every unvisited node. The moment a node *finishes* — every single thing reachable from it has already been fully explored — push it onto a stack. Because a node only gets pushed after everything it points to has already been pushed, the node sits *closer to the top* of the stack than its downstream dependents. Popping the stack (LIFO) therefore yields the node *before* its dependents — exactly the order the problem requires.

```java
public List<Integer> topologicalSortDFS(int n, int[][] edges) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    for (int[] edge : edges) {
        graph.get(edge[0]).add(edge[1]);   // edge[0] before edge[1]
    }

    boolean[] visited = new boolean[n];
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(i, graph, visited, stack);
        }
    }

    List<Integer> order = new ArrayList<>();
    while (!stack.isEmpty()) {
        order.add(stack.pop());
    }
    return order;
}

private void dfs(int node, List<List<Integer>> graph, boolean[] visited, Deque<Integer> stack) {
    visited[node] = true;
    for (int neighbor : graph.get(node)) {
        if (!visited[neighbor]) {
            dfs(neighbor, graph, visited, stack);
        }
    }
    stack.push(node);   // pushed only after every descendant has fully finished
}
```

**Trace** on the same graph (`n=4`, edges 0→1, 0→2, 1→3, 2→3):

```
dfs(0): visit 0.
  → dfs(1): visit 1.
      → dfs(3): visit 3. no neighbors. push 3.        stack=[3]
    no more neighbors for 1. push 1.                  stack=[3,1]
  → dfs(2): visit 2.
      neighbor 3: already visited → skip.
    no more neighbors for 2. push 2.                  stack=[3,1,2]
  no more neighbors for 0. push 0.                     stack=[3,1,2,0]

Pop everything: 0, 2, 1, 3 → order = [0, 2, 1, 3]

Verify: edge 0→1: 0 before 1 ✓.  0→2: 0 before 2 ✓.  1→3: 1 before 3 ✓.  2→3: 2 before 3 ✓.
Valid — a different (also correct) ordering than Kahn's [0,1,2,3], since 1 and 2 can
legally appear in either relative order.
```

### Cycle Detection in a Directed Graph

DFS-based topological sort alone doesn't *detect* cycles — running it on a cyclic graph still produces *some* output, just not a valid one, since no valid order exists. The fix needs three states instead of plain visited/unvisited: **UNVISITED**, **IN_PROGRESS** (currently on the active DFS path, not yet finished), and **VISITED** (fully finished). Encountering a neighbor marked IN_PROGRESS means a back-edge to an ancestor still on the current path — a genuine cycle. Encountering a VISITED neighbor that *isn't* an ancestor is fine — that's just a normal cross-edge to something already fully explored elsewhere, not a cycle.

```java
private static final int UNVISITED = 0, IN_PROGRESS = 1, VISITED = 2;

private boolean hasCycle(int node, List<List<Integer>> graph, int[] state) {
    state[node] = IN_PROGRESS;
    for (int neighbor : graph.get(node)) {
        if (state[neighbor] == IN_PROGRESS) {
            return true;    // back-edge to a node still on the current path — CYCLE
        }
        if (state[neighbor] == UNVISITED && hasCycle(neighbor, graph, state)) {
            return true;
        }
    }
    state[node] = VISITED;
    return false;
}
```

This three-state coloring is exactly what the next problem is built on.

---

## Problem — Course Schedule (LeetCode 207)

**Statement.** `prerequisites[i] = [a, b]` means course `b` must be taken before course `a`. Determine whether it's possible to finish every course — equivalently, whether the prerequisite graph is cycle-free.

**Approach.** This is cycle detection in a directed graph, wearing a scheduling costume. Kahn's algorithm answers it directly: if the resulting order doesn't include every course, a cycle exists.

```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    int[] inDegree = new int[numCourses];
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    for (int[] pre : prerequisites) {
        int course = pre[0], prereq = pre[1];
        graph.get(prereq).add(course);
        inDegree[course]++;
    }

    Queue<Integer> queue = new ArrayDeque<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) queue.offer(i);
    }

    int finished = 0;
    while (!queue.isEmpty()) {
        int course = queue.poll();
        finished++;
        for (int next : graph.get(course)) {
            inDegree[next]--;
            if (inDegree[next] == 0) queue.offer(next);
        }
    }
    return finished == numCourses;
}
```

**Trace — a cyclic case**, `numCourses=2`, `prerequisites=[[1,0],[0,1]]` (course 1 needs 0, *and* course 0 needs 1 — circular):

```
graph: 0→[1], 1→[0].  inDegree=[1, 1] — every node has an incoming edge.
queue: no node has inDegree 0 → queue starts (and stays) empty.
Loop never executes. finished = 0.
finished(0) ≠ numCourses(2) → return false   ✓   (correctly detects the cycle)
```

**Complexity:** O(V + E).

---

## Problem — Course Schedule II (LeetCode 210)

**Statement.** Same setup, but return a *valid order* of courses, or an empty array if impossible.

**Approach.** Literally the same Kahn's algorithm — the only change is *collecting* the order into an array (which Course Schedule's version discards) instead of just counting how many courses finished.

```java
public int[] findOrder(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    int[] inDegree = new int[numCourses];
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    for (int[] pre : prerequisites) {
        graph.get(pre[1]).add(pre[0]);
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
    return idx == numCourses ? order : new int[]{};
}
```

Worth noticing explicitly: this is, line for line, the identical algorithm as Course Schedule — the only change is `order[idx++] = course` in place of a plain counter increment. "Can this be done at all" and "show me exactly how" are frequently the same algorithm with one bookkeeping line added. Kahn's algorithm, topological sort, and the boolean Course Schedule check are really three names for the same nine lines of code.

**Complexity:** O(V + E).

---

*Part 3 covers shortest-path algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall) applied to Network Delay Time, minimum spanning tree construction (Kruskal's and Prim's), and closes with the chapter-wide common mistakes, pattern recognition guide, and summary.*
