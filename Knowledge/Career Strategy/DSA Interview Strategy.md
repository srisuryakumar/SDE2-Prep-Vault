---
type: concept
subject: Career Strategy
source_book: "Book 9 — Interview Mastery and Career Strategy"
source_chapter: "Chapter 9 — DSA Interview Strategy"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [career, interview, dsa, strategy]
---

# DSA Interview Strategy

## The 45-Minute Timeline
- **Clarify (2 min):** Restate problem, ask about input size, constraints, edge cases.
- **Examples (5 min):** Walk through 1-2 examples by hand, including an edge case.
- **Approach (3 min):** State approach and complexity *before* coding. Get interviewer nod.
- **Code (25 min):** Write the solution, narrating key decisions.
- **Test (10 min):** Trace through example, test edge cases, fix bugs.

## Clarifying Questions to Always Ask
- **Input Size:** Dictates whether $O(n^2)$ is okay or $O(n \log n)$ is needed.
- **Constraints:** Negatives, duplicates, empty arrays?
- **Output Format:** Indices, values, or boolean?
- **Mutability:** Can I modify the input in place?

## Signaling Pattern Recognition
Say the pattern out loud *with reasoning*, e.g., "I see this as a sliding window problem because we're looking for a contiguous subarray, and brute-force would re-scan overlapping ranges."

## When Stuck
Don't freeze. "I don't see the optimal approach immediately, so let me start with a brute force and look for what we can improve."
Write the brute force, state complexity, identify the bottleneck ("The bottleneck is the repeated linear scan inside the loop").

## Handling "Can you do better?"
Don't just say yes/no. Name a specific complexity target: "I believe we can get this to $O(n)$ by trading space for time — let me think through whether a hashmap lookup replaces the nested loop here."

## Communication While Coding
- **Narrate:** Overall approach, non-obvious decisions, and what you're testing.
- **Silence is okay for:** Straightforward implementation. Constant narration signals nervousness.
