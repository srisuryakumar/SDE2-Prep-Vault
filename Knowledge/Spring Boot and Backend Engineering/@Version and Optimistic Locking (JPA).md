---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, jpa, concurrency, database]
---

# @Version and Optimistic Locking (JPA)

## Intuition
`@Version` is a single column (`Long`, `int`, or `Timestamp`) that Hibernate manages to prevent **lost updates** (two concurrent transactions reading a row, and the second write silently overwriting the first).

## The Mechanism
1. Transaction A reads an `Inventory` row: `quantity = 5, version = 12`.
2. Transaction A computes a new value (quantity = 4) and issues an update.
3. Hibernate generates the SQL: 
   `UPDATE inventory SET quantity = 4, version = 13 WHERE id = 7 AND version = 12`.
4. If Transaction B already updated the row (version is now 13), Transaction A's `WHERE` clause matches **0 rows**.
5. Hibernate checks the affected-row count. Because it is 0 instead of 1, it knows someone else got there first. It throws an `OptimisticLockException` (which Spring translates to `ObjectOptimisticLockingFailureException`).
6. The global exception handler catches this and returns a `409 Conflict`.

## Optimistic vs Pessimistic Locking
- **Optimistic (`@Version`):** Best for low contention (conflicts are rare). No database row lock is ever held, meaning high throughput and zero deadlock risk. You just have to handle the occasional exception and maybe retry.
- **Pessimistic (`SELECT ... FOR UPDATE`):** Best for high contention (concert tickets, limited stock). It takes a real DB lock, forcing other transactions to wait. Reduced throughput and carries deadlock risk, but guaranteed to succeed if the lock is acquired.
