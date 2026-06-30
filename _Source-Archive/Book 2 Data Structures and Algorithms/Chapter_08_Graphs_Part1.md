# Chapter 8: Graphs
## Part 1 — Representations · BFS · DFS

*Graphs are the chapter where "pick the right traversal" stops being optional. BFS and DFS look almost identical in code — a container and a loop — but they guarantee completely different things, and this chapter is about knowing which guarantee you actually need before you write a single line.*

## 8.1 Graph Representations

**Adjacency list** — a map (or array) of lists, where `graph[node]` holds that node's neighbors (and weights, if weighted). Preferred for **sparse** graphs (most real-world graphs, where E ≪ V²): space is O(V + E), and visiting a node's neighbors costs O(degree), not O(V).

**Adjacency matrix** — a V×V grid where `matrix[i][j]` holds the edge weight between i and j (or 0/∞ for "no edge"). O(V²) space *regardless* of edge count — wasteful for sparse graphs, but gives O(1) "does this edge exist" lookups, which matters for **dense** graphs or algorithms that query edge existence constantly (Floyd-Warshall, later in this chapter, is built around exactly this).

```
Graph: vertices {0,1,2,3}, edges {(0,1),(0,2),(1,2),(2,3)}

Adjacency List:                Adjacency Matrix:
0: [1, 2]                           0  1  2  3
1: [0, 2]                        0 [0, 1, 1, 0]
2: [0, 1, 3]                     1 [1, 0, 1, 0]
3: [2]                           2 [1, 1, 0, 1]
                                  3 [0, 0, 1, 0]
```

**Building an adjacency list from an edge list:**

```java
public List<List<Integer>> buildAdjacencyList(int n, int[][] edges) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        graph.add(new ArrayList<>());
    }
    for (int[] edge : edges) {
        int u = edge[0], v = edge[1];
        graph.get(u).add(v);
        graph.get(v).add(u);   // omit this line for a DIRECTED graph
    }
    return graph;
}
```

---

## 8.2 BFS (Breadth-First Search)

### Template

```java
public void bfs(int start, List<List<Integer>> graph) {
    Set<Integer> visited = new HashSet<>();
    Queue<Integer> queue = new ArrayDeque<>();
    queue.offer(start);
    visited.add(start);

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

### What BFS Guarantees

BFS explores nodes in strictly increasing order of distance from the start — every node at distance d is fully processed, and everything it enqueues at distance d+1 waits in the queue, before any distance-(d+1) node is itself dequeued. That level-by-level discipline is exactly what guarantees **shortest paths in unweighted graphs** — and exactly why it does *not* extend to weighted graphs: BFS only ever counts edges, with zero awareness that a path with fewer edges might have a larger total weight than a path with more, cheaper edges. (Dijkstra's algorithm, later in this chapter, is BFS's weighted-graph replacement.)

**Tracking distance level by level:**

```java
public Map<Integer, Integer> bfsDistances(int start, List<List<Integer>> graph) {
    Map<Integer, Integer> distance = new HashMap<>();
    Queue<Integer> queue = new ArrayDeque<>();
    queue.offer(start);
    distance.put(start, 0);

    while (!queue.isEmpty()) {
        int node = queue.poll();
        for (int neighbor : graph.get(node)) {
            if (!distance.containsKey(neighbor)) {
                distance.put(neighbor, distance.get(node) + 1);
                queue.offer(neighbor);
            }
        }
    }
    return distance;
}
```

### Multi-Source BFS

Instead of starting from one node, seed the queue with **multiple** starting nodes simultaneously, all at distance 0. BFS's level-by-level guarantee still holds — it just now finds, for every node, the distance to its *nearest* source, because every source begins tied at distance 0 and the frontier expands from all of them in lockstep.

```java
Queue<int[]> queue = new ArrayDeque<>();
for (int[] source : sources) {
    queue.offer(source);
    visited.add(source);
}
// ...then the standard BFS loop
```

This does the whole job in one O(V + E) pass — running ordinary single-source BFS separately from each source and taking the minimum would cost O(sources × (V + E)) instead.

---

## 8.3 DFS (Depth-First Search)

**Recursive, with a visited set:**

```java
public void dfs(int node, List<List<Integer>> graph, Set<Integer> visited) {
    visited.add(node);
    // process node
    for (int neighbor : graph.get(node)) {
        if (!visited.contains(neighbor)) {
            dfs(neighbor, graph, visited);
        }
    }
}
```

**Iterative, with an explicit stack:**

```java
public void dfsIterative(int start, List<List<Integer>> graph) {
    Set<Integer> visited = new HashSet<>();
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(start);

    while (!stack.isEmpty()) {
        int node = stack.pop();
        if (visited.contains(node)) continue;   // may have been pushed more than once
        visited.add(node);
        // process node
        for (int neighbor : graph.get(node)) {
            if (!visited.contains(neighbor)) {
                stack.push(neighbor);
            }
        }
    }
}
```

Notice the `continue` guard right after popping — unlike BFS (which marks visited *before* enqueueing, preventing duplicates from ever entering the queue), this iterative DFS commonly marks visited *after* popping, so the same node can land on the stack more than once before its first pop. The guard handles that cleanly.

**What DFS is for:**
- **Connected components** — run DFS from every unvisited node; each fresh start marks one entire component. The number of times you start a *new* DFS is the number of components.
- **Cycle detection** — in an undirected graph, finding a visited node that isn't the immediate parent means a cycle. In a directed graph, this needs a stronger check (a node currently *in progress* on the current path, not just visited at some point) — this exact distinction is what Topological Sort's cycle detection in Part 2 is built on.
- **Path finding** — DFS naturally explores one path to its end before backtracking, which is the right shape for "does a path exist," or (combined with backtracking, Chapter 11) enumerating every path.

---

## Problem — Number of Islands (LeetCode 200)

**Statement.** Given a 2D grid of `'1'` (land) and `'0'` (water), count the islands (land cells connected horizontally/vertically).

**Approach.** Treat each grid cell as a graph node with edges to its (up to) 4 orthogonal land neighbors. Run DFS from every unvisited land cell, marking the entire connected island as visited along the way; every time a *fresh* DFS gets started, that's one new island.

```java
public int numIslands(char[][] grid) {
    int rows = grid.length, cols = grid[0].length;
    int islands = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == '1') {
                islands++;
                sink(grid, r, c);   // mark the entire connected island as visited
            }
        }
    }
    return islands;
}

