---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [oop, design-principles]
---

# DRY, KISS, and YAGNI

## Intuition
These three principles are simpler than SOLID but equally important in day-to-day coding.

## DRY (Don't Repeat Yourself)
Every piece of knowledge must have a single, authoritative representation.
It's about **no duplicate knowledge**, not just "no duplicate code". Two pieces of code can look similar but represent different business concepts—forcing them into one function is the wrong DRY. However, hardcoding a tax rate across three different files is a severe DRY violation.

## KISS (Keep It Simple, Stupid)
Complexity is not a sign of intelligence. The most dangerous code is the "clever" code that only the author understands.
**The Test:** Could a junior engineer understand this in 30 seconds without asking questions? If no, ask whether the complexity is truly necessary.

## YAGNI (You Aren't Gonna Need It)
Do not add functionality until it is strictly necessary.
Speculative generality creates dead code. If you hear yourself saying "we might need this later", delete it. Build what is needed now and rely on good design (like SOLID) to make the code extensible when actual requirements arrive.
