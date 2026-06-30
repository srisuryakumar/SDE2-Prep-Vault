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

# CPU Architecture and Registers

The **Central Processing Unit (CPU)** is the chip that executes instructions. An instruction is a numeric code that the CPU decodes into an operation (like add, jump, load).

## Anatomy of a CPU
- **Control Unit (CU):** The manager of the CPU. Reads instructions, decodes them, and coordinates the ALU, registers, and memory.
- **Arithmetic Logic Unit (ALU):** The calculator. Performs math and logical operations on values stored in registers.
- **Registers:** Tiny, ultra-fast storage inside the CPU. Takes < 1ns to access.

### Key Registers
- **Program Counter (PC) / Instruction Pointer (IP):** Holds the memory address of the *next instruction to execute*. `jump` instructions change the PC.
- **Stack Pointer (SP):** Holds the memory address of the current top of the call stack.
- **General-purpose registers:** Hold the values currently being computed.
- **Flags register:** Holds the result of the last comparison (e.g., zero, negative, overflow).

## The Fetch-Decode-Execute Cycle
Every CPU runs this loop continuously:
1. **Fetch:** Read the instruction at the address in PC from memory.
2. **Decode:** Translate the instruction bytes into an operation.
3. **Execute:** Perform the operation using ALU, registers, and memory.
4. Increment PC and repeat.

A modern 3.5 GHz CPU performs 3.5 billion of these cycles per second per core.
