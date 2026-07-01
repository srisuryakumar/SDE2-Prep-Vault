---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 13 — LLD Interview Strategy"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [lld, interview-strategy, framework]
---

# LLD Interview Strategy

## The 45-Minute Framework
Most LLD interviews run 45–60 minutes. Allocate your time strictly:
- **0–5 mins:** Requirements clarification (Scope, non-functional constraints)
- **5–10 mins:** Entity identification (Extract nouns, define responsibilities)
- **10–20 mins:** Class relationships (UML sketch on whiteboard/paper)
- **20–40 mins:** Core implementation (Code the critical path first)
- **40–45 mins:** Edge cases, Concurrency, Extensibility discussion

## Phase 1: Requirements Clarification
**Never skip this.** It shows seniority. Ask:
- "What are the top 3 operations?"
- "Is consistency more important than availability?"
- Propose simplifications: "I'll assume no authentication — just focus on core logic. Is that OK?"

## Phase 2: Entity Identification
Write nouns, not code. Does this noun have meaningful attributes AND behaviors?
*Bad:* Entry (it's a method).
*Good:* Vehicle, Spot, Ticket.

## Phase 3: Class Relationships (UML Sketch)
Identify the relationships:
1. **Inheritance (IS-A):** `Car extends Vehicle`
2. **Composition (HAS-A):** `ParkingLot HAS-A List<Floor>`
3. **Interfaces (CAN-DO):** `PricingStrategy`
4. **Dependency (USES):** `ParkingLot USES PricingStrategy`

## Phase 4: Core Implementation (Code)
Write the most important code first:
1. The central entity (`ParkingLot`).
2. The core interfaces/hierarchy (`Vehicle`, `PricingStrategy`).
3. The design pattern that solves the key problem.
*Skip:* Getters/Setters, DB repositories, full validation (just mention them verbally).
*Never Skip:* Interface definitions, critical locks/concurrency mechanisms.

## Extensibility: The Killer Phrase
Interviewers love hearing this structure:
> "Currently, I support X. If we need to add Y, I only need to Z, and none of the existing code changes."
*(Demonstrates OCP, DIP, and extensible design).*

## The SDE-2 Difference
An SDE-1 implements a pattern when told. An SDE-2 independently identifies the pattern, spots the exact concurrency race condition, proposes a locking solution, and articulates the trade-offs of their approach.
