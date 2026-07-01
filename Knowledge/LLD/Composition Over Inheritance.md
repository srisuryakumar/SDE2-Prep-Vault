---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Strategy Pattern"]
tags: [oop, design-principles, architecture]
---

# Composition Over Inheritance

## Intuition
Inheritance models a rigid `IS-A` relationship. It is powerful but brittle: subclasses are tightly coupled to parents, leading to the "Fragile Base Class Problem" where changing a parent breaks distant subclasses.

## The Problem with Inheritance
If you have a `Bird` class with `fly()` and `swim()` methods, and you create a `Penguin` subclass, it must override `fly()` to throw an exception (violating LSP). As edge cases grow, deep inheritance trees become unmaintainable.

## The Solution (Composition)
Model behaviors as interchangeable interfaces (`Flyable`, `Swimmable`). Instead of a class being a subclass of a master behavior class, it **HAS-A** behavior. 
A `Penguin` object holds a `SwimmingBehavior` and a `NoFlyingBehavior`. 

**When to prefer Composition:**
- Behavior varies independently of the class hierarchy.
- You need to mix and match behaviors (e.g., flying + swimming).
- You want to change behavior at runtime (Strategy pattern).
