# Chapter 1: Algorithmic Thinking and Complexity Analysis

*Every chapter after this one hands you a new tool: two pointers, sliding windows, heaps, dynamic programming. This chapter gives you the one skill that decides which tool to reach for and proves it's the right one — the ability to predict how a piece of code will behave before you run it.*

## 1.1 What Is an Algorithm?

An **algorithm** is a finite, ordered sequence of unambiguous instructions that transforms an input into an output and is guaranteed to stop.

Three words carry all the weight:

- **Finite** — it terminates. "Keep checking" is not a step; "check up to 100 times" is.
- **Ordered** — the steps happen in a defined sequence, including defined branches and loops. Swap step 2 and step 3 and you may get a different (or wrong) answer.
- **Unambiguous** — each instruction means exactly one thing to whatever executes it. A computer has no judgment to fall back on, so "sort of in order" is not an instruction; "swap adjacent elements if the left one is bigger" is.

"Find the largest number in this list" is a *problem*. The recipe that solves it is the *algorithm*:

```
1. Set max = first element.
2. For every remaining element e:
       if e > max: max = e
3. Return max.
```

This looks trivial, and it is — deliberately. The entire discipline of algorithm design is what happens when the problem stops being trivial: when "largest number" becomes "shortest path," "longest increasing subsequence," or "minimum number of coins." The recipe gets harder to find, but it never stops being a finite, ordered, unambiguous sequence of steps. That's the lens this whole book uses.

## 1.2 Why Complexity Analysis Exists

Here's the sentence that should be tattooed on the inside of your eyelids before any technical interview:

> A solution that is correct on the sample input but takes 40 minutes on the real input is not a solution. It's a wrong answer that happens to look right in small print.

Suppose you write a function that checks every pair of elements in an array to see if any two sum to a target value:

```java
public boolean hasPairWithSum(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        for (int j = i + 1; j < arr.length; j++) {
            if (arr[i] + arr[j] == target) return true;
        }
    }
    return false;
}
```

For an array of 100 elements, this checks roughly 100×100/2 = 5,000 pairs. On any modern machine that finishes before you can blink — call it instant.

Now run the same function on an array of 1,000,000 elements. The number of pairs is roughly 1,000,000 × 1,000,000 / 2 = 500,000,000,000 — five hundred billion. At a (generous) billion basic operations per second, that's about 500 seconds — over eight minutes — for one call. A LeetCode judge times out at 1–2 seconds. An interviewer will stop you well before that.

The code didn't get less *correct* when the input grew. It got less *useful*. Complexity analysis is the discipline of predicting that gap **before** you've burned ten minutes coding the version that times out.

## 1.3 Time Complexity: Counting Operations, Not Seconds

Wall-clock time depends on things that have nothing to do with your algorithm: CPU speed, language, JIT warmup, whether someone else's cron job is hogging the machine. None of that is the algorithm's fault, and none of it is a fair basis for comparison.

So instead of seconds, we count **elementary operations** — comparisons, assignments, arithmetic — as a function of input size, conventionally called **n**. We don't care that one comparison takes 0.3 nanoseconds on your laptop. We care that the *number* of comparisons grows linearly, quadratically, or exponentially as n grows. That growth rate is what survives the move from your laptop to the interviewer's judge to a production server handling real traffic.

## 1.4 Big-O Notation

**Formal definition.** We say f(n) = O(g(n)) if there exist positive constants *c* and *n₀* such that:

```
f(n) ≤ c · g(n)    for all n ≥ n₀
```

In plain language: past some starting point, f(n) never grows faster than a constant multiple of g(n). Big-O is an **upper bound** on growth rate — it says "no worse than this," not "exactly this."

**A worked check.** Take f(n) = 3n + 5. Claim: f(n) = O(n).
Pick c = 4. We need 3n + 5 ≤ 4n, which simplifies to 5 ≤ n. So for n₀ = 5 and c = 4, the inequality holds for every n ≥ 5 (check n = 5: 20 ≤ 20 ✓; n = 6: 23 ≤ 24 ✓). The constant 5 and the coefficient 3 stop mattering once n is large enough — only the *n* matters. That's the entire point of Big-O: it strips away the details that depend on your machine and keeps only the shape of the growth.

**Practical meaning.** When someone says "this is O(n²)," they mean: if you double the input size, expect roughly four times the work. If you 10x the input, expect roughly 100x the work. Big-O tells you how pain scales, not how much pain there is right now.