private void sink(char[][] grid, int r, int c) {
    if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] != '1') {
        return;   // out of bounds, water, or already visited
    }
    grid[r][c] = '0';   // mark visited by sinking — avoids a separate visited set
    sink(grid, r + 1, c);
    sink(grid, r - 1, c);
    sink(grid, r, c + 1);
    sink(grid, r, c - 1);
}
```

**Trace** on:

```
1 1 0
0 1 0
0 0 1
```

```
(0,0)='1' → islands=1. sink(0,0): sinks (0,0),(0,1),(1,1) — the whole connected blob.
Grid becomes:
0 0 0
0 0 0
0 0 1

(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1) all now '0' → skipped.
(2,2)='1' → islands=2. sink(2,2): no land neighbors, sinks just itself.

Final islands = 2   ✓
```

**Complexity:** Time O(rows × cols) — every cell visited at most once. Space O(rows × cols) worst case for the recursion stack (one giant connected island).

**Common mistakes:** forgetting to mark cells visited (here, sinking to `'0'`), causing infinite/redundant re-exploration; checking `grid[r][c]` *before* the bounds check, which throws — the bounds check must come first (the `||` short-circuit in the code above already guarantees this ordering).

---

## Problem — Clone Graph (LeetCode 133)

**Statement.** Given a node in a connected undirected graph, return a deep copy of the entire graph.

**Approach.** DFS from the given node, maintaining a `HashMap<originalNode, clonedNode>` for two reasons at once: avoid cloning the same node twice, and survive cycles (without memoization, a cyclic graph would recurse forever).

```java
public Node cloneGraph(Node node) {
    if (node == null) return null;
    Map<Node, Node> visited = new HashMap<>();
    return dfs(node, visited);
}

private Node dfs(Node node, Map<Node, Node> visited) {
    if (visited.containsKey(node)) {
        return visited.get(node);   // already cloned — reuse, don't recurse again
    }
    Node clone = new Node(node.val);
    visited.put(node, clone);        // register BEFORE recursing into neighbors — this is what breaks cycles
    for (Node neighbor : node.neighbors) {
        clone.neighbors.add(dfs(neighbor, visited));
    }
    return clone;
}
```

**Why registering the clone before recursing into neighbors is essential.** If node A and node B are mutual neighbors, cloning A triggers cloning B — and without A already sitting in the map, B's recursive call would try to clone A all over again, looping forever. Registering A's clone immediately means B's call finds A already mapped and reuses it instead.

**Trace** on a 2-node mutual graph (`1` and `2` are each other's only neighbor):

```
dfs(1, {}): not in map. clone1=Node(1). map={1:clone1}.
  neighbor 2: dfs(2, map):
    not in map. clone2=Node(2). map={1:clone1, 2:clone2}.
    neighbor 1: dfs(1, map): 1 IS in map → return clone1.
    clone2.neighbors = [clone1].
    return clone2.
  clone1.neighbors = [clone2].
