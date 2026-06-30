---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, transactions]
---

# Transaction Propagation

## Intuition
Propagation controls what happens when a `@Transactional` method is called while a transaction is *already active* on the current thread.

## Key Propagation Types
- **`REQUIRED` (default):** Join the existing transaction if there is one. If not, create a new one. Used for 90% of service methods. ("This work belongs to the same unit of work as whatever called me").
- **`REQUIRES_NEW`:** ALWAYS create a brand-new, independent transaction, suspending the caller's transaction if one exists. Changes in the inner transaction commit even if the outer transaction later rolls back. Used for audit logs, idempotency records, or sending notifications (where failure shouldn't roll back the main business logic).
- **`MANDATORY`:** A transaction MUST already be active. Throws an exception if not.
- **`NESTED`:** Creates a *savepoint* within the existing transaction. If the nested method rolls back, it only rolls back to the savepoint. It does NOT survive if the outer transaction rolls back (unlike `REQUIRES_NEW`).
