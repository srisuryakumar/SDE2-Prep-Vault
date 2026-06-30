---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 1 — The Computer at Its Core"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations]
---

# RAM Swap and Paging

When you run a program like `java -jar myapp.jar`, the OS reads the binary from disk into RAM, creates a process, and begins execution.

## The Swap Mechanism
If your application loads 10 GB of data into RAM, but the server only has 8 GB, the OS is forced to move some RAM contents to disk to make room. This is called **swap** or **paging**.

### The Performance Cliff
Disk I/O is 1,000-10,000x slower than RAM. When a system starts swapping heavily (known as **thrashing**), every memory access that hits a swapped-out page requires a disk read (~100,000ns vs 100ns). The application becomes thousands of times slower.

### Out of Memory (OOM)
When a JVM runs out of heap memory and garbage collection cannot free enough space, it throws `OutOfMemoryError: Java heap space` and crashes.

This dynamic is why Kubernetes relies heavily on resource requests and limits (`resources.limits.memory`). If a memory-hungry pod starts thrashing, it can starve the entire node. Kubernetes prefers to kill and restart a pod cleanly (OOMKilled) rather than allow it to thrash indefinitely.
