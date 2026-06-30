# Chapter 8: Graphs
## Part 3 — Shortest Paths · Minimum Spanning Tree

## Shortest Path

### Why BFS Doesn't Work for Weighted Graphs

BFS guarantees shortest paths by **edge count**, treating every edge as cost 1. In a weighted graph, a path with *more* edges can easily have a *smaller* total weight than a path with fewer, more expensive edges. BFS's FIFO queue processes nodes in discovery order, not in order of actual accumulated distance — it can finalize a node's distance before a cheaper route through a not-yet-explored path is even discovered.

### Dijkstra's Algorithm

**The fix:** replace the FIFO queue with a **min-heap** keyed on tentative distance. Always process the node with the smallest currently-known distance next. This guarantees that the moment a node is popped, its distance is final — *provided every edge weight is non-negative* (the reason for that caveat is made concrete in the Bellman-Ford section below).

```java
public int[] dijkstra(int n, List<int[]>[] graph, int source) {
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[source] = 0;

    PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> a[1] - b[1]);   // [node, distance]
    minHeap.offer(new int[]{source, 0});
    boolean[] visited = new boolean[n];

    while (!minHeap.isEmpty()) {
        int[] curr = minHeap.poll();
        int node = curr[0], d = curr[1];
        if (visited[node]) continue;   // stale entry — already finalized with a better distance
        visited[node] = true;

        for (int[] edge : graph[node]) {
            int neighbor = edge[0], weight = edge[1];
            int newDist = d + weight;
            if (newDist < dist[neighbor]) {
                dist[neighbor] = newDist;
                minHeap.offer(new int[]{neighbor, newDist});
            }
        }
    }
    return dist;
}
```

**Trace**, source = 0, on this graph:

```
            0
          /   \
       (1)    (4)
        /       \
       2 --(2)--> 1
        \         /
       (5)      (1)
          \     /
            v  v
             3
```

(Edges: `0→2` weight 1, `0→1` weight 4, `2→1` weight 2, `2→3` weight 5, `1→3` weight 1 — all directed.)

```
dist=[0,∞,∞,∞]   heap=[(0,0)]

Pop(0,0): finalize 0.
  relax 0→2: 0+1=1 < ∞ → dist[2]=1, push(2,1)
  relax 0→1: 0+4=4 < ∞ → dist[1]=4, push(1,4)
  dist=[0,4,1,∞]   heap=[(2,1),(1,4)]

Pop(2,1): finalize 2.
  relax 2→1: 1+2=3 < 4  → dist[1]=3, push(1,3)
  relax 2→3: 1+5=6 < ∞  → dist[3]=6, push(3,6)
  dist=[0,3,1,6]   heap=[(1,3),(1,4)stale,(3,6)]

Pop(1,3): finalize 1.
  relax 1→3: 3+1=4 < 6  → dist[3]=4, push(3,4)
  dist=[0,3,1,4]   heap=[(1,4)stale,(3,4),(3,6)stale]

Pop(1,4): visited[1] already true → SKIP (stale).

Pop(3,4): finalize 3.  no outgoing edges.
  dist=[0,3,1,4]

Pop(3,6): visited[3] already true → SKIP (stale).

heap empty.  Final dist = [0, 3, 1, 4]
```

**Verify by hand:** shortest to 1 — `0→2→1` = 1+2 = 3, beats the direct `0→1` = 4 ✓. Shortest to 3 — candidates are `0→2→1→3`=1+2+1=4, `0→2→3`=1+5=6, `0→1→3`=4+1=5; minimum is 4 ✓. Both match the algorithm's output exactly.

**Complexity:** O((V + E) log V) with a binary heap. Space O(V + E).

### Bellman-Ford

**What it adds over Dijkstra:** correctness with negative edge weights, plus the ability to detect a negative cycle (a cycle whose total weight is negative — meaning "shortest path" is undefined, since looping it forever keeps decreasing the total without bound).

**Why V−1 passes.** Any shortest path in a graph with no negative cycle uses at most V−1 edges (a path revisiting a node would have to contain a cycle, which can only help if that cycle is negative — exactly the case being excluded). Each full pass of relaxing *every* edge propagates "best known distance" one hop further along any path; after V−1 passes, every legitimate shortest path — none of which exceeds V−1 edges — has been fully propagated.

**Detecting a negative cycle.** Run one *additional* pass after the guaranteed-sufficient V−1. If any edge can still be relaxed, the only explanation is a negative cycle reachable from the source — a legitimate shortest path would have already stabilized.

