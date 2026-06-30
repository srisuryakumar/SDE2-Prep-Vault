---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, architecture, microservices, databases]
---

# Database-per-Service Pattern

A critical rule in microservices architecture: **Each microservice must own its own database.**

No other service is allowed to directly query or modify that database. If `UserService` needs order data, it must call the `OrderService` API; it cannot run a SQL query against the `orders` database.

## Why this matters
- **Decoupling:** `OrderService` can refactor its database schema, migrate from PostgreSQL to MongoDB, or change data types without breaking `UserService`.
- **Fault isolation:** If `OrderService`'s database goes down, `UserService` remains unaffected (assuming it fails gracefully when calling the API).
- **Technology Choice:** Each service can use the best database for its specific workload (e.g., a relational DB for transactions, Redis for caching, MongoDB for product catalogs).

This pattern enforces strict boundaries, preventing the "distributed monolith" anti-pattern where services are coupled at the database level.
