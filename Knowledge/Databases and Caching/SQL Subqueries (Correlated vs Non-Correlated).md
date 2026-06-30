---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 1 — SQL Fundamentals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [sql, subqueries, exists]
---

# SQL Subqueries (Correlated vs Non-Correlated)

## Intuition
A subquery is a `SELECT` inside another SQL statement.

## 1. Non-Correlated Subquery
The inner query runs exactly **once** and the result is used by the outer query.
```sql
-- Find products more expensive than the average price
SELECT name, price
FROM   products
WHERE  price > (SELECT AVG(price) FROM products);
```

## 2. Correlated Subquery
The inner query references the outer query's row. It runs **once per outer row**.
```sql
-- Find users who have placed at least one DELIVERED order
SELECT u.username
FROM   users u
WHERE  EXISTS (
    SELECT 1
    FROM   orders o
    WHERE  o.user_id = u.id        -- References outer query alias (u)
      AND  o.status = 'DELIVERED'
);
```

## EXISTS vs IN
- `EXISTS` is better when the subquery returns a large result set, because it short-circuits on the first match. It never counts all matches.
- `IN` is fine for small, fixed lists.

## NOT EXISTS vs NOT IN (The NULL Trap)
`NOT EXISTS` is much safer than `NOT IN` when `NULL`s might be present.
If any subquery row is `NULL`, `NOT IN` returns NO rows (because `NULL` comparisons yield "unknown"). `NOT EXISTS` handles `NULL`s correctly.
```sql
-- Find products that have never been ordered
SELECT p.name
FROM   products p
WHERE  NOT EXISTS (
    SELECT 1 FROM order_items oi WHERE oi.product_id = p.id
);
```
