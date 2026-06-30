# DSA Interview Strategy

### The 45-minute timeline

| Phase | Time | What happens |
|---|---|---|
| Clarify | 2 min | Restate the problem, ask about input size, constraints, edge cases |
| Examples | 5 min | Walk through 1–2 examples by hand, including at least one edge case |
| Approach | 3 min | State your approach and its complexity *before* coding, get a nod from the interviewer |
| Code | 25 min | Write the solution, narrating key decisions, not every line |
| Test | 10 min | Trace through your example, test edge cases, fix anything that breaks |

Treat these as soft targets, not a rigid stopwatch — but if you're 15 minutes in and still "clarifying," that's a signal to move yourself along.

### Clarifying questions to always ask

- **Input size:** "What's the expected size of the input — does that change which approach makes sense?" (This single question often tells you whether O(n²) is fine or whether you need O(n log n).)
- **Constraints:** "Can the input contain negative numbers / duplicates / empty arrays?" — directly shapes which edge cases you need to handle.
- **Output format:** "Should I return the indices, the values, or a boolean?" — avoids building the wrong thing correctly.
- **Mutability:** "Can I modify the input in place, or should I treat it as read-only?"

### How to signal pattern recognition

Say the pattern out loud as you recognize it, with the reasoning attached — not just the label: *"I see this as a sliding window problem because we're looking for a contiguous subarray satisfying a condition, and brute-force would re-scan overlapping ranges unnecessarily."* This does two things: it shows the interviewer your reasoning process, not just your memorized pattern library, and it gives them a chance to correct you early if you've mis-pattern-matched, before you've written 20 lines of code down the wrong path.

### When stuck: brute force out loud, optimize from there

If the optimal approach isn't coming to you, say so directly rather than going silent: *"I don't see the optimal approach immediately, so let me start with a brute force and look for what we can improve."* Write the brute force, state its complexity, then explicitly look for the bottleneck: *"The bottleneck here is the repeated linear scan inside the loop — that's what I'd want to eliminate."* This shows a real optimization process and is a far better outcome than freezing in silence.

### Handling "Can you do better?"

Don't just say "yes" or "no" — respond with a specific complexity target and a direction: *"I believe we can get this to O(n) by trading space for time — let me think through whether a hashmap lookup replaces the nested loop here."* This shows you understand what "better" means concretely (the actual complexity class), not just that you're willing to keep trying.

### Testing strategy

1. Trace through your original example by hand, narrating as you go.
2. Test the edge cases you identified during clarification (empty input, single element, all duplicates, negative numbers).
3. If you find a bug, narrate the fix process calmly: *"That's not handling the empty array case — let me add a guard clause for that."* Finding and fixing a small bug yourself during testing is a positive signal, not a negative one — it shows real verification, not assumed correctness.

### Communication while coding

**Narrate:** your overall approach before typing, any non-obvious decisions ("I'm using a deque here instead of a list because I need O(1) pops from both ends"), and what you're about to test before testing it.

**Silence is okay for:** short stretches of straightforward implementation (writing a loop you've already described), brief thinking pauses before a genuinely hard sub-decision — a few seconds of "let me think" is fine and even expected; constant narration of every keystroke is exhausting to listen to and signals nervousness more than clarity.
