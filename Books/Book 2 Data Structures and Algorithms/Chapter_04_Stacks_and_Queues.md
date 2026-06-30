# Chapter 4: Stacks and Queues

*Two of the simplest data structures in this book, and one pattern — the monotonic stack — that looks like it should be O(n²) and is secretly O(n). Understanding why is the actual point of this chapter.*

## 4.1 Stack — LIFO

A stack is Last In, First Out: the most recently added element is the first one removed. Three operations: `push` (add to top), `pop` (remove and return the top), `peek` (look at the top without removing it).

```
push(1):  [1]
push(2):  [1, 2]            ← 2 is on top
push(3):  [1, 2, 3]         ← 3 is on top
pop():    returns 3.   Stack: [1, 2]
peek():   returns 2 (the new top). Stack unchanged: [1, 2]
```

**In Java, use `ArrayDeque`, not `java.util.Stack`.** `Stack` extends `Vector`, which synchronizes every method — paying a locking cost on every single operation for thread-safety you almost never need in interview code or single-threaded applications. `ArrayDeque` is unsynchronized, backed by a resizable circular array (the same amortized-O(1) doubling logic from Chapter 1's `ArrayList` analysis, just applied at both ends of the buffer instead of one), and has been Java's officially recommended general-purpose stack implementation since Java 6.

```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);
stack.push(2);
stack.pop();     // removes and returns 2
stack.peek();    // returns 1, doesn't remove it
```

## 4.2 Queue — FIFO

A queue is First In, First Out: the element that's been waiting longest is the first one removed. Operations: `offer` (add to the back), `poll` (remove and return the front), `peek` (look at the front without removing it).

```
offer(1):  [1]
offer(2):  [1, 2]
offer(3):  [1, 2, 3]
poll():    returns 1 (the front — first one in).   Queue: [2, 3]
peek():    returns 2 (the new front). Queue unchanged: [2, 3]
```

`ArrayDeque` doubles as a queue too — it implements both the `Deque` and `Queue` interfaces, giving O(1) amortized operations at both ends.

```java
Deque<Integer> queue = new ArrayDeque<>();
queue.offer(1);
queue.offer(2);
queue.poll();     // removes and returns 1
queue.peek();     // returns 2, doesn't remove it
```

## 4.3 When to Reach for Which

**Stack** — anytime you need to remember "what came before" so you can return to it: backtracking (undo the most recent choice), expression parsing and evaluation (matching brackets, operator precedence), depth-first search using an explicit stack instead of recursion (recursion *is* a stack — the call stack — you're just managing one explicitly instead of letting the JVM do it), anything with "most recent first" semantics.

**Queue** — anytime strict arrival order matters: breadth-first search (explore nodes in the exact order they're discovered — this is what guarantees shortest paths in unweighted graphs, covered fully in Chapter 8), level-order tree traversal, task scheduling, simulating a real waiting line, anything with "first come, first served" semantics.

**The one-line test:** if undoing your most recent action would fix the problem, you want a stack. If processing things in the order they arrived is the actual requirement, you want a queue.

---

## Problem — Valid Parentheses (LeetCode 20)

**Statement.** Given a string containing only `(`, `)`, `{`, `}`, `[`, `]`, determine whether every opening bracket is closed by the matching type, in the correct order.

**Approach.** Push every opening bracket onto a stack. When a closing bracket appears, it must match whatever is currently on top of the stack — the most recently opened bracket that hasn't been closed yet. Pop and compare; mismatch (or popping an empty stack) means invalid. At the end, the stack must be completely empty — every opened bracket has to have been closed.

**Trace** on `s = "{[()]}"`:

```
'{': opening → push.            stack: [ { ]
'[': opening → push.            stack: [ {, [ ]
'(': opening → push.            stack: [ {, [, ( ]
')': closing → pop '(' .  Matches ')'. ✓          stack: [ {, [ ]
']': closing → pop '[' .  Matches ']'. ✓          stack: [ { ]
'}': closing → pop '{' .  Matches '}'. ✓          stack: [ ]
End of string. Stack empty → VALID.   ✓
```

**Full Solution:**

```java
public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    Map<Character, Character> pairs = Map.of(')', '(', ']', '[', '}', '{');

    for (char c : s.toCharArray()) {
        if (pairs.containsKey(c)) {
            // Closing bracket: must match whatever is on top
            if (stack.isEmpty() || stack.pop() != pairs.get(c)) {
                return false;
            }
        } else {
            stack.push(c);   // opening bracket
        }
    }
    return stack.isEmpty();   // every opened bracket must have been closed
}
```

**Complexity:** Time O(n). Space O(n) worst case — a string of all opening brackets pushes every character.

**Common mistake:** forgetting the final `stack.isEmpty()` check. A string like `"(()"` matches every closing bracket it actually has correctly, but leaves an unclosed `(` — without checking the stack is empty at the end, this incorrectly reports valid.

---

## Pattern — Monotonic Stack

### Intuition

A monotonic stack keeps its elements in sorted order (either increasing or decreasing, read bottom to top) by popping off anything that would violate that order the moment a new element arrives. The reason this earns its keep: **every pop is informative, not wasted work.** When element X gets popped because the new element Y broke the sorted order, Y is exactly the answer to "what's the next element (greater, or smaller, depending on direction) than X" — the question this entire pattern exists to answer.

**Why it's O(n) despite the nested loop.** A `while` loop sitting inside a `for` loop looks like it should be O(n²). It isn't: every element is pushed exactly once and popped at most once across the *entire* run. The total number of pop operations, summed over every iteration of the outer loop, can never exceed n — because you can't pop more elements than you ever pushed. The work is O(n) total, just spread unevenly across iterations.

### Decreasing Stack → "Next Greater Element" Family

Maintain the stack so that, read bottom to top, values are decreasing. When a new element is *larger* than the top, the order is broken — and the new element is precisely the "next greater element" for the one about to be popped. Pop everything smaller than the new element, recording the new element as each popped element's answer, then push the new element.

```java
// Core subroutine: next greater element for every position in a single array
public int[] nextGreaterElement(int[] arr) {
    int n = arr.length;
    int[] result = new int[n];
    Arrays.fill(result, -1);             // default: no greater element exists
    Deque<Integer> stack = new ArrayDeque<>();   // holds indices, decreasing values bottom→top

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && arr[stack.peek()] < arr[i]) {
            int idx = stack.pop();
            result[idx] = arr[i];
        }
        stack.push(i);
    }
    return result;
}
```

**Trace** on `arr = [2, 1, 2, 4, 3]` (stack shown by value for clarity — the real code stores indices):

```
i=0 (val=2): stack empty → push.                          stack: [2]
i=1 (val=1): top=2, is 2<1? No → push.                     stack: [2, 1]
i=2 (val=2): top=1, is 1<2? Yes → pop, result(for 1)=2.
             new top=2, is 2<2? No → stop. push.           stack: [2, 2]
                                                             result so far: [-1, 2, -1, -1, -1]
i=3 (val=4): top=2, is 2<4? Yes → pop, result(for that 2)=4.
             new top=2, is 2<4? Yes → pop, result(for first 2)=4.
             stack empty → stop. push.                     stack: [4]
                                                             result so far: [4, 2, 4, -1, -1]
i=4 (val=3): top=4, is 4<3? No → push.                      stack: [4, 3]

End of array. Anything still on the stack (4, 3) never found a greater element → stays -1.
Final result: [4, 2, 4, -1, -1]
```

**This subroutine is the entire engine behind the next two problems.**

### Problem — Next Greater Element I (LeetCode 496)

**Statement.** Given `nums1` (a subset of `nums2`, all values distinct), for each element of `nums1`, find its next greater element *in `nums2`*. Output -1 where none exists.

**Approach.** Run the exact subroutine above on `nums2`, but store the results in a `HashMap<value, nextGreater>` instead of an array (since we need to look results up by value, not by index, when answering for `nums1`). Then answer each query in O(1).

**Full Solution:**

```java
public int[] nextGreaterElement(int[] nums1, int[] nums2) {
    Map<Integer, Integer> nextGreaterMap = new HashMap<>();
    Deque<Integer> stack = new ArrayDeque<>();   // holds values directly, decreasing bottom→top

    for (int num : nums2) {
        while (!stack.isEmpty() && stack.peek() < num) {
            nextGreaterMap.put(stack.pop(), num);
        }
        stack.push(num);
    }
    // anything left on the stack simply has no entry in the map — lookups default to -1

    int[] result = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) {
        result[i] = nextGreaterMap.getOrDefault(nums1[i], -1);
    }
    return result;
}
```

**Complexity:** Time O(n + m), where n = `nums2.length`, m = `nums1.length`. Space O(n) for the map.

### Problem — Daily Temperatures (LeetCode 739)

**Statement.** Given daily temperatures, return `answer` where `answer[i]` is the number of days until a warmer temperature. `answer[i] = 0` if no warmer day exists.

**Approach.** This is the identical subroutine — except instead of recording the *value* that broke the order, we record the *distance* (index difference) to it. Same decreasing stack of indices, same popping condition; only what gets written into the answer changes.

**Trace** on `temperatures = [73,74,75,71,69,72,76,73]`:

```
i=0 (73): stack empty → push.                                       stack:[0]
i=1 (74): top=0(73), 73<74 → pop, answer[0]=1-0=1. stack empty→push. stack:[1]
i=2 (75): top=1(74), 74<75 → pop, answer[1]=2-1=1. stack empty→push. stack:[2]
i=3 (71): top=2(75), 75<71? No → push.                              stack:[2,3]
i=4 (69): top=3(71), 71<69? No → push.                              stack:[2,3,4]
i=5 (72): top=4(69), 69<72 → pop, answer[4]=5-4=1.
          top=3(71), 71<72 → pop, answer[3]=5-3=2.
          top=2(75), 75<72? No → stop. push.                        stack:[2,5]
i=6 (76): top=5(72), 72<76 → pop, answer[5]=6-5=1.
          top=2(75), 75<76 → pop, answer[2]=6-2=4.
          stack empty → push.                                       stack:[6]
i=7 (73): top=6(76), 76<73? No → push.                               stack:[6,7]

End. Remaining indices (6, 7) found no warmer day → answer stays 0.
Final: [1, 1, 4, 2, 1, 1, 0, 0]   ✓
```

**Full Solution:**

```java
public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    Deque<Integer> stack = new ArrayDeque<>();   // indices, decreasing temps bottom→top

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && temperatures[stack.peek()] < temperatures[i]) {
            int idx = stack.pop();
            answer[idx] = i - idx;
        }
        stack.push(i);
    }
    return answer;
}
```

**Complexity:** Time O(n) amortized — total pops across the whole run never exceed n. Space O(n) worst case (a strictly decreasing temperature sequence never gets popped, so every index stays on the stack).

---

### Increasing Stack → "Next Smaller Element" Family

Mirror the decreasing stack: maintain values increasing bottom to top. When a new element is *smaller* than the top, that's the violation — and the new element is the "next smaller element" for whatever gets popped. This sub-pattern shows up most dramatically in the hardest stack problem in the curriculum.

### Problem — Largest Rectangle in Histogram (LeetCode 84) — Hard, Full Explanation

**Statement.** Given `heights` representing histogram bar heights (each bar width 1), find the area of the largest rectangle formed by contiguous bars.

```
height
  6 |              ▓
  5 |           ▓  ▓
  4 |           ▓  ▓
  3 |           ▓  ▓        ▓
  2 |  ▓        ▓  ▓     ▓  ▓
  1 |  ▓     ▓  ▓  ▓     ▓  ▓
    +--+--+--+--+--+--+--+
idx    0  1  2  3  4  5
height: 2  1  5  6  2  3
```

**Building the intuition.** Imagine bar `i` as the *limiting height* of some rectangle — extend left and right from `i` as far as possible while every bar in that span is at least `heights[i]` tall. That rectangle's area is `heights[i] * width`, where `width` depends on the nearest bar to the left that's *shorter* than `heights[i]` (the left boundary) and the nearest bar to the right that's shorter (the right boundary). The answer is the maximum such rectangle over every `i`. Computing those two boundaries naively for every bar is O(n) per bar — O(n²) total.

**Speeding it up with a stack.** We need, for each bar, the nearest shorter bar to its left and right — exactly "next smaller element" in both directions. A single left-to-right pass with an increasing stack gets both boundaries at once: maintain a stack of indices with heights increasing bottom to top. When the current bar is *shorter* than the bar at the stack's top, the top bar has just found its **right boundary** — the current bar is the first bar to its right that's shorter than it. Pop it and compute its rectangle immediately: `height` = the popped bar's height; the new stack top (after popping) is the **left boundary**, because everything still sitting between the new top and the popped bar was taller-or-equal (that's exactly why it hasn't been popped yet — nothing shorter has appeared between them).

```
width = currentIndex - newStackTopIndex - 1     (if stack isn't empty after popping)
width = currentIndex                            (if the stack becomes completely empty —
                                                   the rectangle extends back to index 0)
```

To resolve bars that never find a shorter bar to their right within the array, append a sentinel bar of height 0 at the very end — this forces every remaining bar off the stack and resolved.

**Full Solution:**

```java
public int largestRectangleArea(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();   // indices, increasing heights bottom→top
    int maxArea = 0;
    int n = heights.length;

    for (int i = 0; i <= n; i++) {
        int currentHeight = (i == n) ? 0 : heights[i];   // sentinel flushes the stack at the end

        while (!stack.isEmpty() && heights[stack.peek()] > currentHeight) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        stack.push(i);
    }
    return maxArea;
}
```

**Trace** on `heights = [2, 1, 5, 6, 2, 3]`:

```
i=0 (h=2): stack empty → push.                                            stack:[0](h=2)
i=1 (h=1): top=0(h=2), 2>1 → pop. height=2. stack empty → width=i=1.
           area=2*1=2. maxArea=2.                push.                   stack:[1](h=1)
i=2 (h=5): top=1(h=1), 1>5? No → push.                                    stack:[1,2](h=1,5)
i=3 (h=6): top=2(h=5), 5>6? No → push.                                    stack:[1,2,3](h=1,5,6)
i=4 (h=2): top=3(h=6), 6>2 → pop. height=6. new top=2 → width=4-2-1=1.
           area=6*1=6. maxArea=6.
           top=2(h=5), 5>2 → pop. height=5. new top=1 → width=4-1-1=2.
           area=5*2=10. maxArea=10.
           top=1(h=1), 1>2? No → stop. push.                              stack:[1,4](h=1,2)
i=5 (h=3): top=4(h=2), 2>3? No → push.                                    stack:[1,4,5](h=1,2,3)
i=6 (sentinel h=0): top=5(h=3), 3>0 → pop. height=3. new top=4 → width=6-4-1=1.
                    area=3*1=3. maxArea stays 10.
                    top=4(h=2), 2>0 → pop. height=2. new top=1 → width=6-1-1=4.
                    area=2*4=8. maxArea stays 10.
                    top=1(h=1), 1>0 → pop. height=1. stack empty → width=i=6.
                    area=1*6=6. maxArea stays 10.

Final maxArea = 10   (the rectangle formed by the height-5 bar spanning indices 2–3, width 2)   ✓
```

**Complexity:** Time O(n) — same amortized argument as the decreasing stack: total pops across the entire run never exceed n+1. Space O(n).

**Common Mistakes — Largest Rectangle:**
- **Forgetting the sentinel pass.** Without flushing height 0 at the end, any bars still on the stack when the array ends never get resolved, silently undercounting the answer.
- **Off-by-one in width.** It's `i - stack.peek() - 1`, not `i - stack.peek()` — the new top is itself a boundary, excluded from the rectangle's width, not included in it.
- **Forgetting the empty-stack case.** When the stack empties out after a pop, the rectangle extends all the way back to index 0, so width = `i`, not `i - 1` or some other adjustment.

---

## Problem — Min Stack (LeetCode 155)

**Statement.** Design a stack supporting `push`, `pop`, `top`, and `getMin` — all in O(1).

**Why a single variable for "current min" fails.** If you track the minimum in one plain variable, popping the current minimum off the stack leaves you with no way to know what the *previous* minimum was, short of re-scanning everything remaining — O(n).

**Approach.** Maintain a second stack in parallel. Every time you push a value `v` onto the main stack, push `min(v, current minimum)` onto the min-stack. The min-stack at every position remembers what the minimum *was* at that point in history, so popping the main stack and popping the min-stack in lockstep always leaves the min-stack's new top equal to the minimum of whatever remains on the main stack.

```java
class MinStack {
    private Deque<Integer> stack;
    private Deque<Integer> minStack;

    public MinStack() {
        stack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
    }

    public void push(int val) {
        stack.push(val);
        minStack.push(minStack.isEmpty() ? val : Math.min(val, minStack.peek()));
    }

    public void pop() {
        stack.pop();
        minStack.pop();
    }

    public int top() {
        return stack.peek();
    }

    public int getMin() {
        return minStack.peek();
    }
}
```

**Trace:** `push(5), push(3), push(7), getMin(), pop(), getMin()`

```
push(5): stack=[5]      minStack=[5]        (5 is the min so far)
push(3): stack=[5,3]    minStack=[5,3]      (min(3,5)=3)
push(7): stack=[5,3,7]  minStack=[5,3,3]    (min(7,3)=3)
getMin(): minStack.peek() = 3   ✓
pop():    stack=[5,3]   minStack=[5,3]
getMin(): minStack.peek() = 3   ✓  (still correct — 3 is the min of the remaining [5,3])
```

**Complexity:** O(1) for every operation. Space O(n) — two parallel stacks instead of one, but still O(n), not a worse complexity class.

---

## Common Mistakes — Chapter-Wide

- **Using `java.util.Stack` instead of `ArrayDeque`.** Functionally correct, but every operation pays for synchronization you don't need.
- **Panicking that a monotonic stack's nested `while`-inside-`for` is O(n²).** It isn't — total pops across the entire run are bounded by total pushes, which is bounded by n.
- **Mixing up which direction finds what.** Decreasing stack → next *greater* element. Increasing stack → next *smaller* element. If you forget which, rederive it: you pop when the new element breaks the order, and the new element becomes the popped element's answer — so a decreasing stack (which breaks when something *bigger* shows up) is necessarily finding "next greater."
- **Skipping the sentinel flush in Largest Rectangle.** Leaves bars on the stack permanently unresolved.
- **Using one variable instead of a second stack for `getMin`.** Loses all history the moment you pop past the current minimum.

## Pattern Recognition Guide

- "Matching/nested structure" (parentheses, tags, nested expressions) → basic stack.
- "Next greater/warmer/taller element to the right" → decreasing monotonic stack.
- "Next smaller element," or "largest rectangle/area under a histogram-shaped constraint" → increasing monotonic stack.
- "O(1) access to the running min/max while still supporting push/pop" → a parallel auxiliary stack tracking that running extreme value at each push.
- "Process level by level," "shortest path in an unweighted graph," "first-come-first-served" → queue, not stack (this is the setup for Chapter 8's BFS).

## Chapter Summary

- Stack = LIFO: backtracking, undo, matching/nesting, expression parsing, explicit DFS. Queue = FIFO: BFS, level-order traversal, task scheduling.
- Use `ArrayDeque` for both in Java — unsynchronized, O(1) amortized at both ends, faster than `java.util.Stack` or `LinkedList`-backed alternatives.
- A monotonic stack maintains sorted order by popping whatever breaks it — and every pop is itself the answer (next greater/smaller) for the element that just got removed. Total work across the whole run is O(n), not O(n²), because total pops can never exceed total pushes.
- Decreasing stack → next greater element family (Next Greater Element I, Daily Temperatures).
- Increasing stack → next smaller element family (Largest Rectangle in Histogram, resolved with a sentinel flush at the end).
- Min Stack's O(1) `getMin` trick: a parallel stack that remembers the running minimum at every historical push, so popping never erases what the minimum used to be.
