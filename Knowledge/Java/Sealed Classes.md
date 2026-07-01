---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, oop, sealed-classes]
---

# Sealed Classes

Introduced in Java 17, **sealed classes** (and interfaces) allow you to restrict which classes may extend or implement them.

## The `permits` Keyword
You define a closed hierarchy by specifying exactly which subclasses are permitted:
```java
public sealed interface Shape permits Circle, Rectangle, Triangle {}
```
Only `Circle`, `Rectangle`, and `Triangle` are allowed to implement `Shape`. Any other class attempting to implement it will cause a compile-time error.

## Exhaustive Pattern Matching
The primary benefit of sealed classes is that the compiler knows every possible subtype. This enables exhaustive pattern-matching in `switch` expressions without needing a `default` case:
```java
public static double area(Shape shape) {
    return switch (shape) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t  -> 0.5 * t.base() * t.height();
        // No 'default' needed! Compiler knows these are all the cases.
    };
}
```
