---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 3 — Linked Lists"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, linked-lists, pattern, merge]
---

# Merging Sorted Lists

## 1. Merge Two Sorted Lists
Build the merged list with a dummy head and a `tail` pointer. At each step, compare the current heads of both lists, attach the smaller one, and advance. When one list runs out, directly splice the *entire remainder* of the other list on.

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0);
    ListNode tail = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) {
            tail.next = l1; l1 = l1.next;
        } else {
            tail.next = l2; l2 = l2.next;
        }
        tail = tail.next;
    }
    tail.next = (l1 != null) ? l1 : l2;   // attach whatever remains
    return dummy.next;
}
```

## 2. Merge K Sorted Lists
Generalize the two-list merge with a **min-heap** holding the current "front" node of each of the $k$ lists. Repeatedly pop the smallest, attach it to the result, and push its next node back into the heap.

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
        if (smallest.next != null) heap.offer(smallest.next);
    }
    return dummy.next;
}
```
**Complexity:** $O(n \log k)$ time instead of $O(nk)$ for sequential merging. Space $O(k)$ for the heap.
