---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 2 — Creational Patterns"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, creational]
---

# Prototype Pattern

## Intuition
Some objects are very expensive to create from scratch (e.g., they require database queries, HTTP calls, or complex initialization). The Prototype pattern avoids this cost by **cloning** an existing, pre-configured instance.

## Shallow vs Deep Copy
- **Shallow Copy:** Copies primitives and *references* to objects. If the original prototype contains a list, both the original and the clone point to the exact same list. Modifying one affects the other (a common bug).
- **Deep Copy:** Creates entirely new copies of all nested objects (e.g., `new ArrayList<>(this.sections)`). The clone is completely independent.

## Usage
Commonly implemented using a Registry. You register a "Base Invoice" template. When you need a new invoice, you retrieve the template from the registry and call `.copy()`, giving you a fresh, independent instance instantly.
