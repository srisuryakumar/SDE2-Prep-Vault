---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 3 — Structural Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Facade Pattern"]
tags: [lld, design-patterns, structural]
---

# Adapter Pattern

## Intuition
You have a system that expects an interface of type `A`. You have a third-party library or legacy code that provides type `B`. You can't modify either. You need a bridge.

## The Solution
Create an Adapter class that implements interface `A` and wraps an instance of `B`.
When the client calls a method on `A`, the adapter translates the parameters and calls the corresponding method on `B`, returning the translated result.

**Adapter vs Bridge:**
- Adapter: Fixes an incompatibility that *already exists* (retrospective).
- Bridge: Separates abstraction from implementation *before* they are developed (proactive).
