---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Interface Segregation Principle (ISP)"]
tags: [oop, solid, design-principles]
---

# Liskov Substitution Principle (LSP)

## Intuition
If `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` **without altering the correctness** of the program.
A subclass must be usable wherever its parent class is used, without surprising the caller.

## The Classic Violation (Rectangle / Square)
Mathematically, a Square is a Rectangle. In OOP, if `Square extends Rectangle`, it usually violates LSP.
If a caller expects a `Rectangle` and sets the width to 5 and height to 10, it expects the area to be 50. But if a `Square` internally forces width and height to be equal (silent side effects), it breaks the caller's expectations (area becomes 100).

## The Fix
Don't use inheritance if it violates expectations. Use a common interface `Shape` that only defines `area()`. Both `Rectangle` and `Square` implement `Shape` independently.

**Rule of Thumb:** If a subclass overrides a method to throw `UnsupportedOperationException`, it violates LSP.
