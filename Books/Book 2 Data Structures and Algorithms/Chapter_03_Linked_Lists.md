# Chapter 3: Linked Lists

*Arrays gave you O(1) access but O(n) insertion. This chapter flips that trade entirely — and shows you the one technique (dummy heads) and one math proof (Floyd's cycle detection) that make linked-list code reliable instead of off-by-one minefields.*

## 3.1 Node Structure and Memory Layout

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}
```

An array element's location is computed by a formula (`base + i*size`). A linked list node's location is **wherever the garbage collector happened to put it** — nodes are scattered across memory, connected only by pointers.

```
Array (contiguous):
Address:  1000   1004   1008   1012
Value:    [10]   [20]   [30]   [40]

Linked List (scattered):
Address 7240: [10 | next → 1024]
Address 1024: [30 | next → 5096]
Address 5096: [20 | next → null]

head → 7240 → 1024 → 5096 → null
Traversal order: 10 → 30 → 20
(notice the values aren't even stored in address order — there's no formula, only following pointers)
```

There is no `address(i)` formula here. To reach the 5th node you must visit nodes 1 through 4 first, following `next` pointers one at a time. Random access is **O(n)**, not O(1). This is the fundamental trade you're making the moment you choose a linked list over an array.

## 3.2 Why Linked Lists: O(1) Insert/Delete, No Resizing

What you get in exchange for losing O(1) random access: if you already hold a reference to the node before your target position, insertion and deletion are O(1) — just rewire two pointers, nothing shifts.

```
Insert X between A and B:

Before:  A → B
              ↑
         (A.next currently points here)

After:   A → X → B

Code:  X.next = A.next;   // X → B
       A.next = X;        // A → X
```

No element moved in memory. Compare to an array, where inserting at position k requires shifting every element from k onward — O(n) — to physically open up a slot. Deletion is the mirror image: `A.next = A.next.next` unlinks B in O(1), no shifting.

Linked lists also never need the resize-and-copy dance from Chapter 1's `ArrayList` analysis — a new node is simply allocated and linked in, one at a time, with no pre-existing capacity to outgrow.

**The catch:** O(1) insert/delete only holds if you already have a reference to the right spot. Finding that spot (e.g., "delete the node with value 42") still costs O(n), because you have to walk the list to find it — there's no formula to jump straight there.

## 3.3 The Dummy Head Technique

Here's the recurring annoyance with linked lists: modifying a node's `next` pointer is uniform code, but modifying the `head` reference itself is a special case, because `head` is a variable, not a node's field.

```java
// WITHOUT a dummy head — removing nodes with value == target
if (head != null && head.val == target) {
    head = head.next;          // special case: head itself must change
}
ListNode curr = head;
while (curr != null && curr.next != null) {
    if (curr.next.val == target) {
        curr.next = curr.next.next;   // uniform case: rewire a next pointer
    } else {
        curr = curr.next;
    }
}
```

Two different code paths for the same logical operation ("remove a matching node") is exactly the kind of asymmetry that produces bugs under interview pressure. The fix: insert a fake **sentinel node** before the real head. Now the real head is always "some node's `.next`," never a bare variable — every removal becomes the uniform case.

```java
// WITH a dummy head — one uniform case, no special-casing
ListNode dummy = new ListNode(0);
dummy.next = head;
ListNode curr = dummy;
while (curr.next != null) {
    if (curr.next.val == target) {
        curr.next = curr.next.next;
    } else {
        curr = curr.next;
    }
}
return dummy.next;   // dummy.next is always the correct (possibly new) head
```

Use this any time the head of the list might need to change — removing a node, reversing, merging, partitioning. It costs one extra node and removes an entire category of edge-case bugs.

---

## Pattern 1 — Reversal (Iterative)

### Intuition

Reversing a list means every node's `next` pointer must flip to point backward. Walk through once; at each node, before moving on, redirect its `next` to point at the node you just came from. The trap: once you overwrite `curr.next`, you've lost your only way to reach the rest of the original list — so you must save "what's next" in a temporary variable *before* you overwrite anything.

Three pointers: `prev` (what curr should now point to), `curr` (the node being rewired), `next` (a temporary holder so you don't lose your place).

### Template

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    while (curr != null) {
        ListNode next = curr.next;   // save next before overwriting
        curr.next = prev;            // reverse the pointer
        prev = curr;                 // advance prev
        curr = next;                 // advance curr
    }
    return prev;   // prev ends up at the new head
}
```

