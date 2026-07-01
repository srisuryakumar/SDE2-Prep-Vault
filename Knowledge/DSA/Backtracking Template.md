---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 11 — Backtracking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, backtracking, template]
---

# Backtracking Template

## Intuition
Backtracking is essentially Depth-First Search (DFS) over an implicit decision tree, with one extra crucial discipline: **undo every choice before trying its sibling**.

The efficiency comes from "pruning"—abandoning a partial solution the *instant* it's clear it can't lead anywhere valid, rather than generating every complete candidate and checking validity at the end.

## Template: Choose $\rightarrow$ Explore $\rightarrow$ Unchoose
```java
void backtrack(/* current state, parameters */) {
    if (/* base case: complete solution found */) {
        result.add(/* copy of current state */);
        return;
    }
    
    for (/* each possible choice at this point */) {
        if (/* choice is invalid — prune */) continue;

        currentState.add(choice);          // CHOOSE
        backtrack(/* updated parameters */); // EXPLORE
        currentState.remove(currentState.size() - 1); // UNCHOOSE
    }
}
```

**CRITICAL RULE:** Forgetting to unchoose is the single most common backtracking bug. It silently corrupts every branch that runs after the first one, because the `currentState` variable is passed by reference across recursive calls.

## When to Reach for Backtracking
- "Find all X" or "does there exist an X"
- X is built incrementally
- Partial validity can be checked *before* the structure is complete (allowing pruning).
