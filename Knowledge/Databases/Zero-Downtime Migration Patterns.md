---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 4 — Database Migrations with Flyway"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, migration, zero-downtime]
---

# Zero-Downtime Migration Patterns

## Intuition
Directly altering a large production table (e.g., `ALTER TABLE ADD COLUMN NOT NULL DEFAULT`) rewrites every row while holding an exclusive lock. This can cause minutes of full downtime. Zero-downtime migrations avoid holding exclusive locks on large tables for long periods.

## Pattern 1: Adding a NOT NULL Column
*Never do this in one step.* Use 3 deployments:
1. **Migration V10:** Add the column as nullable (instant, no row rewriting).
   - *Deploy App v2:* App writes to this column on all new inserts, reads with a fallback.
2. **Migration V11:** Backfill existing rows in batches.
   ```sql
   -- Run inside a loop with a batch_size and brief pauses (pg_sleep)
   UPDATE orders SET region = 'INDIA' WHERE region IS NULL AND ctid IN (... LIMIT batch_size)
   ```
3. **Migration V12:** Add the `NOT NULL` constraint safely now that all rows have a value.

## Pattern 2: Renaming a Column
*Never rename directly (breaks running code).* Use 3 deployments:
1. **Migration V20:** Add the new column.
   - *Deploy App v2:* Writes to BOTH old and new columns. Reads from new (with fallback).
2. **Migration V21:** Backfill the new column from the old column, then set it `NOT NULL`.
   - *Deploy App v3:* Reads/writes exclusively to the new column.
3. **Migration V22:** Drop the old column.

## Pattern 3: Adding an Index Without Locking
*Never run `CREATE INDEX` on a live production table.* It locks the table for the duration of the build.
Use **`CONCURRENTLY`**:
```sql
CREATE INDEX CONCURRENTLY idx_orders_created_at ON orders(created_at);
```
This builds the index without holding a table lock, allowing reads and writes to continue. (Note: `CONCURRENTLY` cannot be run inside a transaction block).
