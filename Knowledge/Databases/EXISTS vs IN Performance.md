---
type: concept
title: EXISTS vs IN Performance
tags: [sql, database, oa, concepts]
---
# EXISTS vs IN Performance

Both `EXISTS` and `IN` are used to filter results based on the presence of values in a subquery, but their internal execution engines differ drastically, impacting performance.

## `IN`
- **How it works**: The subquery is executed first, fetching a list of all matching values. The outer query then compares each row against this list.
- **When to use**: Best when the subquery returns a very small, static list of values.

## `EXISTS`
- **How it works**: Evaluates true/false. It stops executing the subquery the moment it finds the *first* matching row (short-circuiting).
- **When to use**: Best for correlated subqueries and when the subquery involves large tables.

## Example
**Slower (IN):**
```postgresql
SELECT name FROM customers 
WHERE id IN (SELECT customer_id FROM large_orders_table);
```

**Faster (EXISTS):**
```postgresql
SELECT name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM large_orders_table o WHERE o.customer_id = c.id
);
```

## Why it's tested in OAs
Understanding the short-circuiting nature of `EXISTS` is a classic indicator of a candidate's query optimization skills, especially when dealing with massive relational datasets.