return clone1.

Final: clone1.neighbors=[clone2], clone2.neighbors=[clone1] — mirrors the original exactly,
no infinite recursion.   ✓
```

**Complexity:** Time O(V + E). Space O(V) for the map plus O(V) recursion stack worst case.

---

## Problem — Pacific Atlantic Water Flow (LeetCode 417) — Multi-Source BFS, Reversed

**Statement.** Given a grid of heights, water flows from a cell to an adjacent cell with height ≤ the current cell's. Find every cell from which water can reach *both* the Pacific (top/left borders) and the Atlantic (bottom/right borders).

**Why the obvious approach is too slow.** Checking "can this cell reach the Pacific" independently, for every one of `rows × cols` cells, costs O(rows × cols) per cell in the worst case — O((rows · cols)²) total.

**The reversal that fixes it.** Instead of asking "can water flow *from* this cell *to* the ocean," flip the question: "could water have flowed *into* this cell *from* the ocean, walking the flow direction backward?" Run multi-source BFS starting from *every* border cell at once — once for the Pacific borders, once for the Atlantic — but step to a neighbor only if `height[neighbor] ≥ height[current]` (the reverse of the forward flow rule, since forward flow requires the source to be at least as high as the destination). One BFS pass per ocean finds every cell that ocean's water could have originated from — exactly the cells that can flow *to* that ocean. The answer is the intersection of the two reachable sets.

```java
public List<List<Integer>> pacificAtlantic(int[][] heights) {
    int rows = heights.length, cols = heights[0].length;
    boolean[][] pacificReachable = new boolean[rows][cols];
    boolean[][] atlanticReachable = new boolean[rows][cols];
    Queue<int[]> pacificQueue = new ArrayDeque<>();
    Queue<int[]> atlanticQueue = new ArrayDeque<>();

    for (int r = 0; r < rows; r++) {
        pacificQueue.offer(new int[]{r, 0});          pacificReachable[r][0] = true;
        atlanticQueue.offer(new int[]{r, cols - 1});  atlanticReachable[r][cols - 1] = true;
    }
    for (int c = 0; c < cols; c++) {
        pacificQueue.offer(new int[]{0, c});           pacificReachable[0][c] = true;
        atlanticQueue.offer(new int[]{rows - 1, c});   atlanticReachable[rows - 1][c] = true;
    }

    bfs(heights, pacificQueue, pacificReachable);
    bfs(heights, atlanticQueue, atlanticReachable);

    List<List<Integer>> result = new ArrayList<>();
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (pacificReachable[r][c] && atlanticReachable[r][c]) {
                result.add(Arrays.asList(r, c));
            }
        }
    }
    return result;
}

