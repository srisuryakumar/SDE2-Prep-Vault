---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 13 — Interview Strategy"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, interview, strategy, process]
---

# Interview Strategy (5 Steps)

## How to Approach an Unseen Problem

### Step 1 — Clarify
Before thinking about a solution, ask clarifying questions. This is the highest-leverage 30 seconds of the interview.
- **Input constraints:** value range, empty arrays, duplicates, negatives, sorted or not?
- **Output format:** return type, edge cases (return -1, throw exception, empty list?)
- **Ambiguity:** "smallest" value or index? "substring" (contiguous) or "subsequence" (non-contiguous)?

### Step 2 — Example
Work through 1-2 concrete examples by hand *before* writing any code. Include at least one edge case.
This confirms understanding, catches misunderstandings, and often *reveals* the pattern.

### Step 3 — Pattern
Name the pattern out loud. Start with the brute force time/space complexity, then ask which of the 15 core patterns fits the structure.
Naming it out loud gives the interviewer a chance to confirm you are on the right track or redirect you early.

### Step 4 — Code
Write the solution, talking through the *structure* as you go (not every keystroke). Use standard templates as scaffolding, but adapt them as needed.

### Step 5 — Test
Trace through your own code on the examples from Step 2 *out loud*, pointing at each line. Catch bugs before the interviewer runs the code.

## The 25-Minute Rule
- Clarify + Example: 3-5 min
- Identify pattern + Talk approach: 3-5 min
- Code: 12-15 min
- Test + Discuss complexity: 3-5 min

**When stuck (15 min in):** Fall back to a brute-force solution explicitly. A working $O(n^2)$ solution with 5 minutes left is better than no solution.

## Edge Cases to Always Check
1. **Empty input** (null, size 0).
2. **Single element**.
3. **All elements the same** (strict ordering assumed?).
4. **Negative numbers** (does a monotonic assumption break?).
5. **Integer overflow** (sums, products).
