---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 2 — JVM Memory Architecture"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, jvm, memory, architecture]
---

# JVM Memory Regions (Heap, Stack, Metaspace)

The JVM divides memory into several key regions to manage execution and object lifecycles:

## 1. The Heap
- **Purpose:** Where all objects (created with `new`) live.
- **Scope:** Shared across all threads.
- **Structure:** Divided into the **Young Generation** (Eden + two Survivor spaces) for short-lived objects, and the **Old Generation** (Tenured) for long-lived objects.
- **Management:** This is the primary area managed by Garbage Collection.

## 2. The Stack
- **Purpose:** Where method calls and local variables live.
- **Scope:** Thread-private (each thread gets its own stack).
- **Structure:** Divided into **Stack Frames**. A frame is pushed when a method is called and popped when it returns.
- **Contents:** Holds local primitive variables directly, and holds references (memory addresses) pointing to objects on the Heap.

## 3. Metaspace
- **Purpose:** Holds class-level metadata (class definitions, method bytecode, field descriptors, static fields).
- **Scope:** Shared across all threads.
- **Location:** Resides in native memory (not on the Heap).
- **Note:** Replaced the older "PermGen" in Java 8. It grows dynamically up to available system memory, preventing many `OutOfMemoryError: PermGen space` issues.

## 4. PC Register & Native Method Stack
- **PC Register:** A tiny per-thread register tracking the address of the currently executing bytecode instruction.
- **Native Method Stack:** Used for native C/C++ code invoked via JNI.
