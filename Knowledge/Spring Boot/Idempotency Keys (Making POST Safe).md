---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 2 — REST API Design Principles"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [rest, idempotency, distributed-systems]
---

# Idempotency Keys (Making POST Safe)

## Intuition
`POST` creates a new resource and is NOT idempotent by default. If a client sends a `POST`, the server processes it, but the response is lost due to a network timeout, the client will retry. Without idempotency, this results in a duplicate creation (e.g. charging a user twice).

## The Fix: Idempotency-Key
The client supplies an `Idempotency-Key` header.
```
POST /v1/orders
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7
```
**The Contract:**
1. The client generates this key **once** per logical operation (usually a UUID).
2. The client sends the exact same key on retries.
3. The server checks if it has seen this key before.
4. If it's a new key, process it and store the result alongside the key.
5. If it's an existing key, do NOT reprocess it. Simply return the stored result.

## Concurrency 
A robust implementation relies on a database-level unique constraint on the key column. If two requests with the same key hit the server at the exact same time (a race condition), the DB constraint violation safely prevents the duplicate.
