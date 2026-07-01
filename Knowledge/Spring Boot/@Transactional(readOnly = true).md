---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, transactions, performance]
---

# @Transactional(readOnly = true)

## Intuition
Read-only transactions are a performance optimization hint, not a strict security constraint.

## What it does
1. **JDBC Optimization:** Spring passes the hint to the JDBC driver, which might route the query to a read-replica database.
2. **Hibernate Optimization:** Hibernate **skips "dirty checking"** at the end of the transaction. Normally, Hibernate compares every loaded entity against its original snapshot to see if it needs to generate an `UPDATE` statement. Skipping this check is significantly faster, especially when loading many entities.
3. **Silent Writes:** If you accidentally modify an entity inside a `readOnly = true` transaction, Hibernate will simply not flush those changes. They silently disappear.

Apply it to every service method that only reads data and doesn't need to write.