### Trace on `1 → 2 → 3 → null`

```
Initial:  prev = NULL     curr = [1]→[2]→[3]→NULL

Step 1: next = [2] (saved before overwriting)
        curr.next = prev  →  [1]→NULL
        prev = [1]   curr = [2]
        State:  [1]→NULL          [2]→[3]→NULL
                 ↑prev              ↑curr

Step 2: next = [3]
        curr.next = prev  →  [2]→[1]→NULL
        prev = [2]   curr = [3]
        State:  [2]→[1]→NULL      [3]→NULL
                 ↑prev               ↑curr

Step 3: next = NULL
        curr.next = prev  →  [3]→[2]→[1]→NULL
        prev = [3]   curr = NULL → loop condition fails, stop

Return prev:  [3]→[2]→[1]→NULL   ✓
```

**Complexity:** Time O(n). Space O(1).

---

## Pattern 2 — Reversal (Recursive)

### Intuition

"Trust the recursion": assume `reverseList(head.next)` correctly reverses *everything after* `head` and hands back the new head of that reversed piece. Your job at the current level is just three things: (1) take that returned new head, (2) make the node right after `head` (which is now the **tail** of the reversed sub-list) point back to `head`, (3) make `head` point to `null` since `head` is now the new tail of the whole thing. Then pass the unchanged `newHead` back up.

### Template

```java
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) {
        return head;   // base case: 0 or 1 nodes — already "reversed"
    }
    ListNode newHead = reverseList(head.next);   // trust it reverses the rest
    head.next.next = head;   // the node right after head now points back to head
    head.next = null;        // head becomes the new tail
    return newHead;          // unchanged — passed straight up
}
```

### Trace on `1 → 2 → 3 → null` (call stack unwinding)

```
Calls go down:  reverseList(1) → reverseList(2) → reverseList(3)
At reverseList(3): head.next == null → base case → return 3.
                    List so far, untouched: 1→2→3→NULL

Returns unwind bottom-up:

Level "head=2":  newHead = 3 (from the call below)
                 head.next.next = head  →  3.next = 2        ⇒  3→2
                 head.next = null       →  2.next = null     ⇒  2 is now a tail
                 return newHead = 3
                 Current shape:  1→2     3→2→NULL

Level "head=1":  newHead = 3 (from the call below)
                 head.next.next = head  →  2.next = 1         ⇒  3→2→1
                 head.next = null       →  1.next = null      ⇒  1 is now the tail
                 return newHead = 3

Final list:  3 → 2 → 1 → NULL   ✓
```

**Complexity:** Time O(n). Space **O(n)** — this is the trap. Every recursive call sits on the call stack until the base case returns, so recursion depth equals list length. The recursive version is more elegant to write but trades O(1) space for O(n) space; say this out loud if asked, exactly as Chapter 1's interview rule demands.

### Common Mistakes — Reversal

- **Forgetting to save `next` before overwriting `curr.next`** in the iterative version. Once `curr.next` is overwritten, the rest of the original list is unreachable — permanently lost, not just temporarily.
- **Forgetting `head.next = null`** in the recursive version. After `head.next.next = head`, if you skip clearing `head.next`, the original forward pointer is still there *too* — now `head` and `head.next` point at each other, creating a 2-node cycle.

---

## Pattern 3 — Fast-Slow Pointers

### Find the Middle

**Intuition.** Move `slow` one step and `fast` two steps per iteration. By the time `fast` has traveled to the end, `slow` has covered exactly half that distance — landing it on the middle.

```java
public ListNode findMiddle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}
```

