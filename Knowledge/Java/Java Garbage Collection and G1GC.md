---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 2 — JVM Memory Architecture"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, jvm, gc]
---

# Java Garbage Collection and G1GC

Garbage Collection (GC) automatically reclaims memory from objects that are no longer reachable by the application.

## GC Roots and Reachability
The GC determines liveness via reachability analysis. It starts from **GC Roots**:
- Local variables in active thread stacks
- Static fields
- JNI references
- Interned strings

Any object reachable from a GC root is "live". Any object with NO path from a GC root is "garbage" and is collected. This handles circular references gracefully.

## Generational GC
- **Minor GC:** Scans only the Young Generation. It uses a **Mark-and-Copy** algorithm: live objects in Eden and the active Survivor space are copied to the empty Survivor space. Eden is then cleared instantly. Fast, but stop-the-world.
- **Major/Full GC:** Scans the Old Generation (or the entire heap). Much slower and disruptive.

## G1GC (Garbage-First GC)
The default collector in Java 21. Instead of contiguous Young/Old areas, G1 divides the heap into ~2000 equal-sized **regions** (e.g., 2MB each).
- It performs concurrent marking in the background to find regions with the most garbage.
- During a Mixed GC, it collects all Young regions and *only the most garbage-dense Old regions*, targeting a user-defined pause time (e.g., `-XX:MaxGCPauseMillis=200`).
- Provides predictable, low-latency pauses for large heaps.

## Essential GC JVM Flags
- `-Xms2g -Xmx2g`: Fixed heap size to prevent resizing pauses.
- `-XX:+UseG1GC`: Use G1 Garbage Collector.
- `-XX:+HeapDumpOnOutOfMemoryError`: Crucial for production debugging.
