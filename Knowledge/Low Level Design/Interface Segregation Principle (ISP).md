---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: ["Dependency Inversion Principle (DIP)"]
tags: [oop, solid, design-principles]
---

# Interface Segregation Principle (ISP)

## Intuition
Clients should not be forced to depend upon interfaces they do not use.
Fat, monolithic interfaces force implementing classes to provide dummy methods or throw exceptions for behaviors they don't support.

## The Classic Violation
A single `Worker` interface with `work()`, `eat()`, and `sleep()`.
A `RobotWorker` implements `Worker`, but is forced to implement `eat()` and `sleep()` (usually by throwing `UnsupportedOperationException`).

## The Fix
Split the fat interface into smaller, highly cohesive interfaces: `Workable`, `Feedable`, and `Restable`.
A `HumanWorker` implements all three. A `RobotWorker` implements only `Workable`.
