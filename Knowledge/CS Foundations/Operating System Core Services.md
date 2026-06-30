---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [cs-foundations, os]
---

# Operating System Core Services

The OS is a program that runs first and manages all other software and hardware. Without it, programs would interfere with each other (e.g., two programs trying to use the printer at once, or overwriting each other's memory).

## Four Fundamental Services
1. **Process management:** Run multiple programs simultaneously by giving each a slice of CPU time and isolating them.
2. **Memory management:** Give each program its own private section of RAM (virtual memory) so they cannot read/write each other's memory.
3. **File system:** Organize persistent data on disk into files and directories, providing a consistent API for reading/writing regardless of the underlying storage hardware.
4. **Device drivers:** Translate between programs and hardware. Programs use standard system calls (like `write()`) and the OS driver handles the specific hardware I/O.
