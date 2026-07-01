---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 1 — SQL Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [sql, ddl, databases, constraints]
---

# SQL DDL and Constraints

## Intuition
**DDL (Data Definition Language)** creates, alters, and drops database objects. 
The database enforces DDL constraints on every write — no application code is required. The database is the last line of defense against bad data.

## Common Constraints
- `PRIMARY KEY`: Uniqueness + NOT NULL.
- `FOREIGN KEY`: Referential integrity (values must exist in the referenced table).
- `UNIQUE`: No duplicates allowed.
- `NOT NULL`: Field is required.
- `CHECK`: Custom validation logic (e.g., `price >= 0`, `status IN ('PENDING', 'SHIPPED')`).
- `DEFAULT`: Fallback value if none is provided.

## Examples
```sql
CREATE TABLE employees (
    id            BIGSERIAL      PRIMARY KEY,                  -- auto-increment unique key
    email         VARCHAR(255)   UNIQUE NOT NULL,              -- no duplicates, required
    salary        DECIMAL(10,2)  NOT NULL DEFAULT 50000,       -- default if omitted
    department_id BIGINT         REFERENCES departments(id),   -- foreign key
    manager_id    BIGINT         REFERENCES employees(id),     -- self-referential FK
    hire_date     DATE           NOT NULL,
    level         VARCHAR(10)    CHECK (level IN ('JUNIOR','MID','SENIOR')),  -- enum-like
    age           INTEGER        CHECK (age >= 18 AND age <= 70)              -- range
);
```

**Altering Tables:** In production, always alter tables via migration scripts (e.g., Flyway), never manually.
```sql
ALTER TABLE products ADD COLUMN sku VARCHAR(50) UNIQUE;
ALTER TABLE products ALTER COLUMN description SET NOT NULL;
ALTER TABLE products DROP COLUMN sku;
```

## Indexes
Creates a B-tree (usually) over columns to speed up querying, at the cost of slower writes and extra storage.
```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);
CREATE UNIQUE INDEX idx_products_name ON products(name);
```
