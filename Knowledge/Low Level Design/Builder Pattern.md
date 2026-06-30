---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 2 — Creational Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, creational]
---

# Builder Pattern

## Intuition
When constructing complex objects with many optional fields, a "Telescoping Constructor" (a constructor with 10+ arguments) becomes unreadable and prone to parameter-swapping bugs.

## The Solution
Use a nested static `Builder` class.
1. The `Builder` collects fields step-by-step using method chaining (`.city("Bangalore").age(28)`).
2. Required fields are passed in the `Builder`'s constructor.
3. The `build()` method performs cross-field validation (e.g., "State is required if City is provided") and then returns the final, **immutable** object.

## Lombok `@Builder`
In Spring Boot, the `@Builder` annotation auto-generates the static builder class, the setter chains, and the `build()` method, eliminating all boilerplate.

**Why Builder over POJO Setters?**
Builder ensures immutability (the object has no setters once built) and allows for atomic validation of the entire object state before it is returned to the caller.
