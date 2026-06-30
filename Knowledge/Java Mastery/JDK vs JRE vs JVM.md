---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 1 — How Java Works"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, jvm, tooling]
---

# JDK vs JRE vs JVM

These three acronyms describe different layers of the Java ecosystem.

## JVM (Java Virtual Machine)
The actual execution engine. It contains the ClassLoader, Bytecode Verifier, JIT Compiler, Garbage Collector, and Memory Manager. The JVM is an abstract specification (implemented by HotSpot, GraalVM, etc.) and is **platform-specific** (you need a different JVM binary for Windows, macOS, Linux).

## JRE (Java Runtime Environment)
**JVM + Java Standard Library** (`java.lang`, `java.util`, etc.). This is everything needed to **run** a compiled Java program. End users only need the JRE.

## JDK (Java Development Kit)
**JRE + Development Tools** (`javac` compiler, `jdb` debugger, `javadoc`, monitoring tools). Developers need the JDK. Since Java 11, Oracle no longer ships a standalone JRE; the JDK is used for both development and deployment, or a custom minimal runtime is built using `jlink`.
