---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, jpa, jpql, sql]
---

# @Query (JPQL vs Native SQL)

## Intuition
When a derived query name becomes too complex, or you need to use `JOIN FETCH` to avoid N+1 problems, you write the query explicitly using `@Query`.

## JPQL (Jakarta Persistence Query Language)
Operates on **entity objects and field names**, not database tables and columns.
```java
@Query("SELECT o FROM Order o WHERE o.user.id = :userId")
List<Order> findByUserId(@Param("userId") Long userId);
```
- **Pros:** Database-agnostic. Survives table renames. Syntax is validated at startup against the entity model. Results are merged into Hibernate's first-level cache.
- **Cons:** Cannot use database-specific features (e.g. Postgres `ILIKE`, window functions).

## Native SQL
Operates directly on the underlying database.
```java
@Query(value = "SELECT * FROM orders WHERE user_id = :userId", nativeQuery = true)
List<Order> findByUserIdNative(@Param("userId") Long userId);
```
- **Pros:** Can use any database-specific SQL feature.
- **Cons:** Bypasses JPQL startup validation (fails at runtime instead). Bypasses the Hibernate entity cache. Breaks if table/column names change.