```java
public int[] bellmanFord(int n, int[][] edges, int source) {
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[source] = 0;

    for (int i = 0; i < n - 1; i++) {
        for (int[] edge : edges) {
            int u = edge[0], v = edge[1], weight = edge[2];
            if (dist[u] != Integer.MAX_VALUE && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
            }
        }
    }

    for (int[] edge : edges) {   // one extra pass — any improvement here means a negative cycle
        int u = edge[0], v = edge[1], weight = edge[2];
        if (dist[u] != Integer.MAX_VALUE && dist[u] + weight < dist[v]) {
            throw new IllegalStateException("Graph contains a negative cycle");
        }
    }
    return dist;
}
```

**Trace**, source = 0, on `0→1 (5)`, `0→2 (4)`, `1→2 (−3)` (n=3, so 2 passes):

```
dist=[0,∞,∞]

Pass 1: relax 0→1: 0+5=5 < ∞  → dist[1]=5
        relax 0→2: 0+4=4 < ∞  → dist[2]=4
        relax 1→2: 5+(-3)=2 < 4 → dist[2]=2
        dist=[0,5,2]

Pass 2: relax 0→1: 5, not < 5 → no change
        relax 0→2: 4, not < 2 → no change
        relax 1→2: 2, not < 2 → no change
        dist=[0,5,2]  (stable)

Extra pass: no further improvement anywhere → no negative cycle.
Final dist = [0, 5, 2]
```

**The point this trace is actually making:** watch what Dijkstra would have done on this exact graph. After relaxing from node 0, the tentative distances are `dist[1]=5, dist[2]=4`. Dijkstra's greedy rule pops the *smaller* tentative distance next — node 2, at distance 4 — and **finalizes it immediately**, never revisiting it again. But the true shortest distance to node 2 is 2, reached via `0→1→2` *through the negative edge* — a path Dijkstra never gets the chance to consider, because it already closed the book on node 2 before discovering it. That's the exact mechanism by which a single negative edge breaks Dijkstra's correctness, made concrete rather than asserted.

**Complexity:** O(V · E) — V−1 (plus one) passes, each examining every edge. Slower than Dijkstra, but correct in a regime Dijkstra simply cannot handle.

### Floyd-Warshall

**What it solves.** Shortest paths between **every pair** of nodes at once, via dynamic programming over "which nodes are allowed as intermediate stops."

