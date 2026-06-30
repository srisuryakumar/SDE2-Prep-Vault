---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, architecture, api]
---

# REST vs GraphQL vs gRPC

These are the three main protocols for client-server communication:

## REST (Representational State Transfer)
- **Concept:** Resource-based URLs (`/api/orders`), HTTP verbs indicate actions (`GET`, `POST`).
- **Data format:** Usually JSON.
- **Pros:** Universal, simple, easy to cache.
- **Cons:** Prone to over-fetching (getting too much data) and under-fetching (requiring multiple round trips). Ideal for public APIs.

## GraphQL
- **Concept:** Single endpoint (`/graphql`), client sends a query specifying the exact shape of the data needed.
- **Data format:** JSON.
- **Pros:** Solves over/under-fetching, strongly typed schema, great for varied clients (mobile vs web).
- **Cons:** Complex backend implementation (N+1 query problems), harder to cache.

## gRPC (Google Remote Procedure Call)
- **Concept:** Define services and messages in a `.proto` file. Generates type-safe client/server stubs.
- **Data format:** Binary (Protocol Buffers) over HTTP/2.
- **Pros:** Very fast, compact (3-10x smaller than JSON), supports streaming, type-safe.
- **Cons:** Not human-readable, requires tooling, browsers need a proxy (grpc-web). Ideal for internal microservice-to-microservice communication.
