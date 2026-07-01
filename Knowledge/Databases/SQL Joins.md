---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 1 — SQL Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [sql, joins, databases]
---

# SQL Joins

## Intuition
Joins reconstruct related information split across tables. Think of two tables as two circles in a Venn diagram — the join type determines which part of the diagram appears in your result.

## Join Types
- **INNER JOIN:** Only rows that have a match in BOTH tables. Use when you only want records with a corresponding record on both sides.
- **LEFT JOIN:** ALL rows from the left table, matched rows from the right table. The right-side columns are `NULL` when no match exists. Use when you want all left-side records regardless of whether a match exists.
- **RIGHT JOIN:** ALL rows from the right table, matched from left. Rarely used—rewrite as a `LEFT JOIN` with tables swapped for clarity.
- **FULL OUTER JOIN:** ALL rows from BOTH tables, `NULL`s for non-matching sides.
- **CROSS JOIN:** Cartesian product (every row from A paired with every row from B).
- **SELF JOIN:** A table joined with itself (e.g., employee and their manager).

## The NULL-Filter Trick
A `LEFT JOIN` coupled with `WHERE right.id IS NULL` is an extremely common pattern to find rows that have **NO** match on the right side.
```sql
-- Find users who have NEVER placed an order
SELECT u.username
FROM   users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE  o.id IS NULL;
```
