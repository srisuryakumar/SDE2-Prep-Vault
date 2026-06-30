---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [architecture, design-patterns]
---

# DTOs vs Entities

## Intuition
- **Entities** represent the persistence model (the database schema).
- **DTOs (Data Transfer Objects)** represent the API contract (the JSON request/response shape).

## Why separate them?
1. **Schema Evolution:** You can change your database schema without breaking API clients.
2. **Security:** It prevents accidentally leaking internal or sensitive fields (like a hashed `password` or an internal `version` column) by simply omitting them from the DTO. You don't have to remember to add `@JsonIgnore` to every sensitive field on the entity.
3. **Validation:** Request DTOs can have validation annotations (`@NotNull`, `@Size`) specific to a particular use-case (like `CreateOrderRequest`) that don't apply universally to the database entity.
