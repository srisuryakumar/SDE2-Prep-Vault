---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, arrays, memory-layout, fundamentals]
---

# Array Memory Layout

An array is the simplest possible data structure: a contiguous block of memory where every element occupies exactly the same number of bytes.

## O(1) Random Access
Because the block is contiguous and every slot is the same size, the memory address of any element $i$ is calculated mathematically:
`address(i) = baseAddress + i * elementSize`

This formula takes one multiplication and one addition regardless of $i$. That's why random access is $O(1)$ — finding the element is completely independent of the array's size.

## Cache Locality
Elements live at consecutive addresses. When the CPU fetches `arr[0]`, it pulls an entire cache line (typically 64 bytes = 16 integers) into the fast L1 cache all at once. Subsequent accesses to `arr[1]` through `arr[15]` hit the L1 cache and are effectively free. This invisible performance advantage makes array-based algorithms almost always faster in practice than linked list equivalents.

## The Cost
- **Fixed size:** Java arrays cannot grow. `ArrayList` handles growth by allocating a new array and copying elements ($O(n)$ work, $O(1)$ amortized).
- **Insert/Delete:** Inserting or deleting in the middle requires shifting all subsequent elements, taking $O(n)$ time.
