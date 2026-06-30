---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, os, memory]
---

# Virtual Memory and Page Faults

Multiple processes share one physical RAM. The OS uses **virtual memory** to give each process the illusion that it has the entire address space to itself. The Memory Management Unit (MMU) in the CPU translates these virtual addresses to physical RAM addresses automatically.

## Page Tables and MMU
- **Page:** A fixed-size chunk of memory, typically 4 KB.
- **Page table:** Maintains the mapping from a process's virtual pages to physical frames.
- **TLB (Translation Lookaside Buffer):** A CPU cache for page table lookups, preventing the need to check RAM on every memory access.

## Page Faults
A page fault occurs when a process accesses a virtual address not currently backed by physical RAM. The CPU raises an exception, and the OS:
1. Validates the address. If invalid, the process is killed (Segmentation Fault).
2. If valid, finds a free physical frame, loads the page from disk (or allocates it), and updates the page table.
3. Resumes the process.

Page faults only become a performance problem if they require disk I/O (swapping), leading to **thrashing** when RAM is full.

## JVM Memory Note
When you configure `-Xmx4g`, it sets the max size for the JVM heap. This heap is just one segment of the JVM process's virtual address space, which also needs memory for native libraries, thread stacks, and off-heap buffers.
