---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 9 — Spring Cloud Microservices"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Circuit Breaker Pattern"]
tags: [distributed-systems, microservices, resilience]
---

# Cascading Failures in Microservices

## Intuition
If Service A calls Service B synchronously, and Service B becomes extremely slow (e.g., taking 8 seconds instead of 100ms), Service A's threads will block while waiting. Under load, Service A will exhaust its entire thread pool very quickly. 

Service A will then crash or become unresponsive, even though there was nothing wrong with it. Any service that calls Service A will then experience the same thing. This is a **cascading failure**. 

To prevent this, you must use resilience patterns like Timeouts, Bulkheads (limiting concurrent calls to a specific dependency), and **Circuit Breakers**.
