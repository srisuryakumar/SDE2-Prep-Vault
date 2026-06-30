---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 1 — SQL Fundamentals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [sql, cte, recursive]
---

# CTEs (Common Table Expressions)

## Intuition
A CTE (`WITH` clause) names a subquery so you can reference it like a table. 
Benefits: Highly readable, avoids repeating logic, can reference the same CTE multiple times in the main query.

## Basic CTE
```sql
WITH user_spending AS (
    SELECT u.id, u.username, COALESCE(SUM(o.total_amount), 0) AS total_spent
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'DELIVERED'
    GROUP BY u.id, u.username
),
avg_spending AS (
    SELECT AVG(total_spent) AS avg FROM user_spending
)
SELECT us.username, us.total_spent, ROUND(us.total_spent - a.avg, 2) AS above_average_by
FROM user_spending us
CROSS JOIN avg_spending a
WHERE us.total_spent > a.avg;
```

## Recursive CTE
Used to walk hierarchical or graph data (e.g. org charts, category trees).
Requires: `UNION ALL` between a **base case** and a **recursive case**.

```sql
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: start with roots (employees with no manager)
    SELECT id, full_name, manager_id, 0 AS depth, full_name::TEXT AS path
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: find employees whose manager is in the previous result set
    SELECT e.id, e.full_name, e.manager_id, eh.depth + 1, (eh.path || ' → ' || e.full_name)
    FROM employees e
    INNER JOIN employee_hierarchy eh ON eh.id = e.manager_id
    WHERE eh.depth < 10 -- Safety valve to prevent infinite loops
)
SELECT depth, full_name, path
FROM employee_hierarchy
ORDER BY depth, full_name;
```
