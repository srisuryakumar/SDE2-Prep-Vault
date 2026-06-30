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

# @EntityGraph (Fixing N+1)

## Intuition
`@EntityGraph` allows you to eagerly fetch associations without writing JPQL string joins manually. It's the perfect fit for Spring Data **derived query methods**.

```java
@EntityGraph(attributePaths = {"items", "items.product"})
Page<Order> findByUserIdAndStatus(Long userId, OrderStatus status, Pageable pageable);
```

## How it works
It generates the same `LEFT OUTER JOIN` SQL as a `JOIN FETCH`. 

## Pagination Safety
Unlike a raw `JOIN FETCH` which memory-crashes when combined with `Pageable`, Spring Data handles `@EntityGraph` with `Page<T>` perfectly. It automatically executes the two-query pattern (one for IDs, one for the joined data) without you having to write it manually.
