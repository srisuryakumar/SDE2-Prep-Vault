---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 1 — SQL Fundamentals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [sql, set-operations, union, intersect]
---

# SQL Set Operations

## Intuition
Set operations combine results from two `SELECT` statements. Both sides must have the same number of columns and compatible data types.

## Operations
- **`UNION`**: Combines results and **deduplicates**. This requires a sort step, making it slower.
- **`UNION ALL`**: Combines results and **keeps duplicates**. This is much faster. Use this whenever duplicates are impossible or acceptable.
- **`INTERSECT`**: Returns only rows appearing in BOTH result sets.
- **`EXCEPT`**: Returns rows in the first set that do NOT appear in the second set. (Same logic as `LEFT JOIN / NOT EXISTS`).

## Examples
```sql
-- UNION ALL: Fast combination
SELECT username FROM users WHERE is_active = TRUE
UNION ALL
SELECT username FROM users WHERE id IN (SELECT user_id FROM orders);

-- EXCEPT: Find users who have NEVER placed an order
SELECT username FROM users
EXCEPT
SELECT username FROM users WHERE id IN (SELECT user_id FROM orders);
```
