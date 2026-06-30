---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 3 — How Programs Run"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, compilation]
---

# Source Code Compilation and Execution

Source code is just text. The hardware only understands machine code (binary instructions specific to a CPU architecture). 

There are three main approaches to bridging this gap:

## 1. Compiled Languages (C, C++, Go, Rust)
The compiler translates source code into machine code *before execution*. The result is a native binary.
- **Pros:** Maximum runtime performance, small deployment artifacts.
- **Cons:** Must be recompiled for every target OS/CPU architecture.

## 2. Interpreted Languages (Python, Ruby, Shell)
An interpreter (itself a native program) reads the source code line-by-line at runtime and executes it.
- **Pros:** Write once, run anywhere. Easy to iterate.
- **Cons:** Slow, because every statement incurs interpretation overhead every time it runs.

## 3. Just-In-Time (JIT) Compiled (Java, C#, JS/V8)
A hybrid approach. The code is first compiled to an intermediate representation (bytecode). At runtime, a Virtual Machine (JVM, V8) interprets the bytecode.
- **JIT Compilation:** As the program runs, the VM profiles which methods are "hot" (frequently executed). It then compiles those specific methods directly to native machine code. 
- After this "warmup" period, the hot paths run at near-native speed.
