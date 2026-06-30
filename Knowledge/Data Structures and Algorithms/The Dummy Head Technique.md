---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 3 — Linked Lists"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, linked-lists, pattern, dummy-head]
---

# The Dummy Head Technique

Modifying a node's `next` pointer is uniform code, but modifying the `head` reference itself is a special case because `head` is a variable, not a node's field. Writing two different code paths for the same logical operation (e.g., removing a node) produces bugs.

**The Fix:** Insert a fake **sentinel node** before the real head. 
Now the real head is always "some node's `.next`", never a bare variable — every modification becomes the uniform case.

## Template
```java
ListNode dummy = new ListNode(0);
dummy.next = head;
ListNode curr = dummy;

while (curr.next != null) {
    if (curr.next.val == TARGET) {
        curr.next = curr.next.next; // Rewire (works even if deleting the actual head)
    } else {
        curr = curr.next;
    }
}
return dummy.next; // The correct (possibly new) head
```

**Rule of Thumb:** Use this any time the head of the list might need to change (removing a node, reversing, merging, partitioning). It costs one extra node and removes an entire category of edge-case bugs.