**The recurrence.** Let `dist[i][j]` represent the shortest path from i to j using only nodes `0..k-1` as possible intermediates. Considering whether node k itself helps: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`. Iterate k from 0 to n−1, updating the *entire* matrix at each step; once k has swept through every node, `dist[i][j]` holds the true shortest path allowing *any* node as an intermediate stop.

```java
public int[][] floydWarshall(int n, int[][] edges) {
    int[][] dist = new int[n][n];
    final int INF = Integer.MAX_VALUE / 2;   // avoid overflow when summing two INFs
    for (int i = 0; i < n; i++) {
        Arrays.fill(dist[i], INF);
        dist[i][i] = 0;
    }
    for (int[] edge : edges) {
        dist[edge[0]][edge[1]] = edge[2];
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

**Complexity:** O(V³) — three nested loops, each O(V). Worse than running Dijkstra from every source (O(V·(V+E) log V)) on a *sparse* graph, but simpler to implement (no heap at all), handles negative edges natively (same no-negative-cycle caveat as Bellman-Ford), and becomes competitive — or better — on *dense* graphs, where E approaches V² and Dijkstra-from-every-source's cost approaches O(V³ log V), strictly worse than Floyd-Warshall's plain O(V³).

**Choosing among the three:**

| Situation | Algorithm | Complexity |
|---|---|---|
| Non-negative weights, single source | Dijkstra | O((V+E) log V) |
| Negative weights allowed, single source | Bellman-Ford | O(V·E) |
| All pairs, dense graph or small V | Floyd-Warshall | O(V³) |

---

## Problem — Network Delay Time (LeetCode 743)

**Statement.** Directed weighted edges `times[i]=[u,v,w]` mean a signal travels u→v in time w. Starting from node k, return the time for *every* node to receive the signal, or −1 if some node never does.

**Approach.** Direct Dijkstra from source k. "Every node has received the signal" means waiting for the *slowest* one — the answer is the **maximum** of all finalized shortest distances. If any node's distance is still infinity at the end, it's unreachable — return −1.

```java
public int networkDelayTime(int[][] times, int n, int k) {
    List<int[]>[] graph = new List[n + 1];
    for (int i = 1; i <= n; i++) graph[i] = new ArrayList<>();
    for (int[] time : times) {
        graph[time[0]].add(new int[]{time[1], time[2]});
    }

    int[] dist = new int[n + 1];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[k] = 0;

    PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    minHeap.offer(new int[]{k, 0});
    boolean[] visited = new boolean[n + 1];

    while (!minHeap.isEmpty()) {
        int[] curr = minHeap.poll();
        int node = curr[0], d = curr[1];
        if (visited[node]) continue;
        visited[node] = true;
        for (int[] edge : graph[node]) {
            int neighbor = edge[0], weight = edge[1];
            if (d + weight < dist[neighbor]) {
                dist[neighbor] = d + weight;
                minHeap.offer(new int[]{neighbor, d + weight});
            }
        }
    }

    int maxDist = 0;
    for (int i = 1; i <= n; i++) {
        if (dist[i] == Integer.MAX_VALUE) return -1;
        maxDist = Math.max(maxDist, dist[i]);
    }
    return maxDist;
}
```

**Trace** on `times=[[2,1,1],[2,3,1],[3,4,1]]`, `n=4`, `k=2`:

```
graph: 2→[(1,1),(3,1)], 3→[(4,1)]
dist (1-indexed) = [_, ∞, 0, ∞, ∞]

Pop(2,0): finalize 2.  relax 2→1: dist[1]=1, push.  relax 2→3: dist[3]=1, push.
Pop(1,1): finalize 1.  no outgoing edges.
Pop(3,1): finalize 3.  relax 3→4: dist[4]=2, push.
Pop(4,2): finalize 4.  no outgoing edges.

dist = [_, 1, 0, 1, 2].  maxDist = max(1,0,1,2) = 2.

Final answer: 2   ✓   (the signal reaches node 4 last, via 2→3→4)
```

**Complexity:** O((V + E) log V). Space O(V + E).

---

## Minimum Spanning Tree

**What it is.** Given a connected, undirected, weighted graph, a spanning tree connects all V vertices using exactly V−1 edges with no cycles. The *minimum* spanning tree (MST) is the spanning tree with the smallest possible total edge weight.

### Kruskal's Algorithm

**Greedy strategy.** Sort *all* edges by weight, ascending. Process them in that order, adding an edge to the MST exactly when its two endpoints are **not already connected** — checked with Union-Find. Stop once V−1 edges have been added.

**Why greedy-by-weight is correct (the cut property, briefly).** For any way of splitting the graph's vertices into two non-empty groups, the cheapest edge crossing between them *must* belong to some MST — swapping it in for any pricier crossing edge can only produce an equal-or-cheaper spanning tree. Processing edges from cheapest to most expensive, accepting any that doesn't close a cycle, is exactly this cut property applied over and over: every accepted edge is, at the moment it's considered, the cheapest possible way to join its two (still-separate) components.

```java
public int kruskalMST(int n, int[][] edges) {
    Arrays.sort(edges, (a, b) -> a[2] - b[2]);   // ascending by weight
    UnionFind uf = new UnionFind(n);
    int totalWeight = 0, edgesUsed = 0;

    for (int[] edge : edges) {
        int u = edge[0], v = edge[1], weight = edge[2];
        if (uf.union(u, v)) {   // true means NOT already connected — no cycle created
            totalWeight += weight;
            edgesUsed++;
            if (edgesUsed == n - 1) break;
        }
    }
    return totalWeight;
}
```

**Trace** on `n=4`, edges `(0,1,10), (0,2,6), (0,3,5), (1,3,15), (2,3,4)`:

```
Sorted by weight: (2,3,4), (0,3,5), (0,2,6), (0,1,10), (1,3,15)

(2,3,4): different roots → merge.  totalWeight=4, edgesUsed=1.
(0,3,5): different roots → merge.  totalWeight=9, edgesUsed=2.
(0,2,6): SAME root already (0,2,3 all merged) → would create a cycle → skip.
(0,1,10): different roots → merge.  totalWeight=19, edgesUsed=3.
edgesUsed == n-1 (3) → done.

Final totalWeight = 19
```

**Verify:** to connect all 4 nodes, node 1 must join via either `(0,1,10)` or `(1,3,15)` — 10 is cheaper, and that's exactly what got chosen. 19 is indeed minimal.

**Complexity:** O(E log E) for the sort — Union-Find's contribution is amortized O(1) per operation and doesn't change the dominant term.

### Prim's Algorithm

**Greedy strategy, different shape.** Start from any node. Maintain a `visited` set — the MST grown so far — and repeatedly add the **cheapest edge** connecting a visited node to an unvisited one, using a min-heap to find that cheapest crossing edge efficiently each time.

```java
public int primMST(int n, List<int[]>[] graph) {
    boolean[] visited = new boolean[n];
    PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> a[1] - b[1]);   // [node, edgeWeight]
    minHeap.offer(new int[]{0, 0});   // arbitrary start
    int totalWeight = 0, nodesAdded = 0;

    while (!minHeap.isEmpty() && nodesAdded < n) {
        int[] curr = minHeap.poll();
        int node = curr[0], weight = curr[1];
        if (visited[node]) continue;   // stale entry — already in the MST
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

**Notice the structural twin of Dijkstra:** same min-heap, same visited set, same "pop smallest, skip stale entries" shape. The difference is *what's being minimized* — Dijkstra minimizes cumulative path distance from a fixed source; Prim's minimizes the weight of the single next edge connecting the growing tree to a new node, with no notion of cumulative distance at all.

**Trace** on the identical graph as Kruskal's (now undirected): `0-1(10), 0-2(6), 0-3(5), 1-3(15), 2-3(4)`, starting from node 0:

```
Pop(0,0): finalize 0.  push (1,10),(2,6),(3,5).
Pop(3,5): finalize 3.  totalWeight=5.  push (1,15),(2,4)  [edge to 0 skipped, 0 already visited]
Pop(2,4): finalize 2.  totalWeight=9.  no new pushes — both 2's neighbors (0,3) already visited.
Pop(2,6): stale (2 already visited) → skip.
Pop(1,10): finalize 1.  totalWeight=19.  nodesAdded=4=n → done.

Final totalWeight = 19   ✓  — IDENTICAL to Kruskal's result, reached by a completely
                              different mechanism (frontier-growing instead of
                              global edge-sorting).
```

**Complexity:** O(E log V) with a binary heap.

**Kruskal's vs. Prim's, practically:** Kruskal's is usually the simpler choice when edges are handed to you as a flat list on a sparse graph (O(E log E) from the sort). Prim's tends to win on dense graphs given as an adjacency list or matrix, where array-based implementation variants can reach O(V²) — beating Kruskal's O(E log E) once E approaches V².

---

## Common Mistakes — Chapter-Wide

- **Using BFS on a weighted graph expecting shortest path.** BFS only counts edges, completely blind to weight — use Dijkstra (or Bellman-Ford for negative weights).
- **Forgetting the stale-entry check** (`if (visited[node]) continue;`) in Dijkstra or Prim's — without it, an already-finalized node can be reprocessed using an outdated, larger value still sitting in the heap.
- **Using Dijkstra on a graph with negative edges.** Its greedy "smallest tentative distance is final" assumption breaks the instant a negative edge can retroactively beat an already-finalized node — demonstrated concretely in the Bellman-Ford trace above.
- **Using only one of path compression or union by rank, not both, in Union-Find.** Either alone still degrades toward O(n) per operation in the worst case; both together give O(α(n)) ≈ O(1).
- **Reversing the direction in Kahn's setup.** `graph[u].add(v)` with `inDegree[v]++` encodes "u before v" — swap u and v and the entire dependency direction silently flips.
- **Conflating "visited" with "finished" in directed-graph cycle detection.** A node can be visited (explored at some point) without being on the *current* path. Only the IN_PROGRESS state — not plain "visited" — correctly signals a cycle.
- **Stopping Bellman-Ford after V−1 passes with no extra check**, silently returning a plausible-looking answer even when a negative cycle makes "shortest path" undefined.
- **Reaching for Floyd-Warshall's O(V³) when only single-source paths are needed.** Dijkstra or Bellman-Ford is the right tool; Floyd-Warshall earns its cost only when *every* pair's distance is actually required.

## Pattern Recognition Guide

- "Shortest path / fewest steps, unweighted" → BFS (multi-source if there are several valid starting points).
- "Shortest path, weighted, all non-negative" → Dijkstra.
- "Shortest path, negative weights allowed, or detect a negative cycle" → Bellman-Ford.
- "Shortest path between every pair of nodes" → Floyd-Warshall (small/dense graphs) or Dijkstra from every source (large/sparse graphs).
- "Are these two nodes connected," especially with edges arriving incrementally → Union-Find.
- "Order tasks given dependencies," "detect a cycle in a directed graph" → topological sort: Kahn's for the order itself (an incomplete result doubles as a cycle check), the three-state DFS coloring when cycle detection alone is the goal.
- "Connect everything as cheaply as possible" → Minimum Spanning Tree: Kruskal's for a sparse graph given as an edge list, Prim's for a dense graph given as an adjacency structure.
- "Flood fill," "count connected regions," "explore reachable cells" → DFS or BFS over an implicit grid graph (Number of Islands, Pacific Atlantic).
- Any problem with an implicit graph disguised as something else (word transformations, state transitions) → identify the nodes and edges first; once that's answered, everything else in this chapter applies (Word Ladder).

## Chapter Summary

- Adjacency lists win for sparse graphs (O(V+E) space); adjacency matrices win when O(1) edge-existence lookups matter more than space, on dense graphs.
- BFS guarantees shortest paths only in unweighted graphs, because its level-by-level discipline is blind to anything but edge count; multi-source BFS finds the distance to the *nearest* of several sources in one O(V+E) pass.
- DFS is the right shape for connected components, path existence, and cycle detection — and directed-graph cycle detection specifically needs three states (unvisited/in-progress/finished), not just visited/unvisited.
- Union-Find answers dynamic connectivity in amortized O(α(n)) ≈ O(1) per operation, but only with *both* path compression and union by rank together.
- Topological sort comes in two equally valid forms — Kahn's (BFS on in-degree) and DFS-based (push on finish, then reverse) — and "can this be scheduled" vs. "show me the schedule" are usually the same algorithm with one bookkeeping line added.
- Dijkstra replaces BFS's FIFO queue with a min-heap ordered by tentative distance, correct only when every weight is non-negative; a single negative edge can retroactively beat an already-finalized node, which is exactly what Bellman-Ford exists to survive.
- Floyd-Warshall trades a worse O(V³) for getting every pair's shortest distance at once, via DP over "which nodes are allowed as intermediate stops."
- Minimum Spanning Tree has two equally correct greedy strategies that converge on the identical answer by entirely different mechanisms: Kruskal's (sort edges, add if no cycle) and Prim's (grow one frontier, always take the cheapest edge leaving it) — pick based on how the graph is given to you and how dense it is.

---

#### Advanced Graph Algorithms — LeetCode Problems with Complete Solutions

**Bellman-Ford Algorithm:**

```java
// LeetCode #743 — Network Delay Time
// Find the time for a signal to reach all nodes from source k.
// Why Bellman-Ford (not Dijkstra): demonstrates the algorithm clearly.
// Note: Dijkstra is also valid here; use Bellman-Ford to learn the pattern.
//
// Time: O(V × E), Space: O(V)

public int networkDelayTime(int[][] times, int n, int k) {
    int[] dist = new int[n + 1];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[k] = 0;  // source node starts at distance 0

    // Bellman-Ford: relax all edges V-1 times
    // After i iterations, dist[] has the shortest path using at most i edges
    for (int i = 0; i < n - 1; i++) {
        for (int[] edge : times) {
            int u = edge[0], v = edge[1], w = edge[2];
            if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;  // relax the edge
            }
        }
    }

    int maxTime = 0;
    for (int i = 1; i <= n; i++) {
        if (dist[i] == Integer.MAX_VALUE) return -1;  // node unreachable
        maxTime = Math.max(maxTime, dist[i]);
    }
    return maxTime;
}
```

```java
// LeetCode #787 — Cheapest Flights Within K Stops
// Minimum cost from src to dst with at most k stops.
// Bellman-Ford variant: run exactly k+1 iterations (k stops = k+1 edges).
//
// Time: O(K × E), Space: O(V)

public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
    int[] prices = new int[n];
    Arrays.fill(prices, Integer.MAX_VALUE);
    prices[src] = 0;

    // Run exactly k+1 times (k stops allows k+1 edges)
    for (int i = 0; i <= k; i++) {
        int[] temp = Arrays.copyOf(prices, n);  // copy BEFORE iteration
        // CRITICAL: use `prices` (last iteration) not `temp` (current iteration)
        // Without the copy, we might use edges added in THIS iteration,
        // allowing more than k+1 edges in the path.
        for (int[] flight : flights) {
            int from = flight[0], to = flight[1], price = flight[2];
            if (prices[from] != Integer.MAX_VALUE && prices[from] + price < temp[to]) {
                temp[to] = prices[from] + price;
            }
        }
        prices = temp;
    }
    return prices[dst] == Integer.MAX_VALUE ? -1 : prices[dst];
}
```

**Floyd-Warshall Algorithm:**

```java
// LeetCode #1334 — Find the City With the Smallest Number of Neighbors
//                   at a Threshold Distance
// For each city, count how many other cities are reachable within threshold.
// Return the city with the fewest reachable neighbors (ties: largest city index).
//
// Time: O(n³), Space: O(n²)

