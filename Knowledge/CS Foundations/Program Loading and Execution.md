---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 3 — How Programs Run"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, process, jvm]
---

# Program Loading and Execution

When you run a command like `java -jar myapp.jar`, the OS and the JVM go through several steps to load the program into memory and execute it.

1. **Process Creation:** The shell `fork()`s a child process, then calls `exec("java")`. The OS replaces the child's memory image with the `java` native binary loaded from disk into RAM.
2. **JVM Initialization:** The JVM (a native C++ program) starts. It initializes the garbage collector (GC), JIT compiler threads, and ClassLoaders.
3. **Application Loading:** The JVM locates `myapp.jar`, finds the `Main-Class` from the manifest, and loads the bytecode into the JVM.
4. **Execution:** The JVM executes `main()`. For frameworks like Spring Boot, this triggers auto-configuration, component scanning, embedded Tomcat startup, and connection pool initialization.
5. **Event Loop:** The JVM enters an event loop (e.g. Tomcat's acceptor threads) waiting for requests.

This heavy startup process (loading thousands of classes, JIT profiling, establishing connections) takes 5-30 seconds. In Kubernetes, this delay is why **readiness probes** are essential to prevent traffic from hitting a pod before it is fully initialized.
