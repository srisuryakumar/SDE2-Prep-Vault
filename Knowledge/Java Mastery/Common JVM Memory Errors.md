---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 2 — JVM Memory Architecture"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, jvm, errors, memory]
---

# Common JVM Memory Errors

Understanding JVM errors requires knowing the underlying memory architecture.

## 1. OutOfMemoryError: Java heap space
- **Cause:** The heap is full, and Garbage Collection cannot reclaim enough memory to allocate a new object.
- **Diagnosis:** Usually caused by a memory leak (e.g., strong references held in a static `HashMap` preventing objects from being collected).
- **Fix:** Use `-XX:+HeapDumpOnOutOfMemoryError` to generate a heap dump, then analyze it with a tool like Eclipse MAT to find the "Leak Suspect".

## 2. OutOfMemoryError: Metaspace
- **Cause:** The Metaspace (native memory region for class metadata) is full.
- **Diagnosis:** The application has loaded too many classes. Common in applications that dynamically generate bytecode at runtime (like ORMs/Hibernate) or frequently spawn new ClassLoaders.

## 3. StackOverflowError
- **Cause:** A thread's stack is exhausted.
- **Diagnosis:** Method frames are pushed onto the stack faster than they are popped. Almost always caused by infinite recursion without a base case, or a circular call chain between two methods.
