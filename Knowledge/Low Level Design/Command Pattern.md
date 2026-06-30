---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 4 — Behavioral Patterns"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Strategy Pattern"]
tags: [lld, design-patterns, behavioral]
---

# Command Pattern

## Intuition
You want to encapsulate a request (an action) as an object so that you can store it, pass it around, put it in a queue, log it, or undo it.

## The Solution
1. Define a `Command` interface with `execute()` and `undo()`.
2. Concrete commands (e.g., `InsertTextCommand`) hold a reference to the target object (the Receiver) and all parameters necessary to perform the action.
3. An Invoker executes the commands and maintains history stacks for Undo/Redo.

**Why encapsulate?**
It separates *what* to do from *when* and *how* to do it.

**Command vs Strategy:**
- Strategy defines *how* to do something (a general algorithm).
- Command defines *what* to do (a specific operation on a specific receiver with specific parameters).
