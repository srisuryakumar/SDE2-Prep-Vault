---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 4 — Behavioral Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Strategy Pattern"]
tags: [lld, design-patterns, behavioral]
---

# State Pattern

## Intuition
When an object's behavior changes drastically based on its internal state, and you see massive `if (state == X)` statements inside every method, use the State pattern.

## The Solution
1. Create a `State` interface defining all possible actions (e.g., `insertMoney()`, `selectProduct()`).
2. Create concrete classes for each state (`IdleState`, `DispensingState`). Each class only contains the behavior relevant to that specific state.
3. The Context object (`VendingMachine`) holds a reference to the current `State` object and delegates all method calls to it.
4. The State objects themselves are responsible for triggering state transitions (`machine.setState(new IdleState())`).

**Real-world Examples:**
- Vending Machines.
- E-commerce Order Lifecycles (Pending → Paid → Shipped → Delivered).
- Document Workflows (Draft → Review → Published).
