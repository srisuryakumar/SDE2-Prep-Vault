---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, jpa, queries]
---

# Spring Data JPA Derived Queries

## Intuition
Spring Data JPA can read a method name and automatically generate the corresponding SQL query. No `@Query` annotation required.

## How it works
The parser breaks the method name at keywords (`findBy`, `And`, `Or`, `After`, `Before`, `LessThan`, `Containing`, `IgnoreCase`, `OrderBy`) and maps each segment to a field on the entity. 

Example: `findByEmail(String email)` becomes `SELECT u FROM User u WHERE u.email = :email`.

**Warning:** The mapping is case-sensitive to the Java field names. `findByEmail` works because the entity field is `email`. If you write `findByEMAIL`, the application will fail to start because it cannot find an `EMAIL` field on the entity.
