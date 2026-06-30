---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 9 — Spring Cloud Microservices"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Cascading Failures in Microservices", "Retry vs Circuit Breaker"]
tags: [distributed-systems, resilience, microservices]
---

# Circuit Breaker Pattern

## Intuition
A Circuit Breaker prevents cascading failures by failing fast when a downstream service is struggling, rather than piling on more load and blocking threads waiting for timeouts.

## The State Machine
- **CLOSED:** Normal operation. Calls pass through to the downstream service. The breaker monitors the failure rate.
- **OPEN:** The failure rate crossed the threshold. The breaker **stops calling the downstream service entirely** and fails fast instantly (or executes a fallback method). This protects the caller's threads and gives the struggling service room to recover.
- **HALF_OPEN:** After a configured wait duration, the breaker allows a small number of *probe* calls through. If they succeed, it closes. If they fail, it reopens.
