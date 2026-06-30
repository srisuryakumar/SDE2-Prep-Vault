---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, jpa, pagination]
---

# Pagination (Page vs Slice)

## Intuition
Adding a `Pageable` parameter to a repository method tells Spring Data to handle pagination automatically (e.g. `LIMIT` and `OFFSET`).

```java
Page<Order> findByUserId(Long userId, Pageable pageable);
```

## Page<T>
Carries the list of items for the current page, PLUS metadata like `getTotalElements()` and `getTotalPages()`.
- **The Catch:** Calculating the total elements requires Spring Data to execute a separate `SELECT COUNT(*)` query alongside your main query. On tables with hundreds of millions of rows, this count query can be extremely slow. Maps to numbered pagination UIs.

## Slice<T>
Carries the list of items, but only knows `hasNext()`. It does NOT know the total count or total pages.
- **Why it's faster:** Instead of a `COUNT(*)`, it just asks the database for `LIMIT (size + 1)`. If the extra item exists, it knows there is a next page. Maps perfectly to "infinite scroll" or "load more" UIs, saving a very expensive query on massive tables.
