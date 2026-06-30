---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, jpa, database]
---

# @Modifying and clearAutomatically

## Intuition
Any `@Query` that issues a DML statement (`UPDATE`, `DELETE`) must be annotated with `@Modifying`. Without it, Spring Data refuses to execute it, assuming you accidentally mapped a `SELECT` to a `void` returning method.

## The First-Level Cache Trap
Hibernate maintains a first-level cache (the persistence context) for the duration of a transaction. 
A `@Modifying @Query` bypasses this cache and executes SQL directly against the database. However, Hibernate **does not** automatically invalidate the cached copies of any affected entities. 
If your code later in the *same transaction* tries to `findById` one of those updated entities, Hibernate will serve the **old, stale** version from the cache.

## The Fix
Use `@Modifying(clearAutomatically = true)`. This forces Hibernate to empty the first-level cache immediately after the bulk update runs, ensuring subsequent reads hit the database and get fresh state.