public int findTheCity(int n, int[][] edges, int distanceThreshold) {
    // Initialize distance matrix
    int[][] dist = new int[n][n];
    for (int[] row : dist) Arrays.fill(row, Integer.MAX_VALUE / 2); // avoid overflow
    for (int i = 0; i < n; i++) dist[i][i] = 0;  // self-distance = 0

    // Populate known edges
    for (int[] edge : edges) {
        int u = edge[0], v = edge[1], w = edge[2];
        dist[u][v] = w;
        dist[v][u] = w;  // undirected graph
    }

    // Floyd-Warshall: try every node k as intermediate
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                // Can we go i → k → j shorter than i → j directly?
                if (dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }

    // Find city with fewest reachable neighbors within threshold
    int resultCity = -1, minNeighbors = Integer.MAX_VALUE;
    for (int city = 0; city < n; city++) {
        int count = 0;
        for (int other = 0; other < n; other++) {
            if (other != city && dist[city][other] <= distanceThreshold) count++;
        }
        // Use <= (not <) to prefer larger index city when tied
        if (count <= minNeighbors) {
            minNeighbors = count;
            resultCity = city;
        }
    }
    return resultCity;
}
```

**Minimum Spanning Tree (Kruskal's Algorithm):**

```java
// LeetCode #1584 — Min Cost to Connect All Points
// Each point (x,y) — cost to connect = Manhattan distance |x1-x2| + |y1-y2|
// Find the minimum cost to connect ALL points (MST problem).
//
// Time: O(n² log n), Space: O(n² + n)