**Loop condition controls which middle you land on for even-length lists.** With the condition above (`fast != null && fast.next != null`), a 4-node list `1→2→3→4` lands `slow` on node **3** — the *second* of the two middle nodes. Swap the condition to `fast.next != null && fast.next.next != null` and the same list lands `slow` on node **2** — the *first* middle. This single-character difference matters for problems like Reorder List, where you need a specific split point. Know both, and check which one the problem needs.

### Detect a Cycle — Floyd's Algorithm, With Proof

**Intuition.** Same two speeds, `slow` and `fast`. If there's no cycle, `fast` simply reaches `null` — no cycle exists. If there *is* a cycle, claim: `fast` is guaranteed to eventually land exactly on `slow` inside the cycle.

**Why this is guaranteed, not just likely.** Once both pointers have entered the cycle, think about the gap between them — `fast`'s position minus `slow`'s position, measured in steps along the cycle, modulo the cycle length C. Each iteration, `slow` advances 1 and `fast` advances 2, so the gap grows by exactly 1 step (mod C) every iteration. A quantity that increases by exactly 1 each step, inside a space of only C possible values (0 through C−1), **cannot skip over 0** — it must land on every residue in sequence, including 0, within at most C iterations. When the gap is 0 (mod C), `fast` and `slow` are at the identical node. They are mathematically guaranteed to meet; it isn't a coincidence that toy examples happen to work.

```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            return true;
        }
    }
    return false;
}
```

**Trace** on a list `1 → 2 → 3 → 4 → 5 → (back to 3)`:

```
slow=1 fast=1
iter1: slow=2, fast=3
iter2: slow=3, fast=5
iter3: slow=4, fast: from 5, next=3, next.next=4 → fast=4.
       slow == fast == 4  →  CYCLE DETECTED, return true.
```

**Complexity:** Time O(n) — at most one extra lap around the cycle after entering it. Space O(1).

### Find the Cycle Entry Point — the Two-Pointer Reset Trick, Derived

This is the step most people memorize without understanding — here's where the trick actually comes from.

**Setup.** Let `a` = distance from `head` to the cycle's start. Let `C` = the cycle's length. Let the meeting point found by Floyd's algorithm be `b` steps into the cycle (measured from the cycle start, along the direction of travel).

When `slow` and `fast` meet:
- `slow` has traveled `a + b` total steps.
- `fast` has traveled `a + b + kC` total steps, for some non-negative integer k — it lapped the cycle k extra times before meeting `slow`.

Since `fast` always travels exactly twice the distance `slow` does in the same time:

```
a + b + kC = 2(a + b)
a + b + kC = 2a + 2b
kC = a + b
a  = kC − b
a  ≡ (C − b)   (mod C)
```

**What that equation buys you.** Place a new pointer `ptr1` at `head`. Leave `ptr2` at the meeting point. Advance both one step at a time:
- `ptr1` needs exactly `a` steps to reach the cycle's start.
- `ptr2`, already `b` steps into the cycle, needs exactly `C − b` steps to complete its lap and arrive back at the cycle's start.

Because `a ≡ (C − b) (mod C)`, and `ptr2` is moving inside a cycle (so "extra full laps" land it back in the same place), **both pointers arrive at the cycle's entry point at the same time.** That's the entire trick — it isn't a coincidence, it's a direct consequence of the algebra above.

```java
public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            ListNode ptr1 = head;
            ListNode ptr2 = slow;   // meeting point
            while (ptr1 != ptr2) {
                ptr1 = ptr1.next;
                ptr2 = ptr2.next;
            }
            return ptr1;   // cycle entry point
        }
    }
    return null;   // no cycle
}
```

**Verifying the trace** on `1 → 2 → 3 → 4 → 5 → (back to 3)`: here `a = 2` (nodes 1, 2 precede the cycle), `C = 3` (cycle is 3→4→5→3), and the meeting point found above was node 4, which is `b = 1` step into the cycle. Check the formula: `a ≡ (C − b) mod C` → `2 ≡ (3 − 1) = 2 mod 3` ✓.

