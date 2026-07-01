---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 1 — Algorithmic Thinking and Complexity Analysis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, complexity, rules]
---

# Big-O Simplification Rules

When calculating Big-O, apply these three rules:

## 1. Drop Constants
$O(3n)$ and $O(n)$ are the same complexity class. Only the curve's *shape* matters, not the multiplier. Looping over an array three times in sequence is still $O(n)$.

## 2. Drop Non-Dominant Terms
$O(n^2 + n)$ simplifies to $O(n^2)$, because as $n$ grows, the $n^2$ term completely swamps the $n$ term. 
Similarly, $O(n + \log n) \rightarrow O(n)$. 
*(Common mistake: dropping the *wrong* one — $O(n^2 + n)$ is NOT $O(n)$).*

## 3. Different Inputs Get Different Variables
If a function takes two independent inputs (e.g., two strings of length $n$ and $m$), **do not collapse them into one variable**.
- A function that loops over the first input and then the second is $O(n + m)$, not $O(n)$.
- A function with nested loops, one over each input, is $O(n \times m)$, not $O(n^2)$.
Using a single $n$ when you actually have two independent sizes is a major red flag in interviews.
