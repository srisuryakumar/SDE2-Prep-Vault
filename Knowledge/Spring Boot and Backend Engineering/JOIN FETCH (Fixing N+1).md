---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, jpa, sql, performance]
---

# JOIN FETCH (Fixing N+1)

## Intuition
The most direct fix for the N+1 problem. It tells Hibernate to load the association in the *same* SQL query as the parent using a `LEFT OUTER JOIN`.

```java
@Query("""
    SELECT DISTINCT o FROM Order o
    LEFT JOIN FETCH o.items i
    LEFT JOIN FETCH i.product
    WHERE o.id = :orderId
""")
Optional<Order> findByIdWithItemsAndProducts(@Param("orderId") Long orderId);
```
**One query** for the order, its items, and each item's product, regardless of how many items the order has.
*Note: `DISTINCT` deduplicates the parent objects in Java memory, since the SQL join produces duplicate rows for the parent.*

## The JOIN FETCH + Pagination Trap
If you combine `JOIN FETCH` on a collection (`@OneToMany`) with `Pageable` (`LIMIT`/`OFFSET`), Hibernate warns you:
`HHH90003004: firstResult/maxResults specified with collection fetch; applying in memory`
Because the SQL join returns multiple rows per order, applying `LIMIT 20` would cut off an order's items halfway. So Hibernate loads *every single row* matching the `WHERE` clause into Java memory, and paginates in memory. **This will crash your server at scale.**

**The Fix:** Use two queries.
1. Paginated query to fetch ONLY the IDs: `SELECT o.id FROM orders o ... LIMIT 20`.
2. A second query to `JOIN FETCH` the associations for exactly those IDs using an `IN` clause.