```
ptr1 = head = 1,  ptr2 = meeting point = 4
iter1: ptr1 = 2,  ptr2 = 5             → not equal
iter2: ptr1 = 3,  ptr2 = 5.next = 3    → EQUAL → return 3

Cycle entry point: node 3  ✓ (matches how the example was constructed)
```

**Complexity:** Time O(n). Space O(1).

---

## Pattern 4 — Merge Two Sorted Lists

### Intuition

Build the merged list with a dummy head and a `tail` pointer that tracks where to attach the next node. At each step, compare the current heads of both input lists, attach the smaller to `tail`, and advance that list. The moment one list runs out, splice the *entire remainder* of the other list on directly — no need to keep comparing one element at a time once there's nothing left to compare against.

### Solution (LeetCode 21)

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0);
    ListNode tail = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) {
            tail.next = l1;
            l1 = l1.next;
        } else {
            tail.next = l2;
            l2 = l2.next;
        }
        tail = tail.next;
    }
    tail.next = (l1 != null) ? l1 : l2;   // attach whatever remains
    return dummy.next;
}
```

### Trace on `l1 = 1→3→5`, `l2 = 2→4→6`

```
dummy→NULL, tail=dummy
1 vs 2: 1<=2 → attach 1, l1=3, tail=1.        dummy→1
3 vs 2: 3>2  → attach 2, l2=4, tail=2.        dummy→1→2
3 vs 4: 3<=4 → attach 3, l1=5, tail=3.        dummy→1→2→3
5 vs 4: 5>4  → attach 4, l2=6, tail=4.        dummy→1→2→3→4
5 vs 6: 5<=6 → attach 5, l1=null, tail=5.     dummy→1→2→3→4→5
l1==null → loop ends.  tail.next = l2 = 6.    dummy→1→2→3→4→5→6

Return dummy.next:  1→2→3→4→5→6   ✓
```

**Complexity:** Time O(n + m). Space O(1) auxiliary.

---

## Pattern 5 — Merge K Sorted Lists

### Intuition

Generalize the two-list merge with a **min-heap** holding the current "front" node of each of the k lists. Repeatedly pop the smallest, attach it to the result, and — if that list has more nodes — push its next node back into the heap. Every one of the n total nodes across all lists is pushed and popped exactly once, and each heap operation costs O(log k), giving O(n log k) total instead of the O(nk) you'd get merging the lists two at a time, k times over.

### Solution (LeetCode 23)

```java
public ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> heap = new PriorityQueue<>((a, b) -> a.val - b.val);
    for (ListNode node : lists) {
        if (node != null) heap.offer(node);
    }

    ListNode dummy = new ListNode(0);
    ListNode tail = dummy;
    while (!heap.isEmpty()) {
        ListNode smallest = heap.poll();
        tail.next = smallest;
        tail = tail.next;
        if (smallest.next != null) {
            heap.offer(smallest.next);
        }
    }
    return dummy.next;
}
```

**Trace (abbreviated)** on `lists = [[1,4,5], [1,3,4], [2,6]]`:

```
Initial heap: {1(L1), 1(L2), 2(L3)}
poll 1(L1) → result: 1            push L1.next=4   → heap: {1(L2), 2(L3), 4(L1)}
poll 1(L2) → result: 1,1          push L2.next=3   → heap: {2(L3), 3(L2), 4(L1)}
poll 2(L3) → result: 1,1,2        push L3.next=6   → heap: {3(L2), 4(L1), 6(L3)}
poll 3(L2) → result: 1,1,2,3      push L2.next=4   → heap: {4(L1), 4(L2), 6(L3)}
poll 4(L1) → result: ...,4        push L1.next=5   → heap: {4(L2), 5(L1), 6(L3)}
poll 4(L2) → result: ...,4,4      L2 exhausted     → heap: {5(L1), 6(L3)}
poll 5(L1) → result: ...,5        L1 exhausted     → heap: {6(L3)}
poll 6(L3) → result: ...,6        heap empty, done

