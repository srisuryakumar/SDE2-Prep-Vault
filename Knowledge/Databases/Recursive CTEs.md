---
type: concept
title: Recursive CTEs
tags: [sql, database, oa, concepts]
---
# Recursive Common Table Expressions (CTEs)

A Recursive CTE is a CTE that references itself. It is primarily used to query hierarchical data, such as organizational charts, bill of materials, or network routing graphs.

## Structure
A recursive CTE always consists of two parts separated by a `UNION` or `UNION ALL`:
1. **The Anchor Member**: The base query that forms the starting point of the recursion.
2. **The Recursive Member**: The query that references the CTE itself to iterate through the hierarchy.

## Standard Syntax
```postgresql
WITH RECURSIVE cte_name AS (
    -- Anchor member
    SELECT id, parent_id, 1 AS level
    FROM table_name
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive member
    SELECT t.id, t.parent_id, c.level + 1
    FROM table_name t
    INNER JOIN cte_name c ON t.parent_id = c.id
)
SELECT * FROM cte_name;
```

## Why it's tested in OAs
Recursive CTEs demonstrate that a candidate can think about graph and tree traversal at the database level rather than pulling all data into application memory to build the tree.
