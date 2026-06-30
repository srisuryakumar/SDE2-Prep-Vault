---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 1 — SQL Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [sql, aggregation, group-by, having]
---

# SQL Aggregation and Execution Order

## Intuition
Aggregation collapses multiple rows into a summary value. `GROUP BY` creates groups, then aggregate functions (`COUNT, SUM, AVG, MIN, MAX`) run *once per group*.

## WHERE vs. HAVING
The most common confusion in SQL interviews is `WHERE` vs `HAVING`.
- **`WHERE`** filters rows *before* grouping. It cannot reference aggregate functions.
- **`HAVING`** filters groups *after* aggregation. It can reference aggregate functions.

```sql
SELECT   u.username,
         SUM(oi.quantity * oi.unit_price) AS revenue
FROM     users u
JOIN     orders     o  ON o.user_id    = u.id
JOIN     order_items oi ON oi.order_id = o.id
WHERE    o.status = 'DELIVERED'                          -- row filter (before grouping)
GROUP BY u.id, u.username
HAVING   SUM(oi.quantity * oi.unit_price) > 50000        -- group filter (after aggregation)
ORDER BY revenue DESC;
```

## Execution Order
Memorize this for interviews:
1. `FROM / JOIN` (Identify all source rows)
2. `WHERE` (Filter individual rows)
3. `GROUP BY` (Form groups)
4. `Aggregate fns` (Compute within each group)
5. `HAVING` (Filter groups)
6. `SELECT` (Choose/compute output columns, define aliases)
7. `DISTINCT` (Remove duplicates)
8. `ORDER BY` (Sort; can use SELECT aliases here)
9. `LIMIT / OFFSET` (Truncate result)

**Interview Trap:** Can you use a `SELECT` alias in a `WHERE` clause?
**No.** `WHERE` executes at step 2, before `SELECT` (step 6) defines the alias. You *can* use it in `ORDER BY`. Some dialects allow it in `HAVING`, but standard SQL evaluates `HAVING` at step 5.
