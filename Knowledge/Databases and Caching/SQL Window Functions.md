---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 1 — SQL Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [sql, window-functions, over, partition-by]
---

# SQL Window Functions

## Intuition
Window functions compute a value for each row using a *window* of related rows. 
Unlike `GROUP BY`, they **do not collapse rows** — every individual row remains in the result set with an additional computed column.

**Syntax:** `FUNCTION() OVER (PARTITION BY col ORDER BY col [frame])`
- `PARTITION BY`: Divide rows into independent groups.
- `ORDER BY`: Sort rows within each partition.
- `[frame]`: Which rows in the partition count (e.g., `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).

## Common Functions

### ROW_NUMBER, RANK, DENSE_RANK
- `ROW_NUMBER()`: Unique sequential number (1, 2, 3) regardless of ties. (Non-deterministic ordering among tied rows without a tiebreaker).
- `RANK()`: Skips the next rank(s) to account for ties (1, 1, 3).
- `DENSE_RANK()`: Does not skip ranks (1, 1, 2).

**Top-N Per Group (Standard Technique):**
"Get the 2 most expensive products per category"
```sql
SELECT name, price, category
FROM (
    SELECT name, price, category,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
    FROM products
) AS ranked
WHERE rn <= 2;
```

### LAG and LEAD
Access the previous or next row's value within a partition.
- `LAG()` = Look back 1 row. First row is `NULL`.
- `LEAD()` = Look ahead 1 row. Last row is `NULL`.
```sql
SELECT o.id,
       o.total_amount,
       LAG(o.total_amount) OVER (PARTITION BY o.user_id ORDER BY o.created_at) AS previous_amount
FROM orders o;
```

### Running Totals
```sql
SELECT o.id, o.user_id, o.total_amount,
       SUM(o.total_amount) OVER (
           PARTITION BY o.user_id
           ORDER BY o.created_at
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM orders o;
```
