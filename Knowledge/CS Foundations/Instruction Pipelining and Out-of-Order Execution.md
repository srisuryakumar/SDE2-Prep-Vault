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

# Instruction Pipelining and Out-of-Order Execution

Modern CPUs use two techniques to dramatically improve throughput, but they introduce subtle problems for concurrent programming.

## Pipelining
Overlapping the fetch, decode, and execute stages of consecutive instructions. Like an assembly line, while instruction 5 is executing, instruction 6 is decoding, and instruction 7 is being fetched simultaneously.

## Out-of-Order Execution
The CPU detects when two instructions are independent (they don't use each other's results) and executes them in a different order than written to keep the execution units busy. This happens invisibly in the hardware.

## Implications for Concurrency (Memory Reordering)
These techniques mean two threads on different cores may see the results of memory writes in a different order than the code wrote them. For example, Thread A writes variable X then variable Y, but Thread B might see Y change before X.

This phenomenon is called **memory reordering**. It is the reason why Java's `volatile` keyword and `synchronized` blocks exist—they include **memory barriers** that force the CPU to flush and order its writes correctly.