Final: 1,1,2,3,4,4,5,6   ✓ sorted, all elements present
```

**Complexity:** Time O(n log k), where n is the total node count and k is the number of lists. Space O(k) for the heap.

---

## Problem — Reorder List (LeetCode 143)

**Statement.** Given `L0 → L1 → ... → Ln-1 → Ln`, reorder in-place to `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...` without altering node values.

**Approach.** This problem is a deliberate combination of three patterns from this chapter, in sequence:

1. **Find the middle** (fast-slow pointers) and split the list into two halves.
2. **Reverse the second half** (reversal pattern).
3. **Merge by interleaving** — alternate one node from the first half, one from the reversed second half (not "compare and pick smaller" like Pattern 4 — just strict alternation).

```java
public void reorderList(ListNode head) {
    if (head == null || head.next == null) return;

    // Step 1: find the first middle (note the loop condition — lands on first middle)
    ListNode slow = head, fast = head;
    while (fast.next != null && fast.next.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    ListNode secondHalf = slow.next;
    slow.next = null;   // cut into two independent halves

    // Step 2: reverse the second half
    ListNode prev = null, curr = secondHalf;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    secondHalf = prev;

    // Step 3: interleave
    ListNode first = head;
    ListNode second = secondHalf;
    while (second != null) {
        ListNode firstNext = first.next;
        ListNode secondNext = second.next;
        first.next = second;
        second.next = firstNext;
        first = firstNext;
        second = secondNext;
    }
}
```

**Trace** on `1 → 2 → 3 → 4 → 5`:

```
Find first middle: slow ends at node 2.
secondHalf = slow.next = 4 (→5).  slow.next = null.
Two halves:  first = 1→2→3      second = 4→5

Reverse second half:  4→5  becomes  5→4
secondHalf = 5 (→4)

Interleave:
first=1, second=5:
  firstNext=2, secondNext=4
  1.next = 5      →  1→5
  5.next = 2      →  5→2     (so far: 1→5→2...)
  first=2, second=4

first=2, second=4:
  firstNext=3, secondNext=null (reversed half ends at 4→null)
  2.next = 4      →  2→4
  4.next = 3      →  4→3     (so far: 1→5→2→4→3)
  first=3, second=null → loop ends (second is null)

Final list: 1 → 5 → 2 → 4 → 3
Expected: L0,Ln,L1,Ln-1,L2 = 1,5,2,4,3   ✓
```

**Complexity:** Time O(n). Space O(1) auxiliary.

---

## LRU Cache (LeetCode 146) — Full Implementation

**Statement.** Design a cache with `get(key)` and `put(key, value)`, both O(1), that evicts the **least recently used** item when it exceeds a fixed capacity. Both `get` and `put` count as "using" a key — they should mark it as most recently used.

**Why a HashMap alone fails.** A HashMap gives O(1) lookup by key, but has no concept of "order of use" — finding the least-recently-used item would mean scanning everything, O(n).

**Why a linked list alone fails.** A linked list tracks order easily (move the used node to the front), but finding a specific key by value requires walking the list — O(n) — since there's no direct way to jump to an arbitrary node.

**The combination that makes both O(1):** a `HashMap<Integer, Node>` for instant lookup of *any* node by key, plus a **doubly linked list** to maintain usage order. Because the HashMap hands you a direct reference to the node, removing it from the list is O(1) — you don't need to search for its neighbors, you already have the node itself (and with `prev`/`next` pointers, you can rewire around it instantly). Two sentinel nodes (the dummy-head technique, applied at *both* ends this time) eliminate every edge case at the list's boundaries.

```java
class LRUCache {
    class Node {
        int key, value;
        Node prev, next;
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> map;
    private final Node head;   // sentinel — head.next is the most recently used real node
    private final Node tail;   // sentinel — tail.prev is the least recently used real node

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.map = new HashMap<>();
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        remove(node);
        addToFront(node);    // using it makes it most recently used
        return node.value;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.value = value;
            remove(node);
            addToFront(node);
            return;
        }
        if (map.size() == capacity) {
            Node lru = tail.prev;        // node right before the tail sentinel = least recently used
            remove(lru);
            map.remove(lru.key);
        }
        Node newNode = new Node(key, value);
        map.put(key, newNode);
        addToFront(newNode);
    }

    // O(1): no search needed, we already have direct references via the map
    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    // O(1): insert immediately after the head sentinel = most-recently-used position
    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
}
```

**Trace** with `capacity = 2`:

```
put(1,1): cache empty.                       List: head↔1↔tail.            map={1}
put(2,2): not full yet.                      List: head↔2↔1↔tail.          map={1,2}
get(1):   found. move to front.              List: head↔1↔2↔tail.          return 1
put(3,3): not in map, size==capacity(2).
          evict tail.prev = 2 (LRU).         List after evict: head↔1↔tail. map={1}
          insert 3 at front.                 List: head↔3↔1↔tail.          map={1,3}
