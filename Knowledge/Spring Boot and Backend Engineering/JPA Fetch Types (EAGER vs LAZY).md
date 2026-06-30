---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, jpa, database, performance]
---

# JPA Fetch Types (EAGER vs LAZY)

## Intuition
Every association has a fetch type: `EAGER` (load it immediately with a JOIN) or `LAZY` (don't query the database for it until something actually calls the getter).

## The Defaults (The Trap)
| Association | Default Fetch Type |
| :--- | :--- |
| `@OneToMany` | `LAZY` |
| `@ManyToMany` | `LAZY` |
| `@ManyToOne` | **`EAGER`** |
| `@OneToOne` | **`EAGER`** |

Because `*-to-one` relationships default to `EAGER`, loading a list of `OrderItem`s will instantly and silently trigger additional queries to load every associated `Order` and `Product` (the N+1 problem), even if you never needed them.
**House Rule:** ALWAYS explicitly declare `fetch = FetchType.LAZY` on every single `@ManyToOne` and `@OneToOne`. Only fetch eagerly when a specific query path needs it (using `JOIN FETCH` or `@EntityGraph`).

## The LazyInitializationException
If you mark an association as `LAZY`, Hibernate backs it with a proxy. The proxy can only fetch data while the originating Hibernate `Session` is still open. 
If you try to access a lazy field (e.g. `order.getItems().size()`) inside a controller, *after* the `@Transactional` service method has returned and closed the session, you get a `LazyInitializationException`.
**The fix is NEVER "make it eager".** The fix is to fetch exactly what you need *inside* the transaction using a `JOIN FETCH`, so the data is already loaded when the transaction closes.
