---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 8 — Event Sourcing and CQRS"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["CQRS (Command Query Responsibility Segregation)"]
tags: [architecture, distributed-systems, event-sourcing]
---

# Event Sourcing

## Intuition
Traditional systems store the **current state** (e.g., an `accounts` table with a `balance` column). Every update overwrites the previous value, destroying the history of *how* you arrived at that state.

**Event Sourcing** inverts this: you store **every event that ever changed the state** (e.g., `AccountOpened`, `Deposited`, `Withdrawn`) in an immutable, append-only log. Current state is not stored; it is *derived* by replaying those events from the beginning.

## Benefits
- **Complete audit trail:** You get a perfect history of all changes for free.
- **Time travel:** You can reconstruct the state as of any point in time by replaying events up to that timestamp.
- **Debugging:** If you find a bug in how state is computed, you fix the logic and re-replay the original, untouched events to compute the correct state.

## Snapshots
An entity with 100,000 events shouldn't be replayed from event #1 every time you load it. Periodically persist a **snapshot** (the computed state at event #N) so you only need to replay events *since* the last snapshot.