private void bfs(int[][] heights, Queue<int[]> queue, boolean[][] reachable) {
    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
    while (!queue.isEmpty()) {
        int[] curr = queue.poll();
        for (int[] dir : dirs) {
            int nr = curr[0] + dir[0], nc = curr[1] + dir[1];
            if (nr < 0 || nr >= heights.length || nc < 0 || nc >= heights[0].length) continue;
            if (reachable[nr][nc]) continue;
            if (heights[nr][nc] < heights[curr[0]][curr[1]]) continue;   // reversed flow condition
            reachable[nr][nc] = true;
            queue.offer(new int[]{nr, nc});
        }
    }
}
```

**Trace** on a grid with a single low cell surrounded by higher land:

```
5 5 5
5 1 5
5 5 5
```

Pacific borders (row 0 + column 0) are the five cells `{(0,0),(0,1),(0,2),(1,0),(2,0)}`, all height 5. Reverse-BFS from these: every neighboring height-5 cell accepts the step (`5 ≥ 5`), so the search spreads around the entire height-5 ring — `(2,1), (2,2), (1,2)` all become Pacific-reachable in turn. The **only** cell never reached is the center, height 1: at every attempt to step into it, `height[center]=1 < height[current]=5`, so the reverse condition fails and the search refuses to enter.

The identical logic applies to the Atlantic borders (row 2 + column 2), and by the ring's symmetry, the Atlantic-reachable set is also every cell except the center.

**Intersection = all 8 ring cells.** The center is excluded from both — correctly: it's a local minimum surrounded entirely by higher land, with nowhere downhill to flow at all.

**Complexity:** O(rows × cols) — each ocean's BFS visits every cell at most once.

---

## Problem — Word Ladder (LeetCode 127) — BFS, the Tricky One

**Statement.** Given `beginWord`, `endWord`, and a `wordList`, find the length of the shortest transformation sequence from begin to end, changing one letter at a time, where every intermediate word must exist in `wordList`. Return 0 if impossible.

**Why this is BFS in disguise.** Treat every word as a node in an implicit graph, with an edge between two words that differ by exactly one letter. "Shortest transformation sequence" is then literally "shortest path in an unweighted graph" — precisely what BFS guarantees. The graph just isn't handed to you explicitly; you have to generate each word's neighbors on the fly.

**Why it's tricky.** The naive way to find a word's neighbors — compare it against every other word in `wordList` — costs O(L) comparisons of O(W) length each, for every word, at every BFS step: O(L² · W) worst case, far too slow. The fix: instead of searching the list, **generate** every possible one-letter-changed variant of the current word directly (every position, all 26 letters) — O(W · 26) candidates — and check each one against a `HashSet` of `wordList` in O(1). This is the same "construct candidates and check membership" reflex from Chapter 5's complement lookup, applied here to implicit graph-neighbor generation instead of array elements.

```java
public int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> wordSet = new HashSet<>(wordList);
    if (!wordSet.contains(endWord)) return 0;

    Queue<String> queue = new ArrayDeque<>();
    queue.offer(beginWord);
    Set<String> visited = new HashSet<>();
    visited.add(beginWord);
    int steps = 1;

    while (!queue.isEmpty()) {
        int levelSize = queue.size();
        for (int i = 0; i < levelSize; i++) {
            String word = queue.poll();
            if (word.equals(endWord)) return steps;

            char[] chars = word.toCharArray();
            for (int pos = 0; pos < chars.length; pos++) {
                char original = chars[pos];
                for (char c = 'a'; c <= 'z'; c++) {
                    if (c == original) continue;
                    chars[pos] = c;
                    String candidate = new String(chars);
                    if (wordSet.contains(candidate) && !visited.contains(candidate)) {
                        visited.add(candidate);
                        queue.offer(candidate);
                    }
                }
                chars[pos] = original;   // restore before moving to the next position
            }
        }
        steps++;
    }
    return 0;   // endWord unreachable
}
```

**Trace** on `beginWord="hit"`, `endWord="cog"`, `wordList=["hot","dot","dog","lot","log","cog"]`:

```
wordSet={hot,dot,dog,lot,log,cog}.  "cog" present → proceed.
queue=[hit], visited={hit}, steps=1.

Process "hit" → not endWord. Variant "hot" (i→o) is in wordSet, unvisited → add.
queue=[hot].  steps becomes 2.

Process "hot" → not endWord. Variants "dot" (h→d) and "lot" (h→l) both in wordSet → add both.
queue=[dot,lot].  steps becomes 3.

Process "dot" → not endWord. Variant "dog" (t→g) → add.
Process "lot" → not endWord. Variant "log" (t→g) → add.
queue=[dog,log].  steps becomes 4.

Process "dog" → not endWord. Variant "cog" (d→c) → add.
Process "log" → not endWord. Variant "cog" already visited (just added by "dog") → skip.
queue=[cog].  steps becomes 5.

Process "cog" → word.equals(endWord) → return steps = 5.

Final answer: 5   (hit → hot → dot → dog → cog, a path of 5 words)   ✓
```

**Complexity:** Time roughly O(L · W² · 26) — at most L words get processed (bounded by `wordList` size), each generating O(W · 26) candidates, each candidate costing O(W) to construct. Space O(L · W) for the word set and visited set.

**Common mistakes:**
- **Comparing against every word in the list** instead of generating candidates directly — the O(L² · W) trap this whole approach exists to avoid.
- **Forgetting to restore `chars[pos] = original`** after trying all 26 replacements at a position — corrupts every later position's candidate generation.
- **Not checking `endWord` is in `wordSet` up front** — if it's missing, no path can ever reach it (every word in the sequence except `beginWord` itself must be in the dictionary).
- **Marking visited at poll-time instead of add-time.** Marking at add-time (as shown) prevents the same word from being enqueued multiple times by different same-level words before any of them gets processed — marking late would waste work, or even corrupt the level count.

---

*Part 2 covers Union-Find (with both optimizations, full implementation from scratch) and Topological Sort (Kahn's algorithm and the DFS-based version), applied across Redundant Connection, Number of Connected Components, Course Schedule, and Course Schedule II.*
