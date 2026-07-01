---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Single Responsibility Principle (SRP)", "Dependency Inversion Principle (DIP)"]
tags: [oop, design-principles]
---

# Coupling and Cohesion

## Intuition
These two metrics define the physical structure of a well-designed system. The goal is always **High Cohesion and Loose Coupling**.

## High Cohesion
Measures how related the responsibilities within a single class are. 
A highly cohesive class does exactly one thing and does it well (SRP). All its methods and fields are tightly related to a single concept. A utility catch-all class (`StringUtils`, `DateUtils` lumped together) has low cohesion.

## Loose Coupling
Measures how much one class knows about another.
Tightly coupled classes instantiate each other directly (using `new`) and depend on concrete implementations. Loose coupling means classes communicate through stable, narrow interfaces (DIP) and dependencies are injected. This makes testing and swapping implementations trivial.
