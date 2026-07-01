---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 9 — Flyway"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [database, postgresql, performance, migrations]
---

# Concurrent Index Creation (PostgreSQL)

## Intuition
Creating an index using `CREATE INDEX idx_name ON table_name(col)` takes an exclusive lock on the table. For a large table, this can take minutes, during which all reads and writes are blocked (causing a massive outage).

## The Solution
Use `CREATE INDEX CONCURRENTLY`. This builds the index in the background using lighter locks, allowing reads and writes to continue. The trade-off is it takes longer to build and cannot be run inside a transaction block.

## Flyway Integration
Because Flyway wraps migrations in a transaction by default, a concurrent index creation will fail. You must tell Flyway to disable transactions for that specific migration file using a special comment:

```sql
-- V4__add_product_search_index.sql
-- flyway:executeInTransaction=false
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_name ON products(name);
```
