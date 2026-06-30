---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 3 — How Programs Run"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, compilation, java]
---

# Java Compilation and JIT (HotSpot)

Java has a two-stage compilation process:

## Stage 1: Ahead-of-Time to Bytecode
`javac` compiles `.java` source code into `.class` files. These contain **JVM bytecode** (a platform-independent, intermediate instruction set), not native machine code.

## Stage 2: JVM Runtime Interpretation and JIT
When you run `java MyApp`, the JVM loads the bytecode:
1. It interprets the bytecode initially (interpreter mode).
2. The JVM's profiler (C1 compiler) monitors method execution counts.
3. Methods called frequently (e.g. >10,000 times) are "hot spots".
4. The C2 compiler **JIT-compiles** these hot methods to native machine code (x86-64/ARM).
5. The native compiled code runs at CPU-native speed.

This is why Java applications need a **warmup** period to reach peak performance, and why the JVM is called "HotSpot".

## GraalVM Native Image
GraalVM can perform JIT compilation *ahead of time* (AOT), producing a standalone native binary. 
- **Pros:** Instant startup (no warmup), lower memory usage.
- **Cons:** Longer build times, breaks some dynamic features like reflection unless explicitly configured.
