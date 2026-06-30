---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, architecture, microservices]
---

# Microservices vs Monoliths

## Monolith
An application where all code runs in a single process (e.g., one huge Spring Boot JVM). 
- **Pros:** Simple to develop, deploy, and debug. Can use simple in-memory function calls and ACID database transactions across all modules.
- **Cons:** Hard to scale specific components. A bug in one module can crash the whole app. High deployment risk. Teams step on each other's toes in the same codebase.

## Microservices
Decomposes the monolith into separate services, each running in its own process (container), owning its own database, and communicating over the network (HTTP, gRPC, Kafka).
- **Pros:** Independent deployments. Independent scaling. Teams can use different technologies. Blasts radius of bugs is isolated.
- **Cons:** High operational complexity (Kubernetes, CI/CD). Network overhead/latency between calls. Difficult distributed debugging (requires tracing). No cross-service ACID transactions (requires sagas/eventual consistency).
