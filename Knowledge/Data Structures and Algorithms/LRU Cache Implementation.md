---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 3 — Linked Lists"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, linked-lists, lru-cache, design]
---

# LRU Cache Implementation

Design a cache with $O(1)$ `get` and $O(1)$ `put` that evicts the **least recently used** item when exceeding capacity.

## Why HashMap alone fails
$O(1)$ lookup, but no concept of order. Finding the LRU item would be $O(n)$.

## Why Linked List alone fails
Tracks order easily (move used to front), but finding a specific key by value is $O(n)$.

## The Solution: HashMap + Doubly Linked List
- `HashMap<Integer, Node>` provides instant lookup.
- **Doubly linked list** maintains usage order. Since the map gives you a direct reference to the node, removing it from the list is $O(1)$ because you can rewire `prev` and `next` instantly.
- Two **sentinel nodes** (dummy head and dummy tail) eliminate all boundary edge cases.

```java
class LRUCache {
    class Node { int key, value; Node prev, next; ... }
    
    // ... fields: capacity, map, head, tail ...

    public void get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        remove(node);
        addToFront(node); // Most recently used
        return node.value;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key); node.value = value;
            remove(node); addToFront(node);
            return;
        }
        if (map.size() == capacity) {
            Node lru = tail.prev; // Least recently used is right before tail
            remove(lru); map.remove(lru.key);
        }
        Node newNode = new Node(key, value);
        map.put(key, newNode); addToFront(newNode);
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev; // Common mistake: forgetting to update both sides
    }

    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
}
```
