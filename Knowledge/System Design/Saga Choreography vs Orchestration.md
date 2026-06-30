---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 7 — Distributed Transactions"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["The Saga Pattern"]
tags: [distributed-systems, transactions, microservices, architecture]
---

# Saga Choreography vs Orchestration

## Intuition
There are two ways to coordinate the steps (and compensations) of a Saga.

## Choreography (Event-Driven)
No central coordinator. Each service publishes an event (e.g., to Kafka) when it finishes its step, and the next service(s) react to that event.
- **Pros:** Fully decoupled. Services don't need to know about each other, just the events.
- **Cons:** The overall business logic is implicit and scattered across multiple codebases. Hard to debug "why did this order fail" without distributed tracing. Best for simple flows with few steps.

## Orchestration (Command-Driven)
A central "Orchestrator" service explicitly tells each service what to do, tracks the state of the saga in a database, and explicitly triggers compensations on failure.
- **Pros:** The entire business flow is visible in one place. Easy to read, debug, and modify.
- **Cons:** Introduces a single point of failure/bottleneck (the orchestrator itself must be highly available and durable). Best for complex flows with many steps or conditional branches.
