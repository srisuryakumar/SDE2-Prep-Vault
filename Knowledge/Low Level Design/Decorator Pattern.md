---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 3 — Structural Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Proxy Pattern"]
tags: [lld, design-patterns, structural]
---

# Decorator Pattern

## Intuition
You want to add behaviors (like logging, caching, retry) to an object dynamically at runtime without modifying the object's code and without using deep inheritance hierarchies.

## The Solution
A Decorator implements the same interface as the object it wraps. It intercepts calls, performs its added behavior (e.g., logging the start time), delegates the actual work to the wrapped object, and then performs any post-behavior.
Because decorators implement the same interface, you can stack them infinitely (`LoggingDecorator` wraps `CachingDecorator` wraps `RealService`).

## Real-World Example: Java I/O
```java
BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream("data.txt")));
```
Each class is a decorator adding one specific behavior (line-reading, decoding, file reading) to the underlying stream.

**Decorator vs Inheritance:**
Inheritance is static and determined at compile time. Decorator is dynamic. Furthermore, inheritance suffers from combinatorial explosion if you want multiple combinations of behaviors.
