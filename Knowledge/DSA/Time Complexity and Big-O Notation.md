---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 1 — Algorithmic Thinking and Complexity Analysis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, complexity, big-o, time-complexity]
---

# Time Complexity and Big-O Notation

We don't measure algorithms in seconds (which depend on hardware and language). We measure them in **elementary operations** as a function of the input size $n$. 

## Big-O Notation
Big-O is an **upper bound** on growth rate — it says "no worse than this".
Formally: $f(n) = O(g(n))$ if there exist positive constants $c$ and $n_0$ such that $f(n) \le c \cdot g(n)$ for all $n \ge n_0$.

In plain language: past some starting point, the work required grows no faster than a constant multiple of $g(n)$.
- If an algorithm is $O(n)$, doubling the input doubles the work.
- If an algorithm is $O(n^2)$, doubling the input roughly quadruples the work.

Big-O tells you how pain scales, not how much pain there is right now. A solution that takes $O(n^2)$ might run instantly for $n=100$, but will likely time out for $n=1,000,000$.

*(Note: Big-$\Omega$ is a lower bound, Big-$\Theta$ is a tight bound. Interviews default to Big-O because they care about the worst case).*
