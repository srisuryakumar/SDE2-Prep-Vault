---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, os]
---

# System Calls

A system call (syscall) is the only way for a user-space program to request a service from the kernel. It is a special CPU instruction that switches the CPU from user mode (Ring 3) to kernel mode (Ring 0).

## Common System Calls
- `read()` / `write()`: Read/write bytes to a file descriptor (file, socket, pipe).
- `open()` / `close()`: Open/close a file descriptor.
- `fork()`: Create a new process (copy of current).
- `exec()`: Replace current process image with a new program.
- `socket()` / `connect()` / `accept()`: Network socket operations.
- `clone()`: Create a new thread (on Linux).
- `epoll()`: Efficient I/O event notification (used by Netty, Node.js).

## Overhead
Syscalls are relatively expensive (~1-5 microseconds) because they require a CPU mode switch, context saving/restoring, and kernel validation. 

This is why backend frameworks batch operations:
- Java NIO / Netty uses `epoll` to multiplex thousands of connections onto one syscall.
- `BufferedWriter` collects small writes and flushes them in one `write()` syscall instead of calling it per character.
- Database connection pools reuse TCP connections to avoid `socket()` and `connect()` per query.