*(Two cousins worth knowing, even though this book uses Big-O almost exclusively: Big-Ω (Omega) is a **lower bound** — "at least this slow" — and Big-Θ (Theta) is a **tight bound** — "exactly this rate, both upper and lower." Interviews default to Big-O because they care about the worst case you're promising, not the best case you might get lucky with.)*

## 1.5 Deriving Complexity Directly From Code

This is the skill you'll use forty times a day in an interview: look at code, output a complexity, in seconds, without hesitation.

### 1.5.1 Single Loop → O(n)

```java
public int sum(int[] arr) {
    int total = 0;
    for (int i = 0; i < arr.length; i++) {   // runs n times
        total += arr[i];                      // O(1) work each time
    }
    return total;
}
```

n iterations × O(1) work per iteration = **O(n)**. This is the baseline every other shape gets compared to.

### 1.5.2 Nested Loops → O(n²) — and Why "Nested" Isn't Automatically Quadratic

The naive rule "nested loop = O(n²)" is true *only when the inner loop's range scales with n*. Three variations, three different answers:

```java
// (A) Inner loop bound = n → classic O(n²)
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        // O(1) work
```
n × n = **O(n²)**. No surprises.

```java
// (B) Inner loop shrinks each time → STILL O(n²)
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        // O(1) work
```
Total iterations = (n−1) + (n−2) + ... + 1 + 0 = n(n−1)/2. Drop the constant and the lower-order term, and n(n−1)/2 is **still O(n²)**. This is the trap: the inner loop visibly does *less* work each pass, and people's gut says "that must bring it down a tier." It doesn't — a triangular number is a quadratic in disguise.

```java
// (C) Inner loop bound is a CONSTANT, not n → O(n)
for (int i = 0; i < n; i++)
    for (int j = i; j < Math.min(i + 3, n); j++)   // at most 3 iterations, always
        // O(1) work
```
The inner loop never does more than 3 iterations regardless of how big n gets. Total work ≤ 3n = **O(n)**. Nesting loops is not what creates O(n²) — what creates O(n²) is the inner loop's iteration count scaling with n. Always ask "does the inner bound depend on n?" before declaring quadratic.

### 1.5.3 Halving Each Step → O(log n)

```java
public int binarySearch(int[] sorted, int target) {
    int lo = 0, hi = sorted.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (sorted[mid] == target) return mid;
        if (sorted[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

Each iteration throws away half the remaining search space. Starting from n elements, how many halvings until you're down to 1?

```
n → n/2 → n/4 → n/8 → ... → 1
```

That's exactly log₂(n) steps, by definition of logarithm. For n = 1,000,000, that's about 20 steps — you can search a million-element sorted array in about 20 comparisons. This is the single most dramatic complexity improvement you'll see in this book, and it's why "is the data sorted?" is one of the first questions a strong candidate asks.

### 1.5.4 Branching Recursion → O(2ⁿ)

```java
public int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);   // two recursive calls per call
}
```

Draw the call tree for fib(4):

```
                         fib(4)
                        /      \
                  fib(3)        fib(2)
                 /      \       /      \
            fib(2)   fib(1)  fib(1)   fib(0)
            /    \
        fib(1)  fib(0)
