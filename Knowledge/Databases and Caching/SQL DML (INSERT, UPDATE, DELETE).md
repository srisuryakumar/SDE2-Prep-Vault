---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 1 — SQL Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [sql, dml, databases, update, delete]
---

# SQL DML (INSERT, UPDATE, DELETE)

## Intuition
**DML (Data Manipulation Language)** reads and writes rows.

## INSERT and UPSERT
```sql
-- Single row
INSERT INTO users (email, username) VALUES ('diana@example.com', 'diana');

-- Multiple rows (faster, fewer round-trips)
INSERT INTO products (name, price) VALUES 
    ('Keyboard', 2500.00), 
    ('Monitor', 15000.00);

-- UPSERT: Insert if new, update if already exists (ON CONFLICT)
-- Essential for making operations idempotent.
INSERT INTO products (name, price) VALUES ('Laptop', 78000.00)
ON CONFLICT (name) 
DO UPDATE SET price = EXCLUDED.price;
```

## UPDATE
**Production Rule:** Always test your `WHERE` clause with a `SELECT` before running an `UPDATE`. Wrap in a transaction (`BEGIN...COMMIT`) and check the affected row count before committing. Add a conditional check to ensure idempotence.

```sql
UPDATE orders
SET    status     = 'PROCESSING',
       updated_at = NOW()
WHERE  id = 1
  AND  status = 'PENDING'; -- Guards against double-update!
```
**UPDATE with a JOIN:**
```sql
UPDATE order_items oi
SET    unit_price = p.price
FROM   products p
WHERE  oi.product_id = p.id
  AND  oi.unit_price != p.price; -- Only update rows where price actually changed
```

## DELETE
```sql
-- DELETE with subquery
DELETE FROM orders
WHERE  status = 'CANCELLED'
  AND  created_at < NOW() - INTERVAL '90 days'
  AND  id NOT IN (SELECT order_id FROM order_items);
```