public int minCostConnectPoints(int[][] points) {
    int n = points.length;

    // Generate all possible edges (n² edges for n points)
    List<int[]> edges = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int cost = Math.abs(points[i][0] - points[j][0])
                     + Math.abs(points[i][1] - points[j][1]);
            edges.add(new int[]{cost, i, j});
        }
    }

    // Sort edges by cost ascending (greedy: always pick cheapest edge)
    edges.sort((a, b) -> a[0] - b[0]);

    // Union-Find for cycle detection
    int[] parent = new int[n];
    int[] rank = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;

    int totalCost = 0, edgesUsed = 0;

    for (int[] edge : edges) {
        int cost = edge[0], u = edge[1], v = edge[2];
        // Only add edge if it connects two DIFFERENT components (no cycle)
        if (union(parent, rank, u, v)) {
            totalCost += cost;
            edgesUsed++;
            if (edgesUsed == n - 1) break;  // MST has exactly n-1 edges
        }
    }
    return totalCost;
}

private int find(int[] parent, int x) {
    if (parent[x] != x) parent[x] = find(parent, parent[x]); // path compression
    return parent[x];
}

private boolean union(int[] parent, int[] rank, int x, int y) {
    int px = find(parent, x), py = find(parent, y);
    if (px == py) return false;  // already in same component — adding would create cycle
    if (rank[px] < rank[py]) parent[px] = py;
    else if (rank[px] > rank[py]) parent[py] = px;
    else { parent[py] = px; rank[px]++; }
    return true;
}
```

```java
// LeetCode #1135 — Connecting Cities With Minimum Cost (Kruskal's)
// Simpler version: given explicit edges, find MST cost.
// Time: O(E log E), Space: O(n)

public int minimumCost(int n, int[][] connections) {
    // Sort connections by cost
    Arrays.sort(connections, (a, b) -> a[2] - b[2]);

    int[] parent = new int[n + 1];
    for (int i = 0; i <= n; i++) parent[i] = i;

    int cost = 0, edges = 0;
    for (int[] conn : connections) {
        int u = conn[0], v = conn[1], w = conn[2];
        int pu = find(parent, u), pv = find(parent, v);
        if (pu != pv) {
            parent[pu] = pv;  // union
            cost += w;
            edges++;
            if (edges == n - 1) return cost;  // MST complete
        }
    }
    return -1; // cannot connect all cities
}
```
