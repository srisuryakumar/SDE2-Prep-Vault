---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 1 — Algorithmic Thinking and Complexity Analysis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, complexity, amortized]
---

# Amortized Analysis

Amortized analysis answers: "What is the average cost over many operations?" rather than "What is the worst-case cost of this *one* operation?"

## Example: `ArrayList.add()` is $O(1)$ Amortized
A Java `ArrayList` has a fixed backing array. When it fills up, it must allocate a new, bigger array and copy all existing elements into it. 

The specific call to `add()` that triggers this resize takes **$O(n)$** time. 
However, if we double the capacity each time (1, 2, 4, 8, ... n), the sum of all copies made across $n$ insertions is bounded by $2n$.

Total work for $n$ inserts = $O(n)$ (for the inserts themselves) + $O(2n)$ (for all copies combined) = $O(n)$.
Average work per insert = $O(n) / n = \mathbf{O(1)}$.

The expensive operations are so rare, and shrink so fast in relative frequency, that the average cost converges to a constant.
