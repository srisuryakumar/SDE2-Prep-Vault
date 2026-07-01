---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 13 — Interview Strategy"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, interview, strategy, patterns]
---

# The 15 Core Patterns List

This is the 90-second classifier. Memorize this mapping to instantly recognize patterns.

| Pattern | You see this when the problem says... |
| :--- | :--- |
| **Two Pointers (opposite ends)** | "sorted array", "pair summing to X", "remove duplicates", "reverse in-place", "trap water" |
| **Two Pointers (fast/slow)** | "in-place modification", "move elements", "fast and slow pointer", "find cycle", "middle node" |
| **Sliding Window (fixed)** | "contiguous subarray/substring of size k", "maximum/minimum in every window of size k" |
| **Sliding Window (variable)** | "longest subarray/substring satisfying condition", "minimum window", "at most k distinct characters" |
| **Prefix Sum + HashMap** | "subarray sum equals k", "range sum query", "number of subarrays with property", "pivot index" |
| **Binary Search** | "sorted array", "find target", "minimize maximum", "maximize minimum", "feasibility check on answer" |
| **Monotonic Stack / Deque** | "next greater/smaller element", "largest rectangle", "daily temperatures", "stock span", "visible buildings" |
| **BFS (shortest path)** | "minimum steps", "shortest path unweighted graph", "level-by-level processing", "word ladder" |
| **DFS / Backtracking** | "all combinations", "all permutations", "all subsets", "find path", "N-Queens", "Sudoku", "generate all..." |
| **Union-Find** | "connected components", "is A connected to B", "number of islands (alternative)", "cycle detection" |
| **Trie** | "prefix matching", "autocomplete", "word search", "implement dictionary", "starts with..." |
| **Heap (Top-K / Two-Heap)** | "K largest", "K smallest", "K most frequent", "median from stream", "merge K sorted lists" |
| **DP — 1D** | "count ways", "minimum cost path", "can you reach", "robber pattern", "fibonacci-like", "decode ways" |
| **DP — 2D / Grid** | "unique paths", "minimum path sum", "grid traversal", "interleaving string", "maximal square" |
| **DP — Knapsack / String** | "longest common subsequence", "edit distance", "palindrome subsequence", "0/1 knapsack" |

## Elimination approach when stuck
- Specific pair/triplet in a sorted array? $\rightarrow$ **Two Pointers**
- Contiguous sequence? $\rightarrow$ **Sliding Window or Prefix Sum**
- ALL combinations? $\rightarrow$ **Backtracking**
- MINIMUM number of something? $\rightarrow$ **BFS or DP**
- Connectivity between nodes? $\rightarrow$ **Union-Find or BFS/DFS**
- Sorted structure where you need $O(\log n)$? $\rightarrow$ **Binary Search**
