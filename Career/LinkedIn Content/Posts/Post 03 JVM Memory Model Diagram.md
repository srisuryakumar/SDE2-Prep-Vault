---
type: linkedin-post
post_number: 3
scheduled_week: 2
scheduled_day: Tuesday
status: drafted
---
I spent 2 hours understanding JVM memory. Here's what I drew.

[ATTACH: Hand-drawn or Canva diagram of JVM memory areas]

The diagram shows:
→ Heap: shared by all threads (Eden → Survivor → Old Generation)
→ Stack: one per thread, holds method call frames
→ Metaspace: class metadata (replaced PermGen in Java 8)

Why it matters in production:
- OutOfMemoryError: Java heap space → Eden or Old Gen is full
- StackOverflowError → recursion too deep
- OutOfMemoryError: Metaspace → too many dynamically loaded classes

Day 9 insight: when an object 'escapes' a method, the JIT cannot
stack-allocate it. That's why short-lived objects inside tight loops
are not always free — they put pressure on Eden and trigger Minor GCs.

Drawing systems you're learning beats watching someone else explain them.

#Java #JVM #BackendEngineering
