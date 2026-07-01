---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, gotcha, equality]
---

# The Integer Cache Trap

This is a classic Java interview question regarding autoboxing and object equality.

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b); // true

Integer c = 128;
Integer d = 128;
System.out.println(c == d); // false
```

## Why this happens
When autoboxing (`Integer a = 127;`), the compiler calls `Integer.valueOf(127)`. 

To optimize performance, the JVM pre-caches `Integer` objects for values between **-128 and 127** at startup. 
- For values in this range, `Integer.valueOf()` returns a reference to the **same cached object**. Since `a` and `b` point to the exact same object in memory, `a == b` is `true`.
- For values outside this range (like 128), `Integer.valueOf()` creates a **new object** on the Heap. `c` and `d` point to different objects, so `c == d` is `false`.

## The Rule
**Never use `==` to compare object wrappers.** Always use `.equals()`, which compares the underlying values rather than the memory addresses.
```java
System.out.println(c.equals(d)); // true
```
