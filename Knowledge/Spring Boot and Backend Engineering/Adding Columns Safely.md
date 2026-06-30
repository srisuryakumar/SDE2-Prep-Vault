---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 9 — Flyway"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Zero-Downtime Database Migrations"]
tags: [database, sql, migrations]
---

# Adding Columns Safely

## Intuition
A common mistake in database migrations is adding a `NOT NULL` column to an existing table that already has rows.
`ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(50) NOT NULL;` 
This fails immediately because existing rows don't have a value for the new column and thus violate the constraint.

## The Safe Sequence
1. Add the column as nullable.
2. Backfill the existing rows with a default value.
3. Alter the column to add the `NOT NULL` constraint.

```sql
-- Step 1: Add as nullable
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(50);
-- Step 2: Backfill existing rows
UPDATE orders SET tracking_number = 'UNKNOWN-' || id::text WHERE tracking_number IS NULL;
-- Step 3: Enforce constraint
ALTER TABLE orders ALTER COLUMN tracking_number SET NOT NULL;
```
