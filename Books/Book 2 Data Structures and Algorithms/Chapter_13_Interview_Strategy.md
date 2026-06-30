# Chapter 13: Interview Strategy

*Twelve chapters built the toolkit. This one is about what to actually do with it when you're sitting across from an interviewer, a blank screen, and a problem you've never seen before.*

## 13.1 How to Approach an Unseen Problem: Clarify → Example → Pattern → Code → Test

### Step 1 — Clarify

Before thinking about a solution, ask clarifying questions. This isn't stalling — it's the highest-leverage thirty seconds of the entire interview, because solving the *wrong* problem perfectly is worse than asking one good question.

What to clarify: **input constraints** (value range, can the array be empty, duplicates, negatives, is it sorted), **output format** (exact return type, what to do on edge cases — return -1? throw? empty list?), and **ambiguous wording** ("smallest" — value or index? "substring" vs. "subsequence" — contiguous or not?).

### Step 2 — Example

Work through one or two concrete examples by hand *before* writing any code — including at least one edge case (Section 13.6). This does two things at once: it confirms your understanding matches the interviewer's, catching misunderstandings before they cost ten minutes of wasted coding, and it often *reveals* the pattern itself — walking through a real trace by hand is frequently how the right approach becomes obvious in the first place. Every single trace in this book has been demonstrating exactly that: seeing the mechanism work on real numbers is what makes an abstract recurrence or template concrete.

### Step 3 — Pattern

Name the pattern out loud. Start with Chapter 1's lens — "what's the brute force, and what's its complexity" — then ask which of this book's templates the structure matches: *"This looks like a sliding window problem, since we need the longest substring satisfying a condition,"* or *"this is graph reachability, so BFS or DFS."* Naming it out loud, before coding, gives the interviewer a chance to confirm you're headed the right way — or redirect you *early*, before ten minutes of coding the wrong approach.

### Step 4 — Code

Write the solution, talking through the *structure* as you go ("I'll use two pointers here, one from each end") rather than narrating every keystroke. Use this book's templates as scaffolding, not something to recite from memory under pressure — understanding *why* a template has the shape it has (which every chapter spent real effort explaining, not just handing you the code) is what lets you adapt it when the interviewer's exact problem doesn't match a memorized example perfectly.

### Step 5 — Test

Trace through your *own* code on the examples from Step 2 — especially the edge case — out loud, pointing at each line. This catches bugs before the interviewer runs the code, and it's the exact habit every "Trace" section in this book has been modeling for you to internalize and reproduce live, under pressure.

---

## 13.2 The 15 Core Patterns and Their Recognition Signals

A consolidated cheat sheet, pulling every chapter's "Pattern Recognition Guide" into one place. Treat this as flashcard material — the goal is instant recognition, not re-deriving from first principles every time.

