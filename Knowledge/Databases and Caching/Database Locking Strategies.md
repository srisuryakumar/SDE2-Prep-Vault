---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 2 — Database Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, locking, concurrency]
---

# Database Locking Strategies

## Intuition
When concurrency guarantees provided by isolation levels aren't enough, we use locking strategies: **Pessimistic** (lock before reading) and **Optimistic** (detect conflicts at write time).

## 1. Pessimistic Locking
- **Use when:** Contention is HIGH, write conflicts are frequent (e.g. limited stock, seat booking). Retry cost is high.
- **How:** Lock the row when you read it. Other transactions trying to `SELECT FOR UPDATE` on the same row will wait.
```sql
BEGIN;
SELECT stock_count FROM products WHERE id = 1 FOR UPDATE;
UPDATE products SET stock_count = stock_count - 1 WHERE id = 1;
COMMIT;
```
*(Pro tip: `FOR UPDATE SKIP LOCKED` is a great pattern for concurrent queue workers to grab the next unlocked pending task.)*

## 2. Optimistic Locking
- **Use when:** Contention is LOW, reads are frequent, conflicts are rare. (e.g. editing a user profile).
- **How:** No lock on read. You include a `version` field. On write, verify that the version hasn't changed since you read it. Works well across service boundaries/HTTP calls where you can't hold an active DB lock.
```java
// JPA manages this automatically if @Version is present
// UPDATE ... SET bio = ?, version = version + 1 WHERE id = ? AND version = [read_version]
```
If the version changed, no rows are updated, and the ORM throws an `OptimisticLockException`. The application must retry.
