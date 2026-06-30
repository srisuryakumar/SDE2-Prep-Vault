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

# Microservice Communication (Synchronous vs Asynchronous)

## Synchronous Communication (HTTP / gRPC)
Service A sends a request to Service B and waits for the response before continuing.
- **When to use:** When you need the response immediately to make a decision (e.g., checking if a payment succeeded before confirming an order).
- **Tradeoffs:** Tightly couples services. If Service B is down or slow, Service A hangs or fails. This is mitigated by timeouts and Circuit Breakers (like Resilience4j).

## Asynchronous Communication (Message Queues like Kafka / RabbitMQ)
Service A publishes an event (e.g., "OrderCreated") to a message broker and immediately returns a response to the user. Service B reads and processes the event later, independently.
- **When to use:** For side effects that do not need to block the user's request (e.g., sending an email, updating analytics, triggering a background workflow).
- **Tradeoffs:** Better availability and lower latency for the initial request. However, it introduces **eventual consistency** (the email is sent seconds later) and makes debugging harder (requires distributed tracing like Zipkin/Jaeger).
