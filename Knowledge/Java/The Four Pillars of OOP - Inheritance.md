---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, oop, inheritance]
---

# The Four Pillars of OOP - Inheritance

Inheritance allows a new class (Subclass) to inherit fields and methods from an existing class (Superclass), creating an "IS-A" relationship (e.g., a `Dog` IS-A `Animal`).

## Syntax and Rules
- Use the `extends` keyword: `class Dog extends Animal {}`.
- Java supports **single inheritance** only: a class can extend only one superclass.
- **Inherited:** All visible fields and non-private methods.
- **Not Inherited:** Constructors. The subclass must define its own constructors and use the `super(...)` keyword as its first statement to call the parent's constructor.

## Method Overriding
A subclass can provide a specific implementation of a method already defined in its parent.
- Always use the `@Override` annotation. This tells the compiler to check that you are actually overriding a parent method. Without it, a typo in the method signature silently creates a brand new method instead of overriding the parent's.
