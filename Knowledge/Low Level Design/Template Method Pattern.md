---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 4 — Behavioral Patterns"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, behavioral]
---

# Template Method Pattern

## Intuition
You have an algorithm where the skeleton (the sequence of steps) is fixed, but certain steps vary between implementations.

## The Solution
1. Define an abstract base class with a `final` method (the Template Method) that dictates the algorithm's structure (e.g., `fetch`, `process`, `format`, `write`).
2. Provide default implementations for shared steps.
3. Define `abstract` methods for the steps that must vary (forcing subclasses to implement them).
4. Provide empty or default "hook" methods that subclasses *may* override if they want to customize optional behavior.

**Real-world Example:**
- Spring's `JdbcTemplate`: It handles acquiring the connection, preparing the statement, executing, and cleaning up (the skeleton). You provide the SQL and the row mapping logic (the abstract steps).
