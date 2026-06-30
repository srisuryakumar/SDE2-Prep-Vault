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

# Process vs Thread

## Process
A process is a running instance of a program. It is the container that holds:
- Its own isolated virtual memory (address space).
- Open file descriptors.
- A unique process ID (PID).
Multiple runs of the same program (like running `java -jar myapp.jar` twice) create completely separate processes.

### Creating Processes
Unix/Linux uses two system calls:
- **`fork()`:** Creates an exact copy of the current process (identical memory, open files, program counters, but different PID).
- **`exec()`:** Replaces the current process's memory image with a completely different program loaded from disk.

## Thread
A thread is a unit of execution *within* a process. A process starts with one thread (main) and can spawn more.
- **Shared:** All threads in a process share the same heap memory (address space).
- **Separate:** Each thread has its own call stack and program counter.

### Why separate stacks but shared heap?
- **Separate stacks:** Needed to track each thread's independent function call chain (Thread A executing `main()`, Thread B executing `handleRequest()`).
- **Shared heap:** Allows threads to easily share data (like a shared `HashMap`), but this requires synchronization to prevent race conditions.
