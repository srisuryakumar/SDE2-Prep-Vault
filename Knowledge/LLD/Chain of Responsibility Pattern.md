---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 4 — Behavioral Patterns"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, behavioral]
---

# Chain of Responsibility Pattern

## Intuition
You have a request that could be handled by one of many handlers. Instead of a massive `if-else` block evaluating which handler should process the request, pass the request along a chain of handlers.

## The Solution
1. Define a `Handler` interface with a `handle()` method and a reference to the `next` handler.
2. Concrete handlers either process the request (if they can) or pass it to `next.handle()`.
3. Link the handlers together at runtime (`L1.setNext(Billing).setNext(L2)`).

**Real-world Examples:**
- HTTP Filter chains (Spring `FilterChain`, Servlet Filters).
- Middleware pipelines (Auth Check → Rate Limit → CORS).
- Logging frameworks (DEBUG → INFO → WARN).
