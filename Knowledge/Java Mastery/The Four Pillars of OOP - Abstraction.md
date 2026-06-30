---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, oop, abstraction, interfaces]
---

# The Four Pillars of OOP - Abstraction

Abstraction involves hiding complex implementation details and exposing only a clean, simple interface to the user. In Java, this is achieved through Abstract Classes and Interfaces.

## Abstract Classes (`abstract class`)
- **Use when:** You have an "IS-A" hierarchy and want to share state (instance fields) and common method implementations among related classes.
- **Rules:** Cannot be instantiated directly. Can have both abstract methods (no body) and concrete methods. A class can extend only **one** abstract class.

## Interfaces (`interface`)
- **Use when:** You want to define a "CAN-DO" contract across potentially unrelated classes (e.g., `Serializable`, `Runnable`).
- **Rules:** A class can implement **multiple** interfaces.
- **Modern Features (Java 8+):** Interfaces can now include `default` methods (which provide a default implementation) and `static` methods. They still cannot hold instance state (fields).

*Rule of Thumb:* Start with an interface. Only move to an abstract class if you need to share mutable state or have a strict inheritance hierarchy.
