---
type: concept
title: Window Functions
tags: [sql, database, oa, concepts]
---
# Window Functions

Window functions operate on a set of rows and return a single value for each row from the underlying query. Unlike aggregate functions (like `GROUP BY`), window functions do not cause rows to become grouped into a single output row.

## Key Functions
- **`ROW_NUMBER()`**: Assigns a unique, sequential integer to each row within a partition.
- **`RANK()`**: Assigns a rank to each row within a partition, with gaps in rank values if there are ties.
- **`DENSE_RANK()`**: Similar to `RANK()`, but without gaps in rank values.
- **`LAG(col, offset)`**: Accesses data from a previous row in the same result set.
- **`LEAD(col, offset)`**: Accesses data from a subsequent row in the same result set.

## Standard Syntax
```postgresql
SELECT column1, 
       FUNCTION_NAME() OVER (
           PARTITION BY partition_column 
           ORDER BY sort_column
       ) as alias
FROM table_name;
```

## Why it's tested in OAs
Interviewers use window functions to test if you can solve "Top N per category" problems without resorting to highly inefficient subqueries. It's the most reliable way to group, sort, and rank data simultaneously.
