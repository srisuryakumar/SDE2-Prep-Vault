---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 9 — Spring Cloud Microservices"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Circuit Breaker Pattern"]
tags: [distributed-systems, resilience]
---

# Retry vs Circuit Breaker

## Intuition
Both are resilience patterns, but they solve different problems.

- **Retry** handles *transient* failures (a dropped packet, a momentary network blip). It assumes the problem will resolve in milliseconds.
- **Circuit Breaker** handles *sustained* failures. If a service is truly overwhelmed, retrying will just hammer it with more load, making the problem worse. A circuit breaker stops calls entirely.

**Combining them:** They are usually used together. The retry wraps the individual call to handle blips. If retries continually fail and the failure rate climbs, the circuit breaker opens and cuts off all traffic (including retries) to give the downstream service a chance to recover.
