---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 3 — Linked Lists"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, linked-lists, pattern, reversal]
---

# Linked List Reversal

## Iterative Reversal ($O(1)$ Space)
Three pointers are needed: `prev`, `curr`, and `next`.
**The Trap:** Once you overwrite `curr.next`, you lose the rest of the list. You MUST save "what's next" in a temporary variable *before* you overwrite.

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    while (curr != null) {
        ListNode next = curr.next;   // 1. save next before overwriting
        curr.next = prev;            // 2. reverse the pointer
        prev = curr;                 // 3. advance prev
        curr = next;                 // 4. advance curr
    }
    return prev;   // prev ends up at the new head
}
```

## Recursive Reversal ($O(n)$ Space)
Trust the recursion to reverse the rest of the list. Then, wire the node after `head` back to `head`, and set `head.next` to `null`.

```java
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head; // Base case
    
    ListNode newHead = reverseList(head.next);
    
    head.next.next = head; // The node right after head points back to head
    head.next = null;      // Head becomes the new tail (CRITICAL: prevents cycle)
    
    return newHead;
}
```
*Note: The recursive version is $O(n)$ space due to the call stack depth.*
