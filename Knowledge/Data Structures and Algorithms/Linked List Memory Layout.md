---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 3 — Linked Lists"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, linked-lists, memory-layout]
---

# Linked List Memory Layout

Unlike an array whose elements are contiguous in memory, a linked list's nodes are scattered across memory wherever the garbage collector placed them. They are connected only by pointers.

## The Trade-off
There is no `address(i)` formula. To reach the 5th node, you must visit nodes 1 through 4 first. 
- **Random access is $O(n)$**, not $O(1)$. 
- **Insertion and deletion are $O(1)$**, *if* you already hold a reference to the node before your target position. Just rewire two pointers; nothing shifts.
- **No resizing:** A new node is simply allocated and linked in, avoiding the $O(n)$ resize-and-copy penalty of dynamic arrays.

## Node Structure
```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}
```