get(2):   not in map (evicted).              return -1   ✓
get(3):   found, already at front.           return 3    ✓
```

**Complexity:** `get` and `put` are both O(1) — HashMap lookup is O(1), and every linked-list operation touches a fixed number of pointers regardless of cache size. Space O(capacity).

---

## Common Mistakes — Chapter-Wide

- **Updating only one side of a doubly-linked removal.** `remove()` must rewire *both* `node.prev.next` and `node.next.prev`. Forgetting either leaves a dangling or inconsistent link.
- **Using a singly linked list for LRU.** Without a `prev` pointer, removing an arbitrary node by direct reference still costs O(n) to find its predecessor — the entire point of the doubly linked list is O(1) removal from anywhere.
- **In `put()`, updating a key's value but forgetting to also move it to the front.** Both halves of "this key was just used" matter — the value and the recency.
- **Checking `slow == fast` before the first move in Floyd's algorithm.** Both pointers start at `head`, so they're trivially equal before any movement — check *after* advancing, inside the loop, as shown.
- **Forgetting `head.next = null` in recursive reversal**, creating a 2-node cycle (see Pattern 2's Common Mistakes above).
- **Using the wrong fast-slow loop condition for which middle you need.** `fast != null && fast.next != null` lands on the *second* middle for even-length lists; `fast.next != null && fast.next.next != null` lands on the *first*. Reorder List specifically needs the first — check before coding.

## Pattern Recognition Guide

- "Reverse a linked list (or a sub-section of one)" → iterative reversal for O(1) space, recursive for cleaner code at O(n) space.
- "Find the middle node" → fast-slow pointers; pick the loop condition matching which middle (first vs. second) the problem actually needs.
- "Determine if a list has a cycle" → Floyd's algorithm.
- "Find where a cycle begins" → Floyd's algorithm, then the two-pointer reset trick (reset one pointer to `head`, walk both one step at a time).
- "Merge two sorted lists" → dummy head + compare-and-advance.
- "Merge k sorted lists" → min-heap of the k current front nodes.
- "Design a cache with an eviction policy based on usage order" → HashMap (for O(1) lookup) + doubly linked list with sentinel nodes (for O(1) reordering/removal).
- Any problem where "the head might need to change" → dummy head technique, no exceptions.

## Chapter Summary

- A linked list trades O(1) random access (which arrays have) for O(1) insert/delete given a reference to the right spot — there's no free lunch, only a different trade.
- The dummy head technique turns "modifying the head is a special case" into "every modification is the same uniform code." Use it whenever the head might change.
- Iterative reversal is O(1) space; recursive reversal is O(n) space due to the call stack — both are O(n) time. Know which one you're claiming.
- Floyd's cycle detection isn't a lucky heuristic — the gap between `fast` and `slow` increases by exactly 1 (mod cycle length) every step, so it's mathematically guaranteed to hit 0 within one lap.
- The cycle entry point trick follows directly from the algebra `a ≡ (C − b) mod C` — it's not a memorized incantation, it's a derived consequence of fast moving twice as fast as slow.
- Merging two lists uses dummy head + compare-and-advance; merging k lists generalizes that with a min-heap, trading O(nk) for O(n log k).
- LRU Cache is the canonical "combine two data structures to get both of their O(1) guarantees" problem: HashMap for lookup, doubly linked list with sentinels for order.
