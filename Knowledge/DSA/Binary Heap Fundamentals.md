---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 7 — Heaps and Priority Queues"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, heaps, fundamentals]
---

# Binary Heap Fundamentals

A heap makes one promise: **instant access to the current best or worst element** of a changing collection. It is NOT a fully sorted structure. Only the relationship between a parent and its immediate children is guaranteed.

## Structure
A binary heap is a complete binary tree stored in a plain array.
For any element at index `i`:
- `parent(i) = (i - 1) / 2`
- `leftChild(i) = 2*i + 1`
- `rightChild(i) = 2*i + 2`

## Min-Heap vs. Max-Heap
- **Min-heap:** Every parent $\le$ its children. Root is the minimum.
- **Max-heap:** Every parent $\ge$ its children. Root is the maximum.

## Operations
- **Heapify Up (Insert):** Add to the next open array slot (end of array), then "bubble up" (swap with parent) until the heap property is restored. $O(\log n)$.
- **Heapify Down (Extract):** Remove the root. Move the *last* element in the array to the root, then "bubble down" (swap with the smaller/larger child) until the heap property is restored. $O(\log n)$.

## Java PriorityQueue
`PriorityQueue` is backed by a binary heap. `offer` is heapify-up ($O(\log n)$), `poll` is heapify-down ($O(\log n)$), and `peek` is $O(1)$.
**Default is Min-Heap.** For a Max-Heap, use `new PriorityQueue<>(Collections.reverseOrder())`.

**WARNING:** Iterating over a `PriorityQueue` directly does NOT produce sorted order. Only repeated `poll()` calls guarantee sorted output.