```

Every call (except the base cases at the bottom) spawns two more calls. A tree where every node has 2 children and the depth is n has roughly 2ⁿ nodes — each node is one unit of work, so the total work is **O(2ⁿ)**. This is what "overlapping subproblems, recomputed from scratch" looks like, and it's the single justification for every memoization and DP technique in Chapter 10: cache fib(2) the first time you compute it, and that entire repeated subtree collapses to one lookup.

*(Precision note for when an interviewer pushes back: the loose-but-correct upper bound is O(2ⁿ), since each call branches in two. The *tight* bound is actually O(φⁿ) where φ ≈ 1.618 is the golden ratio — slightly better than 2ⁿ, because one branch of the tree is always one level shallower than the other. Say O(2ⁿ) with confidence; mention φⁿ if asked to be exact.)*

### 1.5.5 Sort Then Scan → O(n log n)

```java
public boolean hasPairWithSum(int[] arr, int target) {
    Arrays.sort(arr);                       // O(n log n)
    int lo = 0, hi = arr.length - 1;
    while (lo < hi) {                       // O(n)
        int sum = arr[lo] + arr[hi];
        if (sum == target) return true;
        else if (sum < target) lo++;
        else hi--;
    }
    return false;
}
```

Sorting costs O(n log n); the two-pointer scan after it costs O(n). When you add two different complexities, the **larger one wins** — O(n log n) + O(n) = O(n log n). "Sort first" is a recurring shortcut throughout this book precisely because it converts an unordered mess into something two pointers, greedy logic, or binary search can exploit, at a fixed, predictable O(n log n) entry fee.

## 1.6 The Complexity Hierarchy, Made Concrete

```
O(1)  <  O(log n)  <  O(n)  <  O(n log n)  <  O(n²)  <  O(2ⁿ)  <  O(n!)
```

| Complexity | Real example |
|---|---|
| O(1) | Array index access, HashMap get/put (average case) |
| O(log n) | Binary search, balanced BST search |
| O(n) | Linear scan, single pass with a HashMap |
| O(n log n) | Merge sort, heap sort, "sort then scan" |
| O(n²) | Bubble sort, nested pair comparison |
| O(2ⁿ) | Generating every subset, naive recursive Fibonacci |
| O(n!) | Generating every permutation |

Numbers make the gap impossible to un-see:

| n | O(log n) | O(n) | O(n log n) | O(n²) | O(2ⁿ) | O(n!) |
|---|---|---|---|---|---|---|
| 10 | 3 | 10 | 33 | 100 | 1,024 | 3,628,800 |
| 100 | 7 | 100 | 664 | 10,000 | ~1.3 × 10³⁰ | ~9.3 × 10¹⁵⁷ |
| 1,000 | 10 | 1,000 | 9,966 | 1,000,000 | astronomical | astronomical |
| 1,000,000 | 20 | 1,000,000 | ~19,930,000 | 10¹² | incomputable | incomputable |

Two things to notice and never forget: O(n²) is *fine* up to roughly n = 10,000–100,000 and *dead* by n = 1,000,000 (10¹² operations ≈ hours). O(2ⁿ) is dead by n ≈ 25–30, full stop, regardless of hardware — this is why "can we do better than checking every subset" stops being optional once n gets anywhere near three digits.

## 1.7 Amortized Analysis: Why `ArrayList.add()` Is O(1)

This is the concept that trips people up most, because it sounds like a contradiction: individual calls to `add()` can cost O(n), and yet we confidently say `add()` is O(1). Both are true; they're answers to different questions.

**The mechanism.** A Java array has a fixed size once allocated. `ArrayList` is backed by an array, so when that array fills up, `ArrayList` must allocate a *new*, bigger array and copy every existing element into it before the new element can be added.

```
Capacity 1:  [A]
insert B → full! allocate capacity 2, copy 1 element
Capacity 2:  [A][B]
insert C → full! allocate capacity 4, copy 2 elements
Capacity 4:  [A][B][C][_]
insert D
Capacity 4:  [A][B][C][D]
insert E → full! allocate capacity 8, copy 4 elements
Capacity 8:  [A][B][C][D][E][_][_][_]
```

That copy step is O(current size) — genuinely linear, genuinely slow, on the call that triggers it. Look at any single resize in isolation and "O(1) amortized" looks like a lie.

**The aggregate argument.** Look at the *total* cost across many inserts instead of one. With capacity doubling, resizes happen when size hits 1, 2, 4, 8, 16, ..., and the copy cost at each resize equals the array's size at that moment. Summed across all resizes up to n elements:

```
1 + 2 + 4 + 8 + ... + n/2   <   2n      (a geometric series, bounded by twice its largest term)
```

So across n insertions, you pay O(n) for the n insert operations themselves (each O(1) on its own), plus less than O(2n) total for every copy ever performed by every resize combined. Total work for n inserts: O(n) + O(n) = O(n). Divide that total by n insertions, and the average cost per insertion is O(n)/n = **O(1)**.

That's amortized analysis: not "every operation is fast," but "the expensive operations are so rare, and shrink so fast in relative frequency, that the *average* cost converges to a constant." A few O(n) outliers, diluted across a sea of O(1) operations, average out to O(1).

*(Accuracy note: real Java doesn't double. OpenJDK's `ArrayList` grows by 1.5×: `newCapacity = oldCapacity + (oldCapacity >> 1)`. The doubling model above is the standard textbook simplification because the arithmetic is cleaner — but the conclusion is identical either way. Any fixed growth *factor* greater than 1 produces the same geometric-series argument and the same O(1) amortized result; only the constant changes, never the complexity class. If you grew the array by a fixed *amount* instead — say, +10 every time — the math falls apart and you get O(n) amortized per insert, which is exactly why no real dynamic array implementation does that.)*

## 1.8 Space Complexity

Space complexity asks the same question time complexity does — "how does this scale with n?" — but for memory instead of operations.

- **Auxiliary space**: extra memory your algorithm allocates, *not counting the input itself*. This is almost always what an interviewer means by "space complexity."
- **Total space**: auxiliary space + the input. Rarely the number anyone wants, since you didn't choose to allocate the input.

The most commonly forgotten contributor to auxiliary space: **the call stack**. A recursive function that recurses to depth d uses O(d) space for stack frames, even if it never explicitly allocates a single array or object.

```java
public int depth(TreeNode node) {
    if (node == null) return 0;
    return 1 + Math.max(depth(node.left), depth(node.right));
}
```

No array, no list, nothing that looks like "extra memory" — and yet this is O(h) space, where h is the tree's height, because each recursive call sits on the stack until its children return. For a balanced tree, h = O(log n); for a degenerate tree that's really a linked list in disguise, h = O(n). State this explicitly. It's a favorite "wait, are you sure this is O(1) space?" trap.

## 1.9 The Big-O Simplification Rules

1. **Drop constants.** O(3n) and O(n) are the same complexity class — only the curve's *shape* matters, not the multiplier. Looping over an array three times in sequence is still O(n), not O(3n).
2. **Drop non-dominant terms.** O(n² + n) simplifies to O(n²), because as n grows, the n² term swamps the n term into irrelevance. Same logic applies to O(n + log n) → O(n): the log n term is dwarfed. (Common mistake: dropping the *wrong* one — O(n² + n) is not O(n).)
3. **Different inputs get different variables.** If a function takes two independent inputs — two strings of length n and m, two arrays of different sizes — don't collapse them into one variable. A function that loops over the first input and then the second is O(n + m), not O(n). A function with nested loops, one over each input, is O(n × m), not O(n²). Using a single n when you actually have two independent sizes is one of the most common complexity-statement errors in interviews.

## 1.10 The Interview Rule: Always State Time *and* Space

Before moving on to the next part of a solution — and definitely before declaring you're "done" — say both complexities out loud, even if no one asked. "This is O(n) time, O(1) space" is a complete sentence that does three things at once: it proves you analyzed your own solution instead of just typing until it compiled, it gives the interviewer an opening to immediately tell you if they wanted better, and it catches your own mistakes — the act of justifying a complexity claim out loud is often the moment you notice the nested loop you didn't mean to write.

## Common Mistakes

- **Calling every nested loop O(n²).** Check whether the inner loop's bound actually depends on n (Section 1.5.2, case C). It might not.
- **Calling a shrinking inner loop O(n) or O(n log n).** A triangular sum is still quadratic (Section 1.5.2, case B). "Gets smaller each time" is not the same as "doesn't sum to n²."
- **Forgetting the recursion stack as space.** A recursive solution with no explicit data structure can still be O(n) space, not O(1).
- **Confusing amortized O(1) with worst-case O(1).** "ArrayList.add() is O(1)" is an amortized claim. The specific call that triggers a resize is O(n). Both statements are correct; know which one you're making.
- **Dropping the dominant term instead of the non-dominant one.** O(n² + n) → O(n²), never O(n).
- **Using one variable for two different input sizes.** Two strings, two arrays, two anything — if their sizes can differ, call them n and m, not n and n twice.

## Pattern Recognition Guide — When This Chapter Is the Whole Battle

You're explicitly back in "just analyze the complexity" mode, rather than pattern-matching mode, when:

- You're choosing between two different approaches to the same problem and need to justify the choice with numbers, not vibes.
- An interviewer asks "does this scale to a million records" — translate their input size into n and re-derive, don't guess.
- You catch yourself saying "it's basically O(n)" about something with a loop inside a loop. Stop and actually count what the inner bound depends on.
- You've written a recursive solution and aren't sure if you've introduced exponential blowup. Draw the call tree for n = 4 or 5 by hand and count the nodes.
- You've just finished a brute-force solution and need to name *exactly* where the inefficiency lives before you can fix it. This is the move every pattern in this book exists to make: take something O(n²) or O(2ⁿ) and use a smarter data structure or a smarter traversal order to bring it down a tier.

## Chapter Summary

- An algorithm is finite, ordered, unambiguous — and complexity analysis is how you predict its behavior before you run it.
- Big-O is an upper bound on growth rate: f(n) = O(g(n)) means f(n) ≤ c·g(n) past some n₀. It describes *how pain scales*, not how much pain exists right now.
- Read complexity directly off code: count loop iterations, check whether inner bounds depend on n, draw recursion trees for branching calls, remember sort costs O(n log n) up front.
- The hierarchy O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!) isn't academic — O(n²) dies around a million elements, O(2ⁿ) dies around thirty.
- Amortized analysis answers "what's the average cost over many operations," not "what's the cost of this one operation." `ArrayList.add()` is the canonical example: rare O(n) resizes, diluted across many O(1) inserts, average to O(1).
- Space complexity counts auxiliary memory, including the call stack — a fact many candidates forget when their "O(1) space" recursive solution is actually O(n).
- State time and space out loud, every time, before moving on. It's not a formality — it's how you catch your own mistakes.
