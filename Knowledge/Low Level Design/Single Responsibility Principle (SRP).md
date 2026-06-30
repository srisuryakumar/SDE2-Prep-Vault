---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Open-Closed Principle (OCP)"]
tags: [oop, solid, design-principles]
---

# Single Responsibility Principle (SRP)

## Intuition
A class should have only **one reason to change**.
If two different business requirements could force you to modify the same class, that class has too many responsibilities (low cohesion).

## The Classic Violation
A `User` class that handles data storage, validation rules, and persistence (SQL). 
- Changing the DB schema touches the file.
- Changing validation rules touches the file.
- Changing JSON serialization touches the file.
Three reasons to change = three bugs waiting to happen.

## The Fix
Break the single god class into highly cohesive components:
1. `User`: Pure data model (POJO).
2. `UserValidator`: Validation rules.
3. `UserRepository`: Persistence (SQL logic).
4. `UserSerializer`: JSON conversion.
