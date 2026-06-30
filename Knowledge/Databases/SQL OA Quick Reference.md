---
type: concept
title: SQL OA Quick Reference
tags: [sql, database, oa, cheatsheet]
---
# SQL OA Quick Reference

This note aggregates the most common SQL patterns tested in Online Assessments (OAs), categorized by the weekly practice track.

## 1. JOINs and Anti-Joins
- **Pattern**: Find missing records.
- **Why it's tested**: Tests understanding of `LEFT JOIN` and `IS NULL` vs `NOT IN` performance.
```postgresql
SELECT u.id, u.name
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

## 2. Aggregations and Subqueries
- **Pattern**: Find the highest/lowest aggregated value without a full scan or complex subquery.
- **Why it's tested**: Tests `GROUP BY` paired with `ORDER BY` and `LIMIT`.
```postgresql
SELECT department_id, AVG(salary) as avg_salary
FROM employees
GROUP BY department_id
ORDER BY avg_salary DESC
LIMIT 1;
```

## 3. Window Functions
- **Pattern**: Top N per category.
- **Why it's tested**: Standard way to solve ranking problems within partitions.
```postgresql
WITH RankedEmployees AS (
  SELECT name, salary, department_id,
         DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as rank
  FROM employees
)
SELECT name, salary, department_id
FROM RankedEmployees
WHERE rank <= 3;
```

## 4. Recursive CTEs for Hierarchical Data
- **Pattern**: Traverse trees or graphs (e.g., org charts).
- **Why it's tested**: Proves advanced SQL knowledge beyond basic CRUD.
```postgresql
WITH RECURSIVE Subordinates AS (
  SELECT id, name, manager_id, 1 as level
  FROM employees WHERE id = 1
  UNION ALL
  SELECT e.id, e.name, e.manager_id, s.level + 1
  FROM employees e
  INNER JOIN Subordinates s ON e.manager_id = s.id
)
SELECT * FROM Subordinates;
```

## 5. CASE WHEN and EXISTS Performance
- **Pattern**: Conditional logic and fast filtering.
- **Why it's tested**: `EXISTS` short-circuits and is often faster than `IN` for correlated subqueries.
```postgresql
SELECT o.id,
       CASE WHEN o.total > 1000 THEN 'High Value' ELSE 'Standard' END as category
FROM orders o
WHERE EXISTS (
    SELECT 1 FROM subscriptions s WHERE s.user_id = o.user_id AND s.status = 'ACTIVE'
);
```

## 6. Date/String Functions and EXPLAIN ANALYZE
- **Pattern**: Filtering by recent dates and extracting substrings.
- **Why it's tested**: Real-world utility. `EXPLAIN ANALYZE` shows debugging skills.
```postgresql
EXPLAIN ANALYZE
SELECT id, SUBSTRING(email FROM '@(.*)$') as domain
FROM users
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';
```
