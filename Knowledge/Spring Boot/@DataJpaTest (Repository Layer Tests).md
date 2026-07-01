---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 6 — Testing"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [testing, spring, database, jpa]
---

# @DataJpaTest (Repository Layer Tests)

## Intuition
`@DataJpaTest` is a Spring Boot slice test. It loads *only* the JPA infrastructure: repositories, `EntityManager`, datasource, and Hibernate. It does not load the web layer or services.

## How it works
- By default, it replaces your real database with an in-memory H2 database (fast, zero setup).
- It runs each test inside a transaction and rolls it back at the end (so tests don't pollute each other's data).
- `TestEntityManager` is provided to allow easy `persistAndFlush()` operations to set up test data.

## Limitations
H2 is not PostgreSQL/MySQL. If you use database-specific SQL features (e.g. `ILIKE`, `ON CONFLICT`, `FOR UPDATE SKIP LOCKED`), `@DataJpaTest` with H2 will fail. In those cases, you should use Testcontainers.
