---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 1 — How Java Works"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, jvm, compilation]
---

# Java Compilation Pipeline and Bytecode

Java's compilation model was designed to solve the "compile once per platform" problem (Write Once, Run Anywhere).

## The Pipeline
1. **Source Code (`.java`):** Human-readable code.
2. **Compiler (`javac`):** The Java compiler reads `.java` and compiles it into `.class` files.
3. **Bytecode (`.class`):** This is a platform-neutral binary format. It is not native machine code (x86 or ARM); it is an instruction set for an imaginary CPU called the Java Virtual Machine (JVM).
4. **JVM Execution Engine:**
   - **Interpreter:** When the JVM runs the bytecode, it interprets it line-by-line initially (which is slow).
   - **JIT (Just-In-Time) Compiler:** The JVM monitors the execution for "hot paths" (e.g., methods called 10,000+ times). It compiles these hot bytecode paths into native machine code on the fly. Subsequent calls run at near-native speed.

This hybrid approach allows Java applications to start immediately (via interpretation) and eventually reach C++ level speeds (via JIT compilation) once they "warm up".
