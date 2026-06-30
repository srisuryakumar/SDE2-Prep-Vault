# Chapter 7: Heaps and Priority Queues

*A heap makes one promise — instant access to the current best or worst element of a changing collection — and breaks every other expectation you might have about "sorted" structures. This chapter is about using that one promise precisely, and not assuming more than it actually gives you.*

## 7.1 Binary Heap Structure

A binary heap is a complete binary tree (Chapter 6's definition: every level full except possibly the last, filled left to right) stored in a plain array — no left/right/parent pointers needed at all, because the tree's shape is implicit in array index arithmetic.

```
Tree:                          Array:
        1                      index:  0  1  2  3  4  5  6
      /   \                    value: [1, 3, 5, 7, 9, 8, 6]
     3     5
    / \   / \
   7   9 8   6
```

For any element at index `i`:

```
parent(i)     = (i - 1) / 2
leftChild(i)  = 2*i + 1
rightChild(i) = 2*i + 2
```

Check it against the diagram: index 2 (value 5) → `parent(2) = 0` (value 1) ✓; `leftChild(2) = 5` (value 8) ✓; `rightChild(2) = 6` (value 6) ✓. Because the tree is complete — no gaps — filling an array left to right, level by level, wastes no slots and needs no pointers. That's also why heaps are unusually cache-friendly compared to pointer-based trees.

## 7.2 Min-Heap vs. Max-Heap

- **Min-heap:** every parent ≤ both its children. Consequence: the root is *always* the minimum element in the entire heap.
- **Max-heap:** every parent ≥ both its children. Root is always the maximum.

**The misconception to kill immediately: a heap is not a sorted structure.** Only each parent's relationship to its *immediate* children is guaranteed — there's no guarantee about ordering between two siblings' subtrees, or between a grandparent and grandchild beyond what transitivity happens to give you. The *only* strong guarantee is "the root holds the min (or max)." That weaker guarantee is exactly what makes insert and extract O(log n) — a fully sorted structure would need O(n log n) total work to stay sorted after every single insertion.

## 7.3 Heapify Up (Insert) — O(log n)

**Intuition.** Place the new value at the very next open array slot — this automatically preserves the complete-tree shape, since that slot is exactly where the next node belongs in left-to-right, level-by-level order. The new element might now violate the heap property relative to its parent, so "bubble up": repeatedly swap with the parent as long as the heap property is violated (for a min-heap: as long as the child is smaller than its parent), until it reaches the root or finds a parent it's no longer smaller than.

```java
private void heapifyUp(int[] heap, int index) {
    while (index > 0) {
        int parent = (index - 1) / 2;
        if (heap[index] >= heap[parent]) break;   // heap property restored
        swap(heap, index, parent);
        index = parent;
    }
}
```

**Trace** — insert `2` into the min-heap `[1, 3, 5, 7, 9, 8, 6]`. After appending: `[1, 3, 5, 7, 9, 8, 6, 2]`, new element at index 7.

```
index=7 (val=2): parent=(7-1)/2=3 (val=7).  2>=7? No → swap.  [1,3,5,2,9,8,6,7]   index=3
index=3 (val=2): parent=(3-1)/2=1 (val=3).  2>=3? No → swap.  [1,2,5,3,9,8,6,7]   index=1
index=1 (val=2): parent=(1-1)/2=0 (val=1).  2>=1? YES → stop.

Final: [1,2,5,3,9,8,6,7]
Verify: index0(1)≤{2,5}✓  index1(2)≤{3,9}✓  index2(5)≤{8,6}✓  index3(3)≤{7}✓   valid min-heap.
```

**Complexity:** O(log n) — at most height-many swaps, and a complete tree's height is O(log n).

## 7.4 Heapify Down (Extract) — O(log n)

**Intuition.** Extracting the root leaves a hole at index 0. Shifting everything would be O(n), so instead: move the **last** array element into the root's position (this is exactly how a complete tree correctly shrinks by one node), then "bubble down" — repeatedly swap with whichever child is smaller, as long as that child is smaller than the current node, until the heap property holds again or the node becomes a leaf.

```java
private void heapifyDown(int[] heap, int size, int index) {
    while (true) {
        int left = 2 * index + 1;
        int right = 2 * index + 2;
        int smallest = index;

        if (left < size && heap[left] < heap[smallest]) smallest = left;
        if (right < size && heap[right] < heap[smallest]) smallest = right;

        if (smallest == index) break;   // heap property restored
        swap(heap, index, smallest);
        index = smallest;
    }
}
```

**Trace** — extract-min from `[1,2,5,3,9,8,6,7]` (the result of the previous insert). Save `1` as the return value. Move the last element (`7`, index 7) to index 0, shrink size to 7: `[7,2,5,3,9,8,6]`.

```
index=0 (val=7): left=1(val=2), right=2(val=5). smallest starts at 0.
                 2<7 → smallest=1.  5<2? No → smallest stays 1.
                 swap(0,1).  [2,7,5,3,9,8,6]   index=1

index=1 (val=7): left=3(val=3), right=4(val=9). smallest starts at 1.
                 3<7 → smallest=3.  9<3? No → smallest stays 3.
                 swap(1,3).  [2,3,5,7,9,8,6]   index=3

index=3 (val=7): left=7 (out of range, size=7), right=8 (out of range) → smallest stays 3 → stop.

Final: [2,3,5,7,9,8,6].   Returned min value: 1.
Verify: index0(2)≤{3,5}✓  index1(3)≤{7,9}✓  index2(5)≤{8,6}✓   valid min-heap.
```

**Complexity:** O(log n).

## 7.5 Java `PriorityQueue`

```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();                            // min-heap (default)
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());    // max-heap

minHeap.offer(5);
minHeap.offer(2);
minHeap.offer(8);
minHeap.poll();    // removes and returns 2 (the smallest)
minHeap.peek();    // returns 5, doesn't remove it
```

`PriorityQueue` is backed by exactly the array-based binary heap just described: `offer` is heapify-up, `poll` is heapify-down — both O(log n); `peek` is O(1).

**The gotcha that catches people:** `PriorityQueue` is **not** a sorted list. Iterating it directly (a for-each loop, `toString()`) does *not* produce sorted order. Only repeated `poll()` calls guarantee sorted output, because each `poll()` triggers a fresh heapify-down that re-establishes "the new root is the new minimum" one extraction at a time. Need the full contents sorted? Poll everything into a list, or sort directly instead.

---

## Pattern — Top-K Elements

### Intuition

Finding the k largest elements among n total doesn't require fully sorting everything (O(n log n)) — only tracking the best k candidates seen so far. Maintain a **min-heap of size k**: while the heap has fewer than k elements, just add. Once it reaches size k, compare each new element against the heap's root — the *weakest* of your current top-k candidates. If the new element beats it, evict the root and insert the new one; otherwise discard the new element, it's not in the top k.

**Why a min-heap, specifically, for the k *largest*.** You need O(1) access to the *smallest* of your current top-k candidates, because that's the one question that matters on every new arrival: "does this beat my weakest current member?" A min-heap puts exactly that weakest member at the root. (Finding the k *smallest* flips this: use a max-heap, so the *largest* of your current bottom-k sits at the root for comparison.)

### Template

```java
public int[] topKLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) {
            minHeap.poll();   // evict the current weakest — not in the top k
        }
    }
    return minHeap.stream().mapToInt(Integer::intValue).toArray();
}
```

Every element triggers at most one O(log k) heap operation (the heap never sits above size k+1 for more than an instant), giving **O(n log k)** total — versus O(n log n) for sorting everything. When k is small relative to n, that's a real win.

---

### Problem — Kth Largest Element in an Array (LeetCode 215)

**Statement.** Find the kth largest element in an unsorted array.

**Approach.** Direct application: a min-heap of size k. Once every element is processed, the heap's root — its minimum — is exactly the kth largest overall, because it's the weakest member of "the k largest values seen."

**Trace** on `nums = [3,2,1,5,6,4]`, `k = 2`:

```
offer(3): heap=[3]                       size 1 ≤ 2, no eviction
offer(2): heap=[2,3]                     size 2 ≤ 2, no eviction
offer(1): heap=[1,2,3] → evict 1         heap=[2,3]
offer(5): heap=[2,3,5] → evict 2         heap=[3,5]
offer(6): heap=[3,5,6] → evict 3         heap=[5,6]
offer(4): heap=[4,5,6] → evict 4         heap=[5,6]

Final root = 5.  (sorted desc: 6,5,4,3,2,1 → 2nd largest is 5)   ✓
```

**Full Solution:**

```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) {
            minHeap.poll();
        }
    }
    return minHeap.peek();
}
```

**Complexity:** Time O(n log k). Space O(k).

**Worth knowing as an alternative:** **QuickSelect** (the same partitioning idea behind quicksort) solves this in O(n) *average* case, O(n²) worst case, with O(1) extra space — better average complexity than the heap, at the cost of a worse worst case and a trickier implementation. This chapter focuses on the heap because it generalizes cleanly to streaming input and to the variants below; mention QuickSelect if asked "can you beat O(n log k)."

---

### Problem — K Closest Points to Origin (LeetCode 973)

**Statement.** Given points `[x, y]`, return the k points closest to the origin.

**Approach.** The identical Top-K template — only the comparator changes: compare squared Euclidean distance (`x² + y²`, no need for the square root, since it's monotonic and only relative order matters).

```java
public int[][] kClosest(int[][] points, int k) {
    PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
        (a, b) -> (b[0]*b[0] + b[1]*b[1]) - (a[0]*a[0] + a[1]*a[1])   // farthest sits on top
    );
    for (int[] point : points) {
        maxHeap.offer(point);
        if (maxHeap.size() > k) {
            maxHeap.poll();   // evict the current FARTHEST — not in the k closest
        }
    }
    return maxHeap.toArray(new int[0][]);
}
```

**Note the flip:** "closest" means "smallest distance," so per the rule above this needs the *farthest* of the current candidates at the root for eviction — a **max-heap**, not a min-heap.

**Complexity:** Time O(n log k). Space O(k).

---

### Problem — Top K Frequent Elements, Revisited (LeetCode 347)

This problem already has a complete O(n) bucket-sort solution in **Chapter 5**. It belongs here too, because it's the textbook proof that "K Most Frequent" is the same Top-K template as K Closest — frequency as the comparator instead of distance:

```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) freq.merge(num, 1, Integer::sum);

    PriorityQueue<Integer> minHeap = new PriorityQueue<>(
        (a, b) -> freq.get(a) - freq.get(b)   // lowest frequency on top
    );
    for (int num : freq.keySet()) {
        minHeap.offer(num);
        if (minHeap.size() > k) {
            minHeap.poll();   // evict the least frequent of the current top-k
        }
    }
    return minHeap.stream().mapToInt(Integer::intValue).toArray();
}
```

**Complexity:** O(n log k) — strictly worse than Chapter 5's O(n) bucket sort. **So why bother showing it?** Because bucket sort's O(n) only works *because this specific problem* bounds frequency between 1 and n — a constraint that won't hold for every "top-k by some score" problem. The heap version is the general-purpose tool: identical code structure whether the comparator is frequency, distance, or anything else, bounded or not. Reach for bucket sort when the value range is conveniently bounded; reach for the heap otherwise.

---

## A Note on Heaps of Objects — Merge K Sorted Lists, Revisited

Every example so far has compared simple values. Nothing stops a heap from holding entire **objects** with a custom comparator — which is exactly what Chapter 3's **Merge K Sorted Lists** did: a `PriorityQueue<ListNode>` ordered by `node.val`, holding one "current front" node from each of the k input lists. It's worth recalling that problem right now for one reason: it's the cleanest proof in this book that a heap doesn't care *what* it holds, only that you've given it a comparator that decides ordering. Full implementation and trace are in Chapter 3, Pattern 5 — nothing about the algorithm changes when revisited through this chapter's lens; only the realization that "heap of objects, not just numbers" is itself a reusable idea, independent of any one problem.

---

## Problem — Task Scheduler (LeetCode 621): Greedy Scheduling with a Max-Heap

**Statement.** Given tasks (as characters) and a cooldown `n` (a task can't repeat until `n` other slots have passed since its last run), find the minimum total time to run them all, idling where necessary.

**Approach.** A different flavor of heap usage: not "track the best k," but **greedy simulation** — at every time slot, run the most frequent *currently available* task. A max-heap of task frequencies gives O(1) access to "which available task should run next." A separate cooldown queue holds `(remaining count, time it becomes available again)` for tasks that are resting, re-admitting them to the heap once their cooldown expires.

```java
public int leastInterval(char[] tasks, int n) {
    Map<Character, Integer> freq = new HashMap<>();
    for (char task : tasks) freq.merge(task, 1, Integer::sum);

    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    maxHeap.addAll(freq.values());

    Queue<int[]> cooldown = new ArrayDeque<>();   // [remainingCount, timeAvailableAgain]
    int time = 0;

    while (!maxHeap.isEmpty() || !cooldown.isEmpty()) {
        time++;
        if (!maxHeap.isEmpty()) {
            int count = maxHeap.poll() - 1;             // run the most frequent available task
            if (count > 0) {
                cooldown.offer(new int[]{count, time + n});
            }
        }
        // Re-admit EVERY task whose cooldown expires exactly now — must be a `while`,
        // not an `if`, in case more than one task becomes available on the same tick
        while (!cooldown.isEmpty() && cooldown.peek()[1] == time) {
            maxHeap.offer(cooldown.poll()[0]);
        }
    }
    return time;
}
```

**Trace** on `tasks = [A,A,A,B,B,B]`, `n = 2`. Frequencies `{A:3, B:3}` start in the heap as `[3, 3]` — the heap never needs to track *which* task each count belongs to, since only the multiset of remaining counts determines the total time, not the labels.

| time | action | maxHeap after | cooldown after |
|---|---|---|---|
| 1 | poll 3 → count 2 → cooldown += (2,3) | `[3]` | `[(2,3)]` |
| 2 | poll 3 → count 2 → cooldown += (2,4) | `[]` | `[(2,3),(2,4)]` |
| 3 | heap empty, idle. (2,3) expires → readmit 2 | `[2]` | `[(2,4)]` |
| 4 | poll 2 → count 1 → cooldown += (1,6). (2,4) expires → readmit 2 | `[2]` | `[(1,6)]` |
| 5 | poll 2 → count 1 → cooldown += (1,7) | `[]` | `[(1,6),(1,7)]` |
| 6 | heap empty, idle. (1,6) expires → readmit 1 | `[1]` | `[(1,7)]` |
| 7 | poll 1 → count 0, no re-add to cooldown. (1,7) expires → readmit 1 | `[1]` | `[]` |
| 8 | poll 1 → count 0, no re-add. cooldown empty | `[]` | `[]` |

Both empty → loop ends. **Final time = 8** — matching the schedule `A, B, idle, A, B, idle, A, B`. ✓

**Complexity:** Time O(total tasks × log(distinct tasks)) — each task triggers at most one heap operation. Space O(distinct tasks).

**Common mistake:** using `if` instead of `while` for the cooldown re-admission check. With `if`, if two tasks' cooldowns happen to expire on the exact same tick, only one gets re-admitted that tick — and since the check is an exact equality (`== time`), the other one's expiry moment passes and it can never be re-admitted at all, breaking the algorithm. The trace above didn't happen to hit this case, but real inputs can, which is exactly why the fix matters even when a specific example doesn't expose it.

A second, easier mistake: forgetting that an **idle slot still counts toward total time**, even though no task runs during it.

---

## Pattern — Two-Heap for Streaming Median

### Intuition

Maintaining a running median as numbers arrive one at a time — with cheap insertion and cheap retrieval — needs more than a single heap can offer. One heap gives fast access to an *extreme* (min or max); the median sits in the *middle*. The fix: split everything seen so far into two halves using **two heaps**. The **lower half** lives in a **max-heap**, so its largest element — the boundary closest to the median — is O(1) accessible at the root. The **upper half** lives in a **min-heap**, so its smallest element — the other boundary — is O(1) accessible. Keep the two heaps balanced in size (never differing by more than 1).

```
All numbers seen so far, conceptually sorted:
[ ... lower half ... ] | [ ... upper half ... ]
                     ↑                   ↑
              max-heap root        min-heap root
           (largest of the lower   (smallest of the
                  half)                upper half)
```

**Reading the median, once balanced:** equal sizes → average of the two roots. Unequal by one → the root of the larger heap.

**Inserting a new number.** Compare it to the max-heap's root (the current lower-half boundary): smaller-or-equal goes to the lower half (max-heap), otherwise the upper half (min-heap). If that insertion pushes the size difference past 1, move the larger heap's root across to the other heap to restore balance.

### Problem — Find Median from Data Stream (LeetCode 295)

```java
class MedianFinder {
    private PriorityQueue<Integer> lowerHalf;   // max-heap
    private PriorityQueue<Integer> upperHalf;   // min-heap

    public MedianFinder() {
        lowerHalf = new PriorityQueue<>(Collections.reverseOrder());
        upperHalf = new PriorityQueue<>();
    }

    public void addNum(int num) {
        if (lowerHalf.isEmpty() || num <= lowerHalf.peek()) {
            lowerHalf.offer(num);
        } else {
            upperHalf.offer(num);
        }

        if (lowerHalf.size() > upperHalf.size() + 1) {
            upperHalf.offer(lowerHalf.poll());
        } else if (upperHalf.size() > lowerHalf.size() + 1) {
            lowerHalf.offer(upperHalf.poll());
        }
    }

    public double findMedian() {
        if (lowerHalf.size() == upperHalf.size()) {
            return (lowerHalf.peek() + upperHalf.peek()) / 2.0;
        }
        return lowerHalf.size() > upperHalf.size() ? lowerHalf.peek() : upperHalf.peek();
    }
}
```

**Trace**, inserting `5, 15, 1, 3` in order:

```
addNum(5):  lowerHalf empty → goes to lowerHalf.        lowerHalf=[5]    upperHalf=[]
            sizes 1 vs 0 — within balance.
findMedian(): unequal sizes → lowerHalf.peek() = 5.

addNum(15): 15 > lowerHalf.peek()=5 → goes to upperHalf. lowerHalf=[5]    upperHalf=[15]
            sizes 1 vs 1 — balanced.
findMedian(): equal sizes → (5+15)/2 = 10.0

addNum(1):  1 <= lowerHalf.peek()=5 → lowerHalf.         lowerHalf=[5,1]  upperHalf=[15]
            (max-heap root still 5)  sizes 2 vs 1 — within balance (diff=1, allowed).
findMedian(): unequal sizes → lowerHalf.peek() = 5.

addNum(3):  3 <= lowerHalf.peek()=5 → lowerHalf.         lowerHalf=[5,1,3]  upperHalf=[15]
            sizes 3 vs 1 — diff=2 > 1 → REBALANCE: move lowerHalf root (5) to upperHalf.
            lowerHalf=[3,1] (root=3)                     upperHalf=[5,15] (root=5)
            sizes now 2 vs 2 — balanced.
findMedian(): equal sizes → (3+5)/2 = 4.0

Check against the true sorted order of {5,15,1,3} = [1,3,5,15]:
median of 4 numbers = average of the two middle = (3+5)/2 = 4.0   ✓ matches.
```

**Complexity:** `addNum` is O(log n) — one heap insertion plus at most one rebalancing move, both O(log n). `findMedian` is O(1). Space O(n).

---

## Common Mistakes — Chapter-Wide

- **Using the wrong heap direction for the question being asked.** The heap holding your "current top-k candidates" needs its *weakest* member at the root for comparison/eviction — for "k largest," the weakest is the smallest, meaning a min-heap. Mixed up, you silently get the wrong k elements.
- **Assuming `PriorityQueue` iterates in sorted order.** It doesn't — only sequential `poll()` guarantees that.
- **Computing actual (square-rooted) distance in K Closest Points** instead of comparing squared distances — the square root changes nothing about the ordering and only adds floating-point overhead.
- **Using `if` instead of `while` when re-admitting from a cooldown/waiting queue** (Task Scheduler) — silently drops simultaneous expirations.
- **Forgetting that idle slots count as elapsed time** in scheduling problems.
- **Skipping the rebalance check in the streaming median**, or comparing a new number to the wrong heap's root — breaks the size invariant the entire two-heap structure depends on.
- **Reaching for two heaps when the data isn't actually streaming.** If you have the whole dataset up front and only need the median once, sorting (or QuickSelect for the middle element) is simpler and equally fast.

## Pattern Recognition Guide

- "Find the k largest/smallest/closest/most-or-least-frequent" → Top-K: min-heap of size k for largest, max-heap of size k for smallest, evicting the root whenever the heap exceeds size k.
- "Merge multiple sorted sequences" → a heap holding one "current front" element/object per sequence, with a custom comparator.
- "Continuously running median as data streams in" → two heaps, lower half as max-heap, upper half as min-heap, rebalanced to never differ by more than one element.
- "Always do the best/most-frequent available option right now, with something that temporarily disables choices" (scheduling, cooldowns) → a heap for "what's best right now," plus an auxiliary structure tracking what's temporarily unavailable.
- The chapter-wide tell: repeated access to "the current best or worst of a changing collection," where full sorting would be overkill, is a heap problem.

## Chapter Summary

- A binary heap is a complete binary tree stored as a plain array — `parent(i)=(i-1)/2`, `left(i)=2i+1`, `right(i)=2i+2` — needing no pointers at all.
- A heap guarantees only that the root is the min (or max); it is *not* a fully sorted structure.
- Insert (heapify up) and extract (heapify down) are both O(log n), bounded by the tree's height — guaranteed here by the complete-tree shape itself, the heap equivalent of Chapter 6's "height determines complexity" lesson.
- Java's `PriorityQueue` is a min-heap by default; pass `Collections.reverseOrder()` (or an equivalent comparator) for a max-heap.
- The Top-K pattern — a heap of size k, evicting the current weakest member on overflow — solves Kth Largest, K Closest Points, and Top K Frequent with the identical mechanism; only the comparator changes.
- A heap can hold entire objects with a custom comparator, not just raw numbers — Merge K Sorted Lists and Task Scheduler both lean on this.
- Two heaps, kept balanced within one element of each other, turn a continuously-streaming median into O(log n) insertion and O(1) retrieval — something no single heap can do alone, because the median lives in the middle, not at either extreme.
