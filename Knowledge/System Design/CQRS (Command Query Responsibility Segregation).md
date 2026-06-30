---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 8 — Event Sourcing and CQRS"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Event Sourcing"]
tags: [architecture, distributed-systems, cqrs]
---

# CQRS (Command Query Responsibility Segregation)

## Intuition
Event sourcing solves *how to store changes*, but makes reading hard (you can't efficiently query "all shipped orders" if you have to replay everyone's events).
CQRS solves this by splitting the system into two independently optimized sides:

## Write Side (Commands)
Receives commands ("ShipOrder"), validates business rules, and on success emits events ("OrderShipped") to an event store or message broker. Optimized for correctness and consistency.

## Read Side (Queries)
Subscribes to the event stream and continuously updates **projections** (read-optimized, denormalized views such as a SQL table, Elasticsearch index, or cache). Optimized for fast, join-less reads.

## The Trade-off
By decoupling the read and write models, both sides can scale and evolve independently. However, the read side is only **eventually consistent** with the write side, as projections update slightly *after* the event is published.
