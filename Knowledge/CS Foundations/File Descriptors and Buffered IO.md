---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, os, file-system]
---

# File Descriptors and Buffered IO

## File Descriptors
When a process opens a file or network socket, the OS returns an integer called a **file descriptor (fd)**. The OS maintains a table mapping each file descriptor to an open file object.
- `0`: stdin
- `1`: stdout
- `2`: stderr
- `3+`: Any files or TCP sockets the process opens.

Every I/O system call (`read()`, `write()`, `close()`) uses this fd. 

### Too Many Open Files
The OS limits how many file descriptors one process can have open (configured via `ulimit -n`). If a Spring Boot server under high load opens too many HTTP connections, DB connections, or log files, it will crash with `java.io.IOException: Too many open files`.

## Buffered I/O
Reading or writing one byte at a time is catastrophically slow because each byte requires a system call (~1-5μs overhead). 

Buffering collects bytes in memory (e.g. an 8KB buffer) and performs ONE system call when full. This is why `BufferedOutputStream` wrapping a `FileOutputStream` (or `BufferedWriter` wrapping `FileWriter`) is crucial for performance in Java.