1. **Two Pointers (Opposite Ends)** — sorted array, pair/triple satisfying a condition.
2. **Two Pointers (Same Direction)** — in-place partition/filter preserving order.
3. **Sliding Window (Fixed)** — subarray/substring of exactly size k.
4. **Sliding Window (Variable)** — longest/shortest subarray/substring satisfying a condition.
5. **Prefix Sum (+ HashMap)** — range sum queries, or subarray sum equals k (complement lookup over running sums).
6. **HashMap/HashSet** — counting, deduplication, "have I seen this before."
7. **Fast-Slow Pointers** — linked list middle, cycle detection.
8. **Monotonic Stack (or Deque)** — next greater/smaller element, histogram-shaped area, sliding window max.
9. **Heap (Top-K / Two-Heap)** — k largest/smallest/closest, streaming median, greedy scheduling.
10. **Tree DFS Template** — any bottom-up tree aggregate (depth, balance, diameter, path sum).
11. **BFS/DFS on Graphs** — shortest path (unweighted), connected components, cycle detection.
12. **Union-Find** — dynamic connectivity, MST (Kruskal's).
13. **Dynamic Programming** — state → recurrence → base case; five sub-patterns (linear, grid, knapsack, string, state machine).
14. **Backtracking** — choose → explore → unchoose; generate all X, or find one X via existence search.
15. **Binary Search (standard + on-the-answer)** — sorted search, or "minimum/maximum value with a monotonic feasibility check."

This deliberately compresses twelve chapters' worth of named techniques — graphs alone had BFS, DFS, Union-Find, topological sort, Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal's, and Prim's — into 15 high-level buckets, because that's the resolution pattern recognition actually operates at under interview pressure. You don't need to instantly distinguish Dijkstra from Bellman-Ford before you've even confirmed "this is a graph shortest-path problem." Recognize the bucket first; narrow down within it second.

---

## 13.3 Time Management: The 25-Minute Rule

A typical 45–60 minute slot needs to fit introductions (2–3 min), the problem statement and your clarifying questions (3–5 min), your solution (the bulk), and buffer for follow-ups or a second problem. That leaves roughly 25–30 minutes for one medium problem, start to finish.

**Rough budget:** Clarify + Example: 3–5 min. Identify pattern + talk through approach: 3–5 min. Code: 12–15 min. Test + discuss complexity: 3–5 min.

If you're 15 minutes in with no working approach, that's the signal to either fall back to a brute-force solution you *know* works — saying so explicitly ("I see an O(n²) approach; let me start there and look for ways to optimize") — or ask for a hint (Section 13.4). A correct O(n²) solution with 5 minutes left to discuss optimization is almost always a better outcome than running out of time with nothing working at all.

---

#### The 15 Pattern Recognition Signals — Your 90-Second Classifier

Pattern recognition is the skill that separates experienced candidates from
struggling ones. An experienced candidate reads a problem and within 90 seconds
names the pattern. Everything after that is implementation — which you can do.

Study this table until you can cover the "You see this when..." column and
predict it from the pattern name alone.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PATTERN              │ YOU SEE THIS WHEN THE PROBLEM SAYS...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Two Pointers         │ "sorted array", "pair summing to X", "remove
 (opposite ends)      │ duplicates", "reverse in-place", "trap water"
 ─────────────────────┼────────────────────────────────────────────────────
 Two Pointers         │ "in-place modification", "move elements", "fast
 (fast/slow)          │ and slow pointer", "find cycle", "middle node"
 ─────────────────────┼────────────────────────────────────────────────────
 Sliding Window       │ "contiguous subarray/substring of size k",
 (fixed)              │ "maximum/minimum in every window of size k"
 ─────────────────────┼────────────────────────────────────────────────────
 Sliding Window       │ "longest subarray/substring satisfying condition",
 (variable)           │ "minimum window", "at most k distinct characters"
 ─────────────────────┼────────────────────────────────────────────────────
 Prefix Sum           │ "subarray sum equals k", "range sum query",
 + HashMap            │ "number of subarrays with property", "pivot index"
 ─────────────────────┼────────────────────────────────────────────────────
 Binary Search        │ "sorted array", "find target", "minimize maximum",
                      │ "maximize minimum", "feasibility check on answer"
 ─────────────────────┼────────────────────────────────────────────────────
 Monotonic Stack      │ "next greater/smaller element", "largest rectangle",
                      │ "daily temperatures", "stock span", "visible buildings"
 ─────────────────────┼────────────────────────────────────────────────────
 BFS (shortest path)  │ "minimum steps", "shortest path unweighted graph",
                      │ "level-by-level processing", "word ladder"
 ─────────────────────┼────────────────────────────────────────────────────
 DFS / Backtracking   │ "all combinations", "all permutations", "all subsets",
                      │ "find path", "N-Queens", "Sudoku", "generate all..."
 ─────────────────────┼────────────────────────────────────────────────────
 Union-Find           │ "connected components", "is A connected to B",
                      │ "number of islands (alternative)", "cycle detection"
 ─────────────────────┼────────────────────────────────────────────────────
 Trie                 │ "prefix matching", "autocomplete", "word search",
                      │ "implement dictionary", "starts with..."
 ─────────────────────┼────────────────────────────────────────────────────
 Heap (Top-K)         │ "K largest", "K smallest", "K most frequent",
                      │ "median from stream", "merge K sorted lists"
 ─────────────────────┼────────────────────────────────────────────────────
 DP — 1D              │ "count ways", "minimum cost path", "can you reach",
                      │ "robber pattern", "fibonacci-like", "decode ways"
 ─────────────────────┼────────────────────────────────────────────────────
 DP — 2D / Grid       │ "unique paths", "minimum path sum", "grid traversal",
                      │ "interleaving string", "maximal square"
 ─────────────────────┼────────────────────────────────────────────────────
 DP — Knapsack /      │ "longest common subsequence/subsequence", "edit
 String               │ distance", "palindrome subsequence", "0/1 knapsack"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**How to use this table during practice:**

After reading any LeetCode problem, before looking at hints or solutions:
1. Underline the key phrases in the problem statement
2. Map each phrase to a row in the table above
3. Name the pattern out loud: "I see this as a sliding window problem because..."
4. If two patterns match, pick the one with lower time complexity
5. Only then open your editor and start coding

**The elimination approach when stuck:**

If you cannot identify the pattern immediately, eliminate:
- Is it asking for a specific pair/triplet in a sorted array? → Two Pointers
- Is it asking for something contiguous? → Sliding Window or Prefix Sum
- Is it asking for ALL combinations? → Backtracking
- Is it asking for the MINIMUM number of something? → BFS or DP
- Is it asking about connectivity between nodes? → Union-Find or BFS/DFS
- Does it involve a sorted structure where you need log(n)? → Binary Search

**Recognition speed targets:**
- Week 1–4: 3–5 minutes to identify pattern
- Week 5–8: 90 seconds to identify pattern
- Week 9–12: 60 seconds to identify pattern
- Week 13–17: 30 seconds to identify pattern (interview-ready)

---

## 13.4 When to Ask for Hints vs. Push Through

**Push through a bit longer when:** you have a partial idea you haven't fully tested; you're making incremental progress (narrowing down what doesn't work); you've been stuck under 5 minutes.

**Ask for a hint when:** you've been completely stuck — no concrete next step, not even a brute-force direction — for more than 5–7 minutes; you've tried 2–3 different angles that all failed the same way (suggesting a key insight a hint could supply directly, not just more time); the clock is a real constraint and a hint would let you demonstrate the *rest* of your ability — coding, testing, complexity analysis — even if the core insight needed a nudge.

Asking for a hint isn't a failure — interviewers expect it, and *how* you use one (immediately running with it, vs. staying lost) is itself signal. Sitting in silence for ten minutes, unwilling to ask, is a worse outcome than asking at minute 6 and solving the rest cleanly.

---

## 13.5 Stating Complexity Before You Start Coding

Chapter 1's interview rule, restated because it belongs at *every* stage, not just the end: after identifying your approach (Step 3) but *before* writing code (Step 4), state the time and space complexity you expect the solution to have. This does three things — gives the interviewer an immediate chance to say "can you do better" before you've spent ten minutes coding something they hoped you'd improve on; forces you to have already thought through the approach's real cost, catching cases where a "clever" idea is secretly no better than brute force; and builds the habit that prevents the embarrassing scenario of finishing a solution and being unable to state its own complexity when asked.

---

## 13.6 Edge Cases to Always Check

Before declaring a solution "done," run this checklist — even unprompted:

- **Empty input** — empty array, empty string, null. Does the solution handle size 0 gracefully, or crash on an out-of-bounds access? (Chapter 2's binary search, Chapter 3's linked list traversal, and Chapter 6's tree base cases all depend on correctly handling "nothing here" as the very first check.)
- **Single element** — does a one-element input break any two-pointer or sliding-window logic that implicitly assumes at least two elements to compare?
- **All elements the same** — does the solution silently assume strict ordering somewhere it shouldn't (Chapter 2's binary search variants; Chapter 10's LIS, which explicitly distinguishes strictly-increasing from non-decreasing)?
- **Negative numbers** — does an assumption of non-negative values break (Chapter 2's Kadane's algorithm handles this explicitly; many binary-search-on-the-answer setups assume a positive search range — check whether *this* problem's constraints actually guarantee that)?
- **Integer overflow** — for sums, products, or anything that could exceed `Integer.MAX_VALUE` (Chapter 1 flagged `(lo+hi)/2` vs. `lo+(hi-lo)/2` as the canonical example; Chapter 8's Floyd-Warshall used `Integer.MAX_VALUE/2` as a deliberately safe "infinity" specifically to avoid overflow when summing two of them).

Not every problem needs all five checked carefully, but running the list takes ten seconds and catches a meaningful fraction of bugs that would otherwise only surface during the interviewer's own test cases.

---

## 13.7 How to Handle Getting Stuck: Backtrack to Brute Force, Optimize From There

When the optimal approach isn't coming, don't sit frozen. Fall back to the brute-force solution you're confident is *correct*, even if it's slow — say so explicitly, and start coding it. This accomplishes several things at once: writing the brute force often reveals the optimization directly (you'll notice, while writing the nested loops, exactly *where* the redundant work is happening — precisely how this book introduced nearly every pattern: start from brute force, identify the redundant work, apply the matching technique to eliminate it). It also guarantees you have *something* working, which beats an ambitious-but-incomplete optimal attempt. And it buys time to keep thinking about the optimization while your hands stay productively occupied writing code you already know is correct.

This is, in miniature, this entire book's arc: Chapter 1 taught you to identify complexity and spot redundant work; Chapters 2–12 taught the specific techniques that eliminate that redundancy in different shapes. Getting stuck in an interview is just "I've identified the brute force but haven't matched it to a pattern yet" — and the fix is the same motion this book has practiced repeatedly: name what's redundant, then ask which of the 15 patterns (Section 13.2) removes redundancy of exactly that shape.

---

## A Final Word

Thirteen chapters, more than 30 named patterns, and close to 100 fully-traced problems later, the actual claim this book has been making is simpler than it looks: there's no such thing as a genuinely *new* LeetCode medium. Every problem is one of the patterns in Section 13.2, wearing a costume specific to that problem's surface details. The work between now and your next interview isn't memorizing more problems — it's getting fast and confident at stripping the costume off and naming the pattern underneath, using exactly the clarify → example → pattern → code → test loop this chapter just laid out.

Go through the patterns one more time. Then go solve something.
