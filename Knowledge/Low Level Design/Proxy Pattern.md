---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 3 — Structural Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Decorator Pattern"]
tags: [lld, design-patterns, structural, spring]
---

# Proxy Pattern

## Intuition
A Proxy controls access to another object. It implements the same interface as the real object and intercepts method calls to add a layer of control.

## The Three Main Types
1. **Virtual Proxy (Lazy Loading):** Delays the creation of a massive, expensive object until its methods are actually called.
2. **Protection Proxy (Access Control):** Checks permissions/roles before delegating the call to the real object.
3. **Remote Proxy:** Hides network communication (e.g., gRPC stubs), making a remote object look like a local one.

## Real-World Example: Spring `@Transactional`
When you annotate a service method with `@Transactional`, Spring doesn't execute your class directly. It creates a Proxy subclass. The proxy intercepts the call, begins a database transaction, calls your actual method, and then commits (or rolls back on exception).

**Proxy vs Decorator:**
Both wrap objects. However, a Decorator *adds* new behavior visible to the client (like adding milk to coffee), whereas a Proxy *controls access* transparently to the client (like caching an expensive API call).
