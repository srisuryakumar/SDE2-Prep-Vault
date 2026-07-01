---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 4 — Stacks and Queues"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, min-stack, stack]
---

# Min Stack Pattern

## Intuition
Design a stack supporting `push`, `pop`, `top`, and `getMin` — all in $O(1)$.

If you track the minimum in a single variable, popping the current minimum off the stack leaves you with no way to know what the *previous* minimum was in $O(1)$ time.

**The Solution:** Maintain a second stack (`minStack`) in parallel.
Every time you push a value $v$ onto the main stack, push $\min(v, \text{current minimum})$ onto the `minStack`. 
The `minStack` remembers what the minimum *was* at every historical point in time. Popping both stacks in lockstep ensures the `minStack` always reflects the minimum of whatever remains on the main stack.

## Implementation
```java
class MinStack {
    private Deque<Integer> stack = new ArrayDeque<>();
    private Deque<Integer> minStack = new ArrayDeque<>();

    public void push(int val) {
        stack.push(val);
        minStack.push(minStack.isEmpty() ? val : Math.min(val, minStack.peek()));
    }

    public void pop() {
        stack.pop();
        minStack.pop();
    }

    public int top() { return stack.peek(); }
    public int getMin() { return minStack.peek(); }
}
```
**Complexity:** $O(1)$ time for all operations. $O(n)$ space for the extra stack.
