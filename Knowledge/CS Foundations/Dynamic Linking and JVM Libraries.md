---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 3 — How Programs Run"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, libraries]
---

# Dynamic Linking and JVM Libraries

Programs often reuse standard libraries (like the C standard library or cryptography functions). If every program had a full copy of these libraries, executables would be huge.

## Static vs Dynamic Linking
- **Static Linking:** The linker copies all library code into the final executable at build time.
- **Dynamic Linking:** The executable contains *references* to library functions. The OS loads a single copy of the shared library into RAM (e.g., `.so` on Linux, `.dylib` on macOS, `.dll` on Windows) and multiple programs share it at runtime.

## Java and Dynamic Libraries
Java JAR files act like shared libraries containing compiled `.class` files. The JVM's `ClassLoader` functions as the dynamic linker, connecting classes at runtime.

The JVM itself (`libjvm.so`) is a native shared library. The small `java` executable loads `libjvm.so` dynamically, which then runs your Java application. This layered architecture is why you can install multiple Java versions side-by-side and easily switch between them.
