---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, jpa, performance]
---

# @BatchSize (Fixing N+1)

## Intuition
`@BatchSize` doesn't eliminate extra queries entirely, but it drastically reduces the *number* of them by batching proxy-initializations.

## Mechanism
If you load 100 users and access their lazy `orders` collections, normally you get 101 queries (1 for users + 100 for orders).
If you add `@BatchSize(size = 25)` to the `orders` collection:
```java
@OneToMany(mappedBy = "user", fetch = FetchType.LAZY)
@BatchSize(size = 25)
private List<Order> orders;
```
Hibernate will group the lazy fetches into batches of 25 using a SQL `IN` clause: `WHERE user_id IN (1, 2, ..., 25)`.
Result: 5 queries instead of 101.

## When to use it
- When `JOIN FETCH` would produce a cartesian explosion (e.g. fetching two independent `@OneToMany` collections at the same time).
- When the association is lazily navigated deep inside existing code scattered across the codebase, and rewriting all queries is impractical.
- Not a first choice for new endpoints (where `JOIN FETCH` or `@EntityGraph` are better since they result in exactly 1 query).
