---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, os]
---

# Process State and Context Switching

## Process State Machine
A process transitions between several states:
- **NEW:** Being created.
- **READY:** Loaded in memory, waiting for its turn on the CPU.
- **RUNNING:** Currently executing instructions on a CPU core.
- **BLOCKED/WAITING:** Waiting for an event (I/O, network packet, lock release). It cannot use the CPU.
- **TERMINATED:** Process exited.

## Context Switching
The OS creates the illusion of simultaneous execution by **time-slicing** (running each process for a short interval, ~1-10ms). Pausing one process and resuming another is a **context switch**.

Cost of a context switch (~1-10 microseconds):
- Save all CPU registers to the Process Control Block (PCB).
- Run the scheduler to pick the next process.
- Restore CPU registers from the new PCB.
- Flush L1/L2 caches (since the previous process's data is now invalid for the new process).

At high loads (e.g. 100,000 context switches per second), this overhead becomes significant.
