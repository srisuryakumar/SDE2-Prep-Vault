---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Open-Closed Principle (OCP)"]
tags: [oop, solid, design-principles, dependency-injection]
---

# Dependency Inversion Principle (DIP)

## Intuition
1. High-level modules should not depend on low-level modules. Both should depend on **abstractions**.
2. Abstractions should not depend on details. Details should depend on abstractions.

## The Classic Violation
An `OrderService` (high-level policy) instantiating a `MySQLOrderRepository` (low-level detail) directly via `new MySQLOrderRepository()`.
Switching the database to PostgreSQL now requires rewriting the core `OrderService`.

## The Fix
1. Define an `OrderRepository` interface (the abstraction).
2. The `OrderService` depends *only* on the interface.
3. The concrete implementation (`PostgreSQLOrderRepository`) is injected into the service (e.g., via constructor injection / Spring `@Autowired`). 
This flips the dependency direction: the low-level DB code now depends on the high-level interface contract.
