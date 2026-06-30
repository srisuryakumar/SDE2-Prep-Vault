# Book 3: Databases and Caching
## From SQL Fundamentals to Production Data Architecture

> **How to use this book:** Every SQL query runs against the four tables defined in Chapter 1.
> Every concept explains the *why* before the *how*.
> Interview callouts appear throughout — look for the 💡 marker.

---

## Chapter 1: SQL Fundamentals

### The 4-Table Schema (Used Throughout This Entire Book)

Every query in this book runs against these four tables.
Create them now and keep them open in a separate terminal:

```sql
-- Users: the people using our platform
CREATE TABLE users (
    id           BIGSERIAL    PRIMARY KEY,
    email        VARCHAR(255) UNIQUE NOT NULL,
    username     VARCHAR(50)  UNIQUE NOT NULL,
    full_name    VARCHAR(100),
    created_at   TIMESTAMP    NOT NULL DEFAULT NOW(),
    is_active    BOOLEAN      NOT NULL DEFAULT TRUE
);

-- Products: items available for purchase
CREATE TABLE products (
    id           BIGSERIAL      PRIMARY KEY,
    name         VARCHAR(255)   NOT NULL,
    description  TEXT,
    price        DECIMAL(10,2)  NOT NULL CHECK (price >= 0),
    stock_count  INTEGER        NOT NULL DEFAULT 0 CHECK (stock_count >= 0),
    category     VARCHAR(100),
    created_at   TIMESTAMP      NOT NULL DEFAULT NOW()
);

-- Orders: a purchase event by a user
CREATE TABLE orders (
    id           BIGSERIAL      PRIMARY KEY,
    user_id      BIGINT         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status       VARCHAR(20)    NOT NULL DEFAULT 'PENDING'
                     CHECK (status IN ('PENDING','PROCESSING','SHIPPED','DELIVERED','CANCELLED')),
    total_amount DECIMAL(10,2),
    created_at   TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP      NOT NULL DEFAULT NOW()
);

-- Order Items: the individual products within an order
CREATE TABLE order_items (
    id           BIGSERIAL      PRIMARY KEY,
    order_id     BIGINT         NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id   BIGINT         NOT NULL REFERENCES products(id),
    quantity     INTEGER        NOT NULL CHECK (quantity > 0),
    unit_price   DECIMAL(10,2)  NOT NULL,
    UNIQUE(order_id, product_id)   -- a product can only appear once per order
);
```

**Why these four tables?** They model a real e-commerce system and cover every
SQL concept you need: one-to-many relationships (users→orders), many-to-many
relationships via a junction table (orders↔products via order_items), constraints,
aggregation, window functions, and self-joins (if we add manager_id to users).

```sql
-- Seed data — run this after creating tables
INSERT INTO users (email, username, full_name) VALUES
    ('alice@example.com',   'alice',   'Alice Johnson'),
    ('bob@example.com',     'bob',     'Bob Smith'),
    ('charlie@example.com', 'charlie', 'Charlie Brown');

INSERT INTO products (name, price, stock_count, category) VALUES
    ('Laptop',   75000.00, 10, 'Electronics'),
    ('Mouse',     1200.00, 50, 'Electronics'),
    ('Desk',      8000.00,  5, 'Furniture'),
    ('Chair',     6000.00,  8, 'Furniture');

INSERT INTO orders (user_id, status, total_amount) VALUES
    (1, 'DELIVERED', 76200.00),   -- Alice's delivered order
    (1, 'PENDING',    6000.00),   -- Alice's pending order
    (2, 'SHIPPED',    8000.00);   -- Bob's shipped order
-- Note: Charlie (user 3) has no orders — useful for LEFT JOIN examples

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 75000.00),  -- Alice's order 1: Laptop
    (1, 2, 1,  1200.00),  -- Alice's order 1: Mouse
    (2, 4, 1,  6000.00),  -- Alice's order 2: Chair
    (3, 3, 1,  8000.00);  -- Bob's order:    Desk
```

---

### DDL — Defining Structure

DDL (Data Definition Language) creates, alters, and drops database objects.
The database enforces DDL constraints on every write — no application code required.

```sql
-- CREATE TABLE with every constraint type demonstrated:
CREATE TABLE employees (
    id            BIGSERIAL      PRIMARY KEY,                  -- auto-increment unique key
    email         VARCHAR(255)   UNIQUE NOT NULL,              -- no duplicates, required
    salary        DECIMAL(10,2)  NOT NULL DEFAULT 50000,       -- default if omitted
    department_id BIGINT         REFERENCES departments(id),   -- foreign key (nullable)
    manager_id    BIGINT         REFERENCES employees(id),     -- self-referential FK
    hire_date     DATE           NOT NULL,
    level         VARCHAR(10)    CHECK (level IN ('JUNIOR','MID','SENIOR')),  -- enum-like
    age           INTEGER        CHECK (age >= 18 AND age <= 70)              -- range
);

-- ALTER TABLE: modify structure of existing tables
-- In production, always do this through Flyway migrations (Chapter 4)
ALTER TABLE products ADD COLUMN sku VARCHAR(50) UNIQUE;        -- add column
ALTER TABLE products ALTER COLUMN description SET NOT NULL;    -- tighten constraint
ALTER TABLE products DROP COLUMN sku;                          -- remove column

-- CREATE INDEX: speeds up queries that filter, sort, or join on indexed columns
-- Without an index, PostgreSQL reads every row (sequential scan).
-- With a B-tree index, PostgreSQL navigates the tree in O(log n) — see Chapter 2.
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);  -- composite
CREATE UNIQUE INDEX idx_products_name ON products(name);                    -- enforces uniqueness
```

> 💡 **Interview:** "What constraints does PostgreSQL enforce automatically?"
> PRIMARY KEY (uniqueness + NOT NULL), FOREIGN KEY (referential integrity),
> UNIQUE, NOT NULL, CHECK. These fire on every INSERT, UPDATE, and DELETE
> with zero application code — the database is the last line of defence.

---

### DML — Manipulating Data

DML (Data Manipulation Language) reads and writes rows.
The four statements are SELECT, INSERT, UPDATE, DELETE.

```sql
-- INSERT: single row
INSERT INTO users (email, username, full_name)
VALUES ('diana@example.com', 'diana', 'Diana Prince');

-- INSERT: multiple rows in one statement (fewer round-trips = faster)
INSERT INTO products (name, price, stock_count, category) VALUES
    ('Keyboard',  2500.00, 30, 'Electronics'),
    ('Monitor',  15000.00, 12, 'Electronics'),
    ('Webcam',    3000.00, 20, 'Electronics');

-- UPSERT: insert if new, update if already exists (ON CONFLICT)
-- Useful for idempotent operations — safe to run multiple times
INSERT INTO products (name, price, stock_count, category)
VALUES ('Laptop', 78000.00, 15, 'Electronics')
ON CONFLICT (name)
DO UPDATE SET
    price       = EXCLUDED.price,
    stock_count = EXCLUDED.stock_count;
-- EXCLUDED refers to the row that would have been inserted

-- UPDATE: modify existing rows
-- RULE: always test your WHERE clause with SELECT before running UPDATE
UPDATE orders
SET    status     = 'PROCESSING',
       updated_at = NOW()
WHERE  id = 1
  AND  status = 'PENDING';  -- only transition from PENDING (guards against double-update)

-- UPDATE with a JOIN (update based on data from another table)
UPDATE order_items oi
SET    unit_price = p.price
FROM   products p
WHERE  oi.product_id = p.id
  AND  oi.unit_price != p.price;  -- only rows where price actually changed

-- DELETE with subquery
DELETE FROM orders
WHERE  status = 'CANCELLED'
  AND  created_at < NOW() - INTERVAL '90 days'
  AND  id NOT IN (SELECT order_id FROM order_items);
-- Deletes only old cancelled orders that have no line items
```

> 💡 **Interview:** "How do you safely run an UPDATE in production?"
> (1) Run the equivalent SELECT to preview affected rows.
> (2) Wrap in BEGIN...ROLLBACK and check row count before committing.
> (3) Add LIMIT for large tables to batch the change.
> (4) Use a conditional WHERE (e.g., `AND status = 'PENDING'`) so the
> update is idempotent and self-protecting.

---

### Joins — Combining Tables

Joins reconstruct related information split across tables.
Think of two tables as two circles in a Venn diagram — the join type
determines which part of the diagram appears in your result.

```
INNER JOIN — only the overlapping part (rows matching in BOTH tables):

       users              orders
      ┌──────┐           ┌──────┐
      │Alice │           │      │
      │ Bob  │▓▓▓▓▓▓▓▓▓▓│order1│  ← only users WITH orders appear
      │Charlie│          │      │
      └──────┘           └──────┘
       Alice and Bob have orders → appear in result
       Charlie has no orders → excluded
```

```sql
-- INNER JOIN: rows that match in BOTH tables
-- Use when: you only want records with a corresponding record on both sides
SELECT u.username, o.id AS order_id, o.status, o.total_amount
FROM   users u
INNER JOIN orders o ON o.user_id = u.id;
-- Result: Alice (2 rows) + Bob (1 row). Charlie excluded — he has no orders.
```

```
LEFT JOIN — all left rows + any matching right rows (right side NULL if no match):

       users              orders
      ┌──────┐           ┌──────┐
      │Alice │▓▓▓▓▓▓▓▓▓▓│order1│
      │ Bob  │▓▓▓▓▓▓▓▓▓▓│order2│  ← ALL users appear; NULL for users without orders
      │Charlie│▓▓▓ NULL  │      │
      └──────┘           └──────┘
```

```sql
-- LEFT JOIN: all rows from LEFT table, matched rows from RIGHT (NULL if no match)
-- Use when: you want ALL left-side records regardless of whether a match exists
SELECT u.username, COUNT(o.id) AS order_count
FROM   users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.username;
-- Result: Alice(2), Bob(1), Charlie(0) — Charlie appears with count=0

-- The NULL-filter trick: LEFT JOIN + WHERE right.id IS NULL → rows with NO match
SELECT u.username
FROM   users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE  o.id IS NULL;
-- Returns: Charlie (the user with no orders)
```

```sql
-- RIGHT JOIN: all rows from RIGHT table, matched from LEFT (NULL if no match)
-- Rarely used — rewrite as a LEFT JOIN with tables swapped (clearer to read)
SELECT u.username, o.id AS order_id
FROM   users u
RIGHT JOIN orders o ON o.user_id = u.id;
-- Equivalent: SELECT u.username, o.id FROM orders o LEFT JOIN users u ON u.id = o.user_id

-- FULL OUTER JOIN: all rows from BOTH tables, NULLs for non-matching side
SELECT u.username, o.id AS order_id
FROM   users u
FULL OUTER JOIN orders o ON o.user_id = u.id;
-- Returns: all users (with their orders or NULL) + any orders with no valid user

-- CROSS JOIN: cartesian product — every row from A paired with every row from B
-- 4 products × 3 users = 12 rows (useful for combinatorics, never for big tables)
SELECT u.username, p.name AS product
FROM   users u CROSS JOIN products p;

-- SELF JOIN: a table joined with itself — for hierarchical/graph data
-- Find each employee and their manager (both rows come from the employees table)
SELECT e.full_name AS employee, m.full_name AS manager
FROM   employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```

> 💡 **Interview:** "What is the difference between INNER JOIN and LEFT JOIN?"
> INNER JOIN returns only rows with a match in BOTH tables — non-matching rows disappear.
> LEFT JOIN returns ALL rows from the left table; right-side columns are NULL when
> no match exists. The pattern `LEFT JOIN ... WHERE right.id IS NULL` efficiently
> finds records that have NO corresponding row on the right side.

---

### Aggregation Functions

Aggregation collapses multiple rows into a summary value.
The key mental model: GROUP BY creates groups, then aggregate functions
run once per group.

```sql
-- COUNT, SUM, AVG, MIN, MAX with GROUP BY
SELECT
    category,
    COUNT(*)                     AS product_count,
    ROUND(AVG(price), 2)         AS avg_price,
    MIN(price)                   AS cheapest,
    MAX(price)                   AS most_expensive,
    SUM(price * stock_count)     AS total_inventory_value
FROM   products
GROUP BY category
ORDER BY total_inventory_value DESC;

-- HAVING: filter groups after aggregation (WHERE filters rows before grouping)
-- "Find categories with more than 2 products AND average price above ₹5000"
SELECT   category, COUNT(*) AS cnt, ROUND(AVG(price), 2) AS avg_price
FROM     products
GROUP BY category
HAVING   COUNT(*) > 2 AND AVG(price) > 5000;
-- Rule: WHERE cannot reference aggregate functions; HAVING can

-- Combining WHERE and HAVING (the most common confusion in SQL interviews):
SELECT   u.username,
         SUM(oi.quantity * oi.unit_price) AS revenue
FROM     users u
JOIN     orders     o  ON o.user_id    = u.id
JOIN     order_items oi ON oi.order_id = o.id
WHERE    o.status = 'DELIVERED'                          -- row filter (before grouping)
GROUP BY u.id, u.username
HAVING   SUM(oi.quantity * oi.unit_price) > 50000       -- group filter (after aggregation)
ORDER BY revenue DESC;
```

**Execution order of a SELECT statement** (memorise this for interviews):

```
1.  FROM / JOIN    → identify all source rows
2.  WHERE          → filter individual rows
3.  GROUP BY       → form groups
4.  Aggregate fns  → COUNT(), SUM(), etc. compute within each group
5.  HAVING         → filter groups based on aggregate results
6.  SELECT         → choose and compute output columns (aliases defined here)
7.  DISTINCT       → remove duplicates if requested
8.  ORDER BY       → sort (can use SELECT aliases)
9.  LIMIT/OFFSET   → truncate result
```

> 💡 **Interview:** "Can you use a SELECT alias in a WHERE clause?"
> No — WHERE executes at step 2, before SELECT (step 6) has defined the alias.
> You can use the alias in ORDER BY and HAVING, which execute after SELECT.
> This is why `WHERE total_spent > 100` fails but `HAVING total_spent > 100` works
> when `total_spent` is a SELECT alias wrapping an aggregate.

---

### Subqueries

A subquery is a SELECT inside another SQL statement.
Two types: non-correlated (runs once) and correlated (runs once per outer row).

```sql
-- Non-correlated subquery: inner query runs once, result is used by outer query
-- "Find products more expensive than the average price"
SELECT name, price
FROM   products
WHERE  price > (SELECT AVG(price) FROM products);
-- The subquery (SELECT AVG...) runs exactly once and returns a scalar.
-- The outer WHERE compares each row's price against that scalar.

-- Correlated subquery: inner query references the outer query's row
-- "Find users who have placed at least one DELIVERED order"
SELECT u.username
FROM   users u
WHERE  EXISTS (
    SELECT 1
    FROM   orders o
    WHERE  o.user_id = u.id        -- ← references outer query alias
      AND  o.status = 'DELIVERED'
);
-- For EACH user row, the subquery runs once.
-- EXISTS stops as soon as it finds ONE match — it never counts all matches.

-- EXISTS vs IN — when does it matter?
-- EXISTS is better when the subquery returns a large result set
--   (it short-circuits on first match)
-- IN is fine for small, fixed lists
-- Modern PostgreSQL often rewrites both to the same plan, but EXISTS is
-- the safer habit for correlated cases.

-- NOT EXISTS — cleaner than NOT IN when NULLs might be present
-- "Find products that have never been ordered"
SELECT p.name
FROM   products p
WHERE  NOT EXISTS (
    SELECT 1 FROM order_items oi WHERE oi.product_id = p.id
);
-- NOT IN with NULLs is a trap: if any subquery row is NULL,
-- NOT IN returns no rows (because NULL comparisons are unknown).
-- NOT EXISTS handles NULLs correctly.

-- Subquery in FROM clause (derived table / inline view)
SELECT username, total_orders
FROM (
    SELECT u.username, COUNT(o.id) AS total_orders
    FROM   users u LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id, u.username
) AS user_stats
WHERE total_orders >= 2;
```

---

### Window Functions

Window functions compute a value for each row using a *window* of related rows.
Unlike GROUP BY, they **do not collapse rows** — every individual row remains in
the result set with an additional computed column.

```
Mental model:
  GROUP BY:  [A, B, B, C, C, C]  →  [A(count=1), B(count=2), C(count=3)]
                                       ↑ rows collapsed into groups

  Window fn: [A, B, B, C, C, C]  →  [A(rn=1), B(rn=1), B(rn=2), C(rn=1), C(rn=2), C(rn=3)]
                                       ↑ all rows kept; each gets a computed annotation
```

**Syntax:** `FUNCTION() OVER (PARTITION BY col ORDER BY col [frame])`
- `PARTITION BY` — divide rows into independent groups (like GROUP BY but rows not collapsed)
- `ORDER BY` inside OVER — sort rows within each partition
- Frame clause — which rows in the partition count (`ROWS BETWEEN ...`)

```sql
-- ROW_NUMBER: unique sequential number per partition (no ties)
SELECT
    o.id,
    o.user_id,
    o.created_at,
    o.total_amount,
    ROW_NUMBER() OVER (PARTITION BY o.user_id ORDER BY o.created_at DESC) AS rn
FROM orders o;
-- Each user's orders are numbered 1, 2, 3... with 1 = most recent
-- Classic use: "Get the most recent order per user" → wrap in CTE and WHERE rn = 1

-- RANK vs DENSE_RANK: tie-handling
-- Given total_spent: Alice=76200, Bob=8000, Charlie=0
SELECT
    username,
    total_spent,
    RANK()       OVER (ORDER BY total_spent DESC) AS rank_with_gaps,
    DENSE_RANK() OVER (ORDER BY total_spent DESC) AS rank_no_gaps
FROM (
    SELECT u.username, COALESCE(SUM(o.total_amount), 0) AS total_spent
    FROM   users u LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id, u.username
) AS user_totals;
-- If two users tie for 1st:
--   RANK:        1, 1, 3   ← gap after tie (rank 2 is skipped)
--   DENSE_RANK:  1, 1, 2   ← no gap

-- LAG and LEAD: access the previous or next row's value within a partition
SELECT
    o.id,
    o.user_id,
    o.total_amount,
    o.created_at,
    LAG(o.total_amount)  OVER (PARTITION BY o.user_id ORDER BY o.created_at)
        AS previous_order_amount,
    LEAD(o.total_amount) OVER (PARTITION BY o.user_id ORDER BY o.created_at)
        AS next_order_amount,
    o.total_amount
        - LAG(o.total_amount) OVER (PARTITION BY o.user_id ORDER BY o.created_at)
        AS change_from_previous
FROM orders o;
-- LAG = look back 1 row; LEAD = look ahead 1 row
-- First row LAG = NULL (no previous); Last row LEAD = NULL (no next)
-- Use case: "Is this order larger or smaller than the user's previous order?"

-- Running total with SUM() OVER (frame clause):
SELECT
    o.id,
    o.user_id,
    o.total_amount,
    SUM(o.total_amount) OVER (
        PARTITION BY o.user_id
        ORDER BY o.created_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM orders o;
-- ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW = "all rows up to and including now"
-- Result: for each order, the cumulative total that user has spent up to that order

-- Top-N per group: ROW_NUMBER is the standard technique
-- "Get the 2 most expensive products per category"
SELECT name, price, category
FROM (
    SELECT
        name, price, category,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
    FROM products
) AS ranked
WHERE rn <= 2;
-- Window function executes before the outer WHERE, so rn is available for filtering
```

> 💡 **Interview:** "What is the difference between RANK and DENSE_RANK?"
> Both assign the same rank to tied rows. RANK then *skips* the next rank(s)
> to account for the tie (1, 1, 3). DENSE_RANK never skips (1, 1, 2).
> ROW_NUMBER always assigns a unique number regardless of ties — its ordering
> among tied rows is non-deterministic without a tiebreaker in ORDER BY.

---

### CTEs — Common Table Expressions

A CTE (`WITH` clause) names a subquery so you can reference it like a table.
Benefits: readable, avoids repeating logic, can reference the same CTE multiple times.

```sql
-- Basic CTE: break a complex query into named, readable steps
WITH user_spending AS (
    -- Step 1: compute each user's total delivered spend
    SELECT
        u.id,
        u.username,
        COALESCE(SUM(o.total_amount), 0) AS total_spent
    FROM   users u
    LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'DELIVERED'
    GROUP BY u.id, u.username
),
avg_spending AS (
    -- Step 2: compute the average of those totals
    SELECT AVG(total_spent) AS avg FROM user_spending
)
-- Step 3: use both CTEs in the final query
SELECT
    us.username,
    us.total_spent,
    ROUND(us.total_spent - a.avg, 2) AS above_average_by
FROM user_spending us
CROSS JOIN avg_spending a
WHERE us.total_spent > a.avg;
-- user_spending is computed once and referenced twice — no redundant computation
```

```sql
-- Recursive CTE: walk hierarchical or graph data (org charts, category trees, paths)
-- Requires: UNION ALL between base case and recursive case
WITH RECURSIVE employee_hierarchy AS (

    -- Base case: start with roots (employees with no manager)
    SELECT
        id,
        full_name,
        manager_id,
        0            AS depth,
        full_name::TEXT AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: find employees whose manager is in the previous result set
    SELECT
        e.id,
        e.full_name,
        e.manager_id,
        eh.depth + 1,
        (eh.path || ' → ' || e.full_name)
    FROM employees e
    INNER JOIN employee_hierarchy eh ON eh.id = e.manager_id
    WHERE eh.depth < 10   -- safety valve: prevents infinite loop on circular references
)
SELECT depth, full_name, path
FROM   employee_hierarchy
ORDER BY depth, full_name;
-- depth=0: CEO
-- depth=1: VPs
-- depth=2: Directors...
-- path shows full chain: "CEO → VP Engineering → Director of Backend"
```

---

### Set Operations

Set operations combine results from two SELECT statements.
Both sides must have the same number of columns and compatible types.

```sql
-- UNION: combine and deduplicate (sort step required — slower)
SELECT username FROM users WHERE is_active = TRUE
UNION
SELECT username FROM users WHERE id IN (SELECT user_id FROM orders);
-- Returns unique usernames satisfying EITHER condition

-- UNION ALL: combine and keep duplicates (no sort — faster)
-- Use UNION ALL whenever duplicates are impossible or acceptable
SELECT username FROM users WHERE is_active = TRUE
UNION ALL
SELECT username FROM users WHERE id IN (SELECT user_id FROM orders);

-- INTERSECT: rows appearing in BOTH result sets
SELECT username FROM users WHERE is_active = TRUE
INTERSECT
SELECT username FROM users WHERE id IN (SELECT user_id FROM orders);
-- Users who are active AND have placed at least one order

-- EXCEPT: rows in the first set that do NOT appear in the second set
SELECT username FROM users
EXCEPT
SELECT username FROM users WHERE id IN (SELECT user_id FROM orders);
-- Users who have NEVER placed an order (same as the LEFT JOIN / NOT EXISTS pattern)
```

---

### 10 Practice Queries (Increasing Complexity)

Each query is self-contained and runs against the seed data from section 1.1.

```sql
-- Q1: List all products with category, sorted by price descending
SELECT name, category, price
FROM   products
ORDER BY price DESC;

-- Q2: Count orders by status
SELECT   status, COUNT(*) AS count
FROM     orders
GROUP BY status
ORDER BY count DESC;

-- Q3: Users who have never placed an order
SELECT u.username
FROM   users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE  o.id IS NULL;

-- Q4: Total revenue per product (from DELIVERED orders only)
SELECT
    p.name,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM   products p
JOIN   order_items oi ON oi.product_id = p.id
JOIN   orders      o  ON o.id          = oi.order_id
WHERE  o.status = 'DELIVERED'
GROUP BY p.id, p.name
ORDER BY revenue DESC;

-- Q5: Average order value per user (only users with 2+ orders)
SELECT
    u.username,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM   users u
JOIN   orders o ON o.user_id = u.id
GROUP BY u.id, u.username
HAVING COUNT(o.id) >= 2;

-- Q6: Most recent order for each user
-- DISTINCT ON is a PostgreSQL extension — cleaner than ROW_NUMBER() for this case
SELECT DISTINCT ON (u.id)
    u.username,
    o.id         AS order_id,
    o.status,
    o.created_at
FROM   users u
JOIN   orders o ON o.user_id = u.id
ORDER BY u.id, o.created_at DESC;
-- DISTINCT ON keeps ONE row per group (the first after ORDER BY)

-- Q7: Products that have never been ordered (NOT EXISTS version)
SELECT p.name
FROM   products p
WHERE  NOT EXISTS (
    SELECT 1 FROM order_items oi WHERE oi.product_id = p.id
);

-- Q8: Monthly revenue trend (from DELIVERED orders)
SELECT
    DATE_TRUNC('month', o.created_at)        AS month,
    COUNT(DISTINCT o.id)                     AS order_count,
    SUM(oi.quantity * oi.unit_price)         AS revenue
FROM   orders      o
JOIN   order_items oi ON oi.order_id = o.id
WHERE  o.status = 'DELIVERED'
GROUP BY DATE_TRUNC('month', o.created_at)
ORDER BY month;

-- Q9: Rank users by total spending with percentile position
SELECT
    u.username,
    SUM(o.total_amount)                                              AS total_spent,
    RANK() OVER (ORDER BY SUM(o.total_amount) DESC)                  AS rank,
    ROUND(
        100.0 * RANK() OVER (ORDER BY SUM(o.total_amount) DESC)
              / COUNT(*) OVER (),
        1
    )                                                                AS percentile_rank
FROM   users u
JOIN   orders o ON o.user_id = u.id
WHERE  o.status = 'DELIVERED'
GROUP BY u.id, u.username;
-- RANK() and COUNT(*) OVER () are both window functions on the GROUP BY result set

-- Q10: Market basket analysis — products frequently bought together
-- Self-join on order_items: for every order, pair every product with every other product
SELECT
    p1.name          AS product_1,
    p2.name          AS product_2,
    COUNT(*)         AS times_bought_together
FROM   order_items oi1
JOIN   order_items oi2 ON  oi1.order_id   = oi2.order_id
                       AND oi1.product_id < oi2.product_id   -- avoid duplicate pairs & self-pairs
JOIN   products p1     ON p1.id = oi1.product_id
JOIN   products p2     ON p2.id = oi2.product_id
GROUP BY p1.id, p1.name, p2.id, p2.name
HAVING COUNT(*) >= 2
ORDER BY times_bought_together DESC;
-- `oi1.product_id < oi2.product_id` ensures (Laptop,Mouse) and (Mouse,Laptop) don't both appear
```

---

## Chapter 2: Database Internals

*Knowing SQL syntax is like knowing how to drive. Understanding internals is
knowing how the engine works — which makes you a dramatically better driver.*

### How PostgreSQL Stores Data on Disk

**Why this matters for interviews:** Every performance decision — when to index,
what index to create, when a full scan beats an index — follows from understanding
how data physically lives on disk.

PostgreSQL reads and writes in **pages** of 8KB, never individual rows.
Even fetching one row requires reading the entire 8KB page containing it.

```
Disk Layout — heap file for the orders table:

┌──────────────────────────────────────────────────────────────────┐
│  Heap File: orders                                               │
│                                                                   │
│  Page 0 (8KB)          Page 1 (8KB)          Page 2 (8KB)       │
│ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│ │ Page Header (24B)│  │ Page Header      │  │ Page Header      │ │
│ │ ItemId[0] ──┐   │  │ ItemId[0] ──┐   │  │ (empty page)     │ │
│ │ ItemId[1] ──┤   │  │             │   │  │                  │ │
│ │   ...       │   │  │             │   │  │                  │ │
│ │─────────────│   │  │             │   │  │                  │ │
│ │ Free Space  │   │  │  Free Space │   │  │  Free Space      │ │
│ │─────────────│   │  │─────────────│   │  │                  │ │
│ │ Row Tuple 2 │   │  │ Row Tuple 3 │   │  │                  │ │
│ │ Row Tuple 1 ◄───┘  │ Row Tuple   ◄───┘  │                  │ │
│ └──────────────────┘  └──────────────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────────────────────┘

Each row (tuple) header contains:
  xmin: transaction ID that created this row version
  xmax: transaction ID that deleted/updated this row (0 = still live)
  ctid: physical location (page number, slot number)
```

**Sequential vs random I/O:**
- Sequential scan: reads pages in order from disk. The OS prefetches ahead.
  ~500 MB/s on SSD.
- Index scan: jumps to specific pages by address. Each jump is a random read.
  Fast on SSD, expensive on spinning disk (~5ms per seek).

Counterintuitive fact: for a query returning 20%+ of a table's rows,
a sequential scan is often **faster** than using an index, because the
index generates thousands of random reads versus one sweep of sequential pages.
The query planner knows this and chooses accordingly.

---

### B-Tree Index — The Most Important Data Structure in Databases

**Why indexes exist:** Without an index, `WHERE user_id = 1` reads every row in
the table and compares. For 10 million orders, that is 10 million comparisons.
A B-tree index makes this O(log n): 3-4 page reads regardless of table size.

```
B-Tree for orders.user_id:

                        [   20   ]                         ← root node
                       /          \
               [ 10 ]              [ 30 ]                  ← internal nodes
              /      \             /     \
          [ 5 ]    [ 15 ]      [ 25 ]   [ 40 ]
         /    \    /    \      /    \   /     \
       [3][7][12][18] [22][27][35][45]                     ← leaf nodes
        │   │   │   │   │   │   │   │
        ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓
       row row row row row row row row                     ← heap pointers

Leaf nodes form a linked list: [3]→[7]→[12]→[18]→[22]→[27]→[35]→[45]
                                                                ↑
                                        This chain enables efficient range queries!
Range scan `WHERE user_id BETWEEN 12 AND 27`:
  1. Navigate tree to leaf [12] in O(log n)
  2. Walk the linked list forward: 12→18→22→27 — stop at 27
  3. Fetch heap rows for each pointer found
```

**Why B-tree height stays small:**

Each internal node in PostgreSQL's B-tree holds ~340 pointers.

| Height | Max rows covered |
|--------|-----------------|
| 1      | 340             |
| 2      | 115,600         |
| 3      | 39,000,000      |
| 4      | 13,000,000,000  |

A table with 100 million rows has an index height of 3-4. Every row lookup =
3-4 disk page reads.

**Multi-column composite indexes — the left-prefix rule:**

```sql
-- Composite index on (user_id, status, created_at)
CREATE INDEX idx_orders_composite ON orders(user_id, status, created_at DESC);

-- CAN use this index (left prefix present):
WHERE user_id = 1
WHERE user_id = 1 AND status = 'DELIVERED'
WHERE user_id = 1 AND status = 'DELIVERED' AND created_at > '2024-01-01'

-- CANNOT efficiently use this index (left column skipped):
WHERE status = 'DELIVERED'
WHERE created_at > '2024-01-01'

-- Analogy: a phone book sorted by (LastName, FirstName, MiddleName).
-- You can look up by LastName, or LastName+FirstName, but not FirstName alone.
```

**Covering index — zero heap access (Index Only Scan):**

```sql
-- A covering index includes all columns the query needs.
-- PostgreSQL can answer the query entirely from the index — no heap page reads.
CREATE INDEX idx_orders_covering
    ON orders(user_id, status)
    INCLUDE (total_amount, created_at);

-- This query never touches the heap — served 100% from the index:
SELECT status, total_amount, created_at
FROM   orders
WHERE  user_id = 1;
-- Plan shows: Index Only Scan — the fastest possible access pattern
```

**Reading EXPLAIN ANALYZE:**

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 1;

-- Output:
Index Scan using idx_orders_user_id on orders
    (cost=0.29..8.31 rows=2 width=64)
    (actual time=0.025..0.028 rows=2 loops=1)
  Index Cond: (user_id = 1)
Planning Time: 0.089 ms
Execution Time: 0.048 ms
```

| Field | Meaning |
|-------|---------|
| `cost=0.29..8.31` | Estimated cost: startup..total (arbitrary units, for comparison only) |
| `rows=2` | Planner's estimated row count (compare against actual to detect bad stats) |
| `actual time=0.025..0.028` | Real milliseconds: first-row time..last-row time |
| `actual rows=2` | Real row count (if far from estimated: run ANALYZE) |
| `loops=1` | How many times this node executed; multiply time × loops for true cost |

**Scan type reference:**

| Scan Type | When Used | Performance |
|-----------|-----------|-------------|
| Seq Scan | No usable index, or planner estimates cheaper than index | Slow for large tables with selective WHERE |
| Index Scan | Selective condition, B-tree index exists | Fast: O(log n) + heap lookup per row |
| Index Only Scan | All needed columns are in the index | Fastest: no heap access |
| Bitmap Index Scan | Moderately selective; many rows needed | Medium: batches heap reads to reduce random I/O |

> 💡 **Interview:** "When is a full table scan faster than an index scan?"
> When the query returns a large fraction of rows (roughly > 5-10% of the table).
> Index scans cause random heap reads — one per row found. For many rows, the
> cumulative random I/O cost exceeds a single sequential scan of all pages.
> The cost-based planner uses table statistics (row count, column distribution)
> to estimate both paths and pick the cheaper one.

---

### ACID Properties

**Why ACID matters:** Without these four guarantees, concurrent database access
produces incorrect results — money disappears, inventory goes negative, users
see inconsistent data. Every financial, medical, and e-commerce system depends on ACID.

#### Atomicity — All or Nothing

```sql
-- Transfer ₹1000 from Alice (user 1) to Bob (user 2)
BEGIN;
    UPDATE accounts SET balance = balance - 1000 WHERE user_id = 1;  -- debit Alice
    UPDATE accounts SET balance = balance + 1000 WHERE user_id = 2;  -- credit Bob
COMMIT;

-- If the server crashes between the two UPDATEs:
-- WITHOUT atomicity: Alice loses ₹1000, Bob never receives it. Money destroyed.
-- WITH atomicity:    PostgreSQL replays the WAL log on restart.
--                   Either BOTH updates apply, or NEITHER does.
--                   Money is never created or destroyed.
```

How it works: Before modifying any data page, PostgreSQL writes the change
description to the **WAL** (Write-Ahead Log). On crash recovery, PostgreSQL
replays all committed WAL entries and ignores all uncommitted ones.

#### Consistency — Rules Are Never Violated

```sql
-- The CHECK constraint enforces the "no negative balance" rule:
ALTER TABLE accounts ADD CONSTRAINT positive_balance CHECK (balance >= 0);

-- This fails entirely — the constraint aborts the transaction:
BEGIN;
    UPDATE accounts SET balance = balance - 1000000 WHERE user_id = 1;
COMMIT;
-- ERROR: new row for relation "accounts" violates check constraint "positive_balance"
-- Neither the debit nor any other change in this transaction is applied.
```

#### Isolation — Concurrent Transactions See Consistent Snapshots

```sql
-- Session 1 starts a transaction but hasn't committed yet:
BEGIN;
UPDATE orders SET status = 'PROCESSING' WHERE id = 1;
-- Not committed — only Session 1 can see this change

-- Session 2 reads the same row (at Read Committed isolation, the default):
SELECT status FROM orders WHERE id = 1;
-- Result: 'PENDING'  ← sees the pre-update state
-- Session 2 never sees Session 1's partial work.

-- Session 1 commits:
COMMIT;

-- Session 2 reads again:
SELECT status FROM orders WHERE id = 1;
-- Result: 'PROCESSING'  ← now sees the committed change
```

#### Durability — Committed Data Survives Crashes

PostgreSQL uses the WAL for durability. Before acknowledging COMMIT to the
client, PostgreSQL `fsync()`s the WAL file to disk. If the machine loses power
one millisecond after COMMIT returns, no data is lost — the WAL will be replayed
on restart and the committed state will be fully recovered.

```
Write sequence for a committed UPDATE:

  ① Transaction begins
  ② PostgreSQL writes change description to WAL (sequential write to disk)
       WAL entry: "In orders, row id=1: status='PENDING'→'PROCESSING'"
  ③ PostgreSQL modifies the in-memory buffer page (still "dirty", not on disk yet)
  ④ PostgreSQL fsync()s WAL → COMMIT acknowledged to application
  ⑤ [Later, asynchronously] Dirty buffer pages are flushed to actual data files

  Crash between ④ and ⑤:
    → Restart: PostgreSQL scans WAL for committed-but-not-flushed changes
    → Re-applies them to data files
    → All committed transactions are fully present
```

---

### Isolation Levels and Concurrency Anomalies

Three anomalies can occur when transactions run concurrently.
Four isolation levels trade performance for protection against them.

```
Isolation Level     │ Dirty Read │ Non-Repeatable │ Phantom Read
────────────────────┼────────────┼────────────────┼─────────────
Read Uncommitted    │ Possible   │ Possible       │ Possible
Read Committed      │ Prevented  │ Possible       │ Possible    ← PostgreSQL default
Repeatable Read     │ Prevented  │ Prevented      │ Possible*
Serializable        │ Prevented  │ Prevented      │ Prevented

* PostgreSQL's MVCC implementation prevents phantoms at Repeatable Read in practice
```

**Dirty Read:** Reading uncommitted changes from another transaction.
```
T1: BEGIN; UPDATE orders SET status='SHIPPED' WHERE id=1;
T2: SELECT status FROM orders WHERE id=1;  → sees 'SHIPPED' (dirty!)
T1: ROLLBACK;  → T1's change is discarded
T2 made a decision based on data that never actually existed.
PostgreSQL prevents this at all levels except Read Uncommitted.
```

**Non-Repeatable Read:** Same query returns different values within one transaction.
```
T1: SELECT total_amount FROM orders WHERE id=1;  → 5000
T2: UPDATE orders SET total_amount=6000 WHERE id=1; COMMIT;
T1: SELECT total_amount FROM orders WHERE id=1;  → 6000  ← different!
Fix: use REPEATABLE READ — T1 sees a frozen snapshot from transaction start.
```

**Phantom Read:** Re-executing a range query returns additional rows inserted by T2.
```
T1: SELECT COUNT(*) FROM orders WHERE user_id=1;  → 3
T2: INSERT INTO orders (user_id, ...) VALUES (1, ...); COMMIT;
T1: SELECT COUNT(*) FROM orders WHERE user_id=1;  → 4  ← phantom row appeared!
Fix: use SERIALIZABLE — T1 and T2 execute as if they ran sequentially.
```

```sql
-- Set isolation level for a transaction:
BEGIN ISOLATION LEVEL REPEATABLE READ;
    SELECT total_amount FROM orders WHERE id = 1;  -- snapshot taken here
    -- ... other work ...
    SELECT total_amount FROM orders WHERE id = 1;  -- identical result guaranteed
COMMIT;

-- Serializable: may abort with error if conflict detected
BEGIN ISOLATION LEVEL SERIALIZABLE;
    -- If a conflicting concurrent transaction commits first:
    -- ERROR: could not serialize access due to concurrent update
    -- Application must catch this and retry the transaction.
COMMIT;
```

---

### MVCC — Multi-Version Concurrency Control

**The problem MVCC solves:** In a naive locking system, every read must acquire
a shared lock and every write must wait for all readers to finish. Under high
concurrency, everything grinds to a halt.

**MVCC's insight:** Instead of locking, keep multiple versions of each row.
Readers see the version that existed when their transaction started. Writers
create new versions. **Readers never block writers. Writers never block readers.**

```
Row versions in the heap — orders table, row id=1:

Version 1 │ status='PENDING'  │ xmin=100 │ xmax=200
           │ (created by T100, deleted/updated by T200)

Version 2 │ status='SHIPPED'  │ xmin=200 │ xmax=NULL
           │ (created by T200, still live — xmax=NULL means not yet deleted)

Visibility rules:
  A row version is visible to transaction T if:
    xmin ≤ T's snapshot XID     (row was created before my snapshot)
    AND (xmax IS NULL            (row has not been deleted/updated)
         OR xmax > T's snapshot XID)  (deletion happened after my snapshot)

Transaction 150 (started between T100 and T200 committing):
  → xmin=100 ≤ 150 ✓, xmax=200 > 150 ✓  →  sees Version 1: status='PENDING'

Transaction 250 (started after T200 committed):
  → Version 1: xmax=200 < 250  →  this version is "deleted" for T250, skip it
  → Version 2: xmin=200 ≤ 250 ✓, xmax=NULL ✓  →  sees status='SHIPPED'

Result: T150 and T250 read the same row simultaneously.
        T200 updates it simultaneously.
        Zero contention. No locks held.
```

**VACUUM:** Dead row versions accumulate (the old version is never immediately removed
because another transaction might still need to read it). PostgreSQL's background
`autovacuum` process periodically scans tables and reclaims dead tuple space.
Without VACUUM, tables grow indefinitely even if all rows are deleted.

```sql
-- Check dead tuple accumulation:
SELECT relname, n_live_tup, n_dead_tup,
       ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 1) AS dead_pct
FROM   pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Trigger manual vacuum (usually autovacuum handles this):
VACUUM ANALYZE orders;
```

---

### Locking Strategies

Two fundamental approaches: pessimistic (lock before reading) and
optimistic (detect conflicts at write time).

```sql
-- Pessimistic Locking: lock the row when you read it
-- Use when: contention is HIGH, write conflicts are frequent (seat booking, limited stock)
BEGIN;
  SELECT stock_count FROM products WHERE id = 1 FOR UPDATE;
  -- FOR UPDATE: no other transaction can modify this row until we COMMIT
  -- Other sessions trying SELECT FOR UPDATE on the same row will WAIT
  UPDATE products SET stock_count = stock_count - 1 WHERE id = 1;
COMMIT;

-- FOR UPDATE SKIP LOCKED: skip already-locked rows (job queue pattern)
SELECT * FROM tasks WHERE status = 'PENDING' LIMIT 1 FOR UPDATE SKIP LOCKED;
-- Returns the next unlocked pending task — perfect for concurrent workers
```

```java
// Optimistic Locking: no lock on read; verify version hasn't changed on write
// Use when: contention is LOW, reads are frequent, conflicts are rare
@Entity
public class UserProfile {
    @Id      private Long id;
    @Version private Long version;  // JPA manages this automatically
    private String bio;
}

// On save, JPA generates:
// UPDATE user_profiles SET bio=?, version=version+1 WHERE id=? AND version=?
//                                                          ↑
//                                                 version we read must still match
// If version changed between read and write: OptimisticLockException → retry
```

> 💡 **Interview:** "When do you use optimistic vs pessimistic locking?"
> Optimistic: low contention, most operations succeed, retry cost is low.
> E.g., editing a user profile — two users rarely edit at the same time.
> Pessimistic: high contention, write conflicts are frequent, retry is expensive.
> E.g., booking the last seat in an event — many users competing simultaneously.
> Optimistic also works across service boundaries (you cannot hold a database lock
> across an HTTP call to another microservice).

---

### WAL — Write-Ahead Log

The WAL is PostgreSQL's mechanism for both **atomicity** and **durability**.
It is a sequential append-only file on disk. Sequential writes are fast —
the WAL is written before any data page is modified.

```
Commit sequence:
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 1. App sends: UPDATE orders SET status='SHIPPED' WHERE id=1        │
  │ 2. PostgreSQL appends WAL record: "orders id=1: PENDING→SHIPPED"   │
  │ 3. PostgreSQL applies change to in-memory buffer page (dirty)       │
  │ 4. PostgreSQL fsync()s WAL file to disk                             │
  │ 5. PostgreSQL returns COMMIT SUCCESS to application                 │
  │                                                                     │
  │ [Asynchronously, later — checkpoint]:                               │
  │ 6. Modified buffer pages written to actual data files on disk       │
  └─────────────────────────────────────────────────────────────────────┘

Crash recovery (server restart after crash at any point):
  → Read WAL from last checkpoint
  → Redo all committed transactions whose data pages weren't flushed
  → Undo all uncommitted transactions
  → Database is consistent and complete
```


---

## Chapter 3: Redis

*PostgreSQL guarantees durability and consistency. The trade-off is latency:
a typical PostgreSQL query takes 1–50ms depending on data size, indexes, and
hardware. For data that changes slowly but is read thousands of times per second
— user sessions, product catalog, leaderboards — this is wasteful.
Redis stores data in RAM and serves most requests in 0.1–1ms: 10–100× faster.*

### Why Redis Exists

The architectural positioning:

```
Request arrives
      │
      ▼
  ┌────────┐        Cache HIT (0.1–1ms)
  │ Redis  │ ───────────────────────────► Response
  │ (RAM)  │
  └────────┘
      │ Cache MISS (first request or expired)
      │
      ▼
  ┌────────┐
  │  PG    │  5–50ms query
  │  DB    │ ───────────────────────────► Response + populate Redis
  └────────┘
```

**The trade-off:** Redis is volatile by default. If the Redis process dies
without persistence enabled, all cached data is lost. This is acceptable for
pure caches (data can be reloaded from PostgreSQL) but not for data that Redis
is the system of record for (e.g., rate-limit counters, distributed locks).
Chapter 3 covers persistence options for those use cases.

---

### The Five Data Structures

#### 1. STRING — The Universal Type

String is the simplest Redis type: one key maps to one value (text, number, or
binary, up to 512 MB). Numbers stored as strings support atomic increment/decrement.

```bash
# Basic SET and GET
SET  user:1:session "eyJhbGciOiJIUzI1NiJ9..."     # store JWT token
GET  user:1:session                                 # retrieve

# SET with expiry (TTL in seconds)
SET  user:1:session "eyJhbGciOiJIUzI1NiJ9..." EX 3600   # expires in 1 hour
SETEX user:1:session 3600 "eyJhbGciOiJIUzI1NiJ9..."      # equivalent

TTL    user:1:session    # seconds remaining (-1 = no expiry, -2 = missing/expired)
EXPIRE user:1:session 1800    # reset TTL to 30 minutes
PERSIST user:1:session        # remove TTL (make permanent)
DEL    user:1:session         # delete immediately

# Atomic integer counter — INCR is thread-safe: no race condition possible
SET    page:home:views 0
INCR   page:home:views        # returns 1 (read-increment-write as one atomic unit)
INCR   page:home:views        # returns 2
INCRBY page:home:views 5      # add 5 atomically → 7
DECR   stock:product:42       # decrement stock counter

# NX flag: SET only if key does NOT exist (atomic check-and-set)
SET lock:payment:order:123 "worker-uuid-abc" NX EX 30
# Returns OK if lock acquired, nil if already locked by another worker
```

> Use cases: session tokens, API rate limiting counters, feature flags,
> simple cached values, distributed counters, idempotency keys.

#### 2. HASH — Object Storage

A hash maps string fields to string values under one key.
Think of it as a JSON object, but with the ability to read or update one field
without fetching or deserializing the entire object.

```bash
# Store a user profile as a hash
HSET   user:1  name "Alice Johnson"  email "alice@example.com"  age "30"
HGET   user:1  name              # "Alice Johnson"
HMGET  user:1  name email        # ["Alice Johnson", "alice@example.com"]
HGETALL user:1                   # {name: Alice Johnson, email: alice@..., age: 30}
HDEL   user:1  age               # remove one field without touching others
HEXISTS user:1 email             # 1 (exists) or 0 (not present)
HSET   user:1  last_login "2024-01-15"  # add a new field without a full rewrite
HLEN   user:1                    # number of fields: 3

# Partial update without deserialization:
HSET user:1 age "31"             # update one field in O(1) — no GET needed first
```

> Use cases: user profiles, product metadata, session data with multiple fields,
> shopping carts (hash key = `cart:user:1`, fields = `product_id`, values = quantity).

#### 3. LIST — Ordered Sequences

A list is a doubly-linked list: O(1) push/pop at both ends, O(n) access by index.
It can function as a queue (RPUSH + LPOP) or a stack (LPUSH + LPOP).

```bash
# Append to right end (enqueue)
RPUSH activity:user:1 "logged_in"
RPUSH activity:user:1 "viewed_product_42"
RPUSH activity:user:1 "added_to_cart"

# Prepend to left end (most-recent-first prepend)
LPUSH notifications:user:1 "New order received"

# Read without removing (index 0 = first, -1 = last)
LRANGE activity:user:1 0 -1   # all items
LRANGE activity:user:1 0 9    # first 10 items (page 1 of a feed)
LLEN   activity:user:1        # item count

# Remove from ends
LPOP activity:user:1          # dequeue from left (FIFO queue: RPUSH + LPOP)
RPOP activity:user:1          # pop from right (LIFO stack: RPUSH + RPOP)

# Bounded list: keep only the N most recent items (critical for memory control)
RPUSH  recent:products:user:1 "42"
LTRIM  recent:products:user:1 0 49     # keep only 50 items; discard older ones

# Blocking pop: wait for up to 30 seconds for an item to appear
BLPOP queue:email:send 30     # worker blocks here; wakes up when a job is pushed
```

> Use cases: activity feeds (time-ordered), job queues (RPUSH + BLPOP worker),
> recent search history (LPUSH + LTRIM), chat message history (append + range).

#### 4. SET — Unique Collections

A set is an unordered collection that guarantees uniqueness.
`SISMEMBER` is O(1) — constant time regardless of set size.
Sets support union, intersection, and difference directly in Redis.

```bash
# Add members (duplicates silently ignored)
SADD product:1:tags "electronics" "laptop" "portable"
SADD product:2:tags "electronics" "accessory" "usb"

SISMEMBER product:1:tags "laptop"     # 1 (member)
SISMEMBER product:1:tags "furniture"  # 0 (not a member)
SMEMBERS  product:1:tags              # {electronics, laptop, portable} (unordered)
SCARD     product:1:tags              # 3 (count)
SREM      product:1:tags "portable"   # remove a member

# Set operations (stored into a new key):
SADD followers:user:1  "u:10" "u:20" "u:30"
SADD followers:user:2  "u:20" "u:30" "u:40"

SINTERSTORE mutual:1:2  followers:user:1  followers:user:2   # {u:20, u:30}
SUNIONSTORE all:1:2     followers:user:1  followers:user:2   # {u:10, u:20, u:30, u:40}
SDIFF       followers:user:1  followers:user:2               # {u:10} (in 1 but not 2)
SCARD       mutual:1:2   # how many mutual followers?
```

> Use cases: product tags, per-day unique visitors, mutual friends/followers,
> preventing duplicate email sends (`SADD sent:{campaign} {user_id}` → 0 means already sent).

#### 5. SORTED SET — Ranked Collections

A sorted set stores unique members each with a floating-point score.
Members are always ordered by score. Updates are O(log n).
You can query by rank (position) or by score range.

```bash
# Add members with scores
ZADD leaderboard 1500.0 "alice"
ZADD leaderboard 2200.0 "bob"
ZADD leaderboard 1800.0 "charlie"

# Query by rank (0 = lowest score)
ZRANGE    leaderboard 0 -1 WITHSCORES    # all, lowest first
ZREVRANGE leaderboard 0 9 WITHSCORES     # top 10, highest first

# Rank and score lookups
ZRANK     leaderboard "alice"     # 0-based rank, 0=lowest score → 0
ZREVRANK  leaderboard "bob"       # 0-based rank, 0=highest score → 0
ZSCORE    leaderboard "charlie"   # get score: 1800.0

# Atomic score update
ZINCRBY   leaderboard 300.0 "alice"   # alice's score: 1500→1800 (now ties charlie)

# Query by score range
ZRANGEBYSCORE leaderboard 1500 2000   # members with score 1500-2000
ZRANGEBYSCORE leaderboard -inf +inf   # all members (use instead of ZRANGE for clarity)
ZCOUNT    leaderboard 1500 2000       # count members in score range

# Remove
ZREM  leaderboard "alice"
ZPOPMIN leaderboard     # atomically remove and return member with lowest score
ZPOPMAX leaderboard     # atomically remove and return member with highest score
```

> Use cases: leaderboards (ZADD scores + ZREVRANGE for top-N), priority queues
> (ZADD with priority score + ZPOPMIN for next task), rate limiting sliding window,
> delayed job queues (ZADD with Unix timestamp as score + ZRANGEBYSCORE to find due jobs).

---

### Caching Patterns

#### Cache-Aside (Lazy Loading) — The Most Common Pattern

The application manages both the cache and the database.
On a miss, the application loads from the database and populates the cache.

```java
@Service
public class ProductService {

    @Autowired private ProductRepository   productRepo;
    @Autowired private RedisTemplate<String, Product> redis;

    private static final Duration TTL = Duration.ofMinutes(15);

    public Product getProduct(Long id) {
        String key = "product:" + id;

        // 1. Try the cache first (~0.1ms)
        Product cached = redis.opsForValue().get(key);
        if (cached != null) {
            return cached;   // Cache HIT — database never involved
        }

        // 2. Cache MISS — load from database (~10ms)
        Product product = productRepo.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));

        // 3. Populate cache for future requests (TTL prevents stale data)
        redis.opsForValue().set(key, product, TTL);

        return product;
    }

    public void updateProduct(Long id, ProductUpdateDTO dto) {
        // Update the database (source of truth)
        Product product = productRepo.findById(id).orElseThrow(...);
        productMapper.applyUpdate(product, dto);
        productRepo.save(product);

        // Invalidate the cache — next read will reload fresh data from DB
        redis.delete("product:" + id);
    }
}
```

Pros: only caches what's actually requested; cache survives Redis restart (DB is always available as fallback).
Cons: first request per key always hits the database (cold-start latency spike); potential staleness window between update and TTL expiry.

#### Read-Through — Cache Owns the Miss

The cache layer itself is responsible for loading from the database on a miss.
The application only ever talks to the cache.

```java
// Configured at the cache layer (Spring Cache + a CacheLoader):
@Cacheable(value = "products", key = "#id")
public Product getProduct(Long id) {
    // Spring Cache checks the cache first.
    // On MISS: this method body runs (loads from DB), result is stored in cache.
    return productRepo.findById(id).orElseThrow(...);
}
// Application code doesn't contain "check cache, load DB, populate cache" logic.
// The caching framework handles it transparently.
```

Pros: simpler application code; cache-loading logic lives in one place.
Cons: same cold-start miss as Cache-Aside; less flexibility for per-request customisation.

#### Write-Through — Cache and Database Always in Sync

Every write updates both the cache and the database in the same operation.
No stale reads possible — the cache is always current.

```java
public Product createProduct(CreateProductDTO dto) {
    Product saved = productRepo.save(mapper.toEntity(dto));
    // Write to cache immediately — future reads will hit cache, not DB
    redis.opsForValue().set("product:" + saved.getId(), saved, TTL);
    return saved;
}

public void updateProduct(Long id, ProductUpdateDTO dto) {
    Product updated = productRepo.save(...);
    redis.opsForValue().set("product:" + id, updated, TTL);  // keep cache fresh
}
```

Pros: cache always contains current data; zero stale reads after writes.
Cons: write latency doubles (two synchronous writes); cache may hold data never subsequently read.
Best for: objects that are read very frequently immediately after being written.

#### Write-Behind (Write-Back) — Async Database Writes

Write to the cache immediately and return to the caller.
A background process flushes the dirty data to the database asynchronously.

```java
public void updateProductPrice(Long id, BigDecimal newPrice) {
    // Update cache instantly (returns in <1ms)
    redis.opsForHash().put("product:" + id, "price", newPrice.toString());
    redis.opsForSet().add("dirty:products", id.toString());  // mark as dirty

    // Background job (runs every 100ms):
    // for each id in dirty:products → UPDATE products SET price=? WHERE id=?
}
```

Pros: extremely fast writes (memory only); can batch multiple writes.
Cons: **risk of data loss** if Redis crashes before the background flush.
Use only for non-critical data where loss is tolerable: view counts, analytics events,
non-transactional counters.

#### Cache Stampede / Thundering Herd Prevention

```
Problem:
  A popular cache key expires at T=0.
  10,000 concurrent requests all get a cache MISS simultaneously.
  All 10,000 query the database at the same time.
  Database is overwhelmed → cascade failure.

  ┌────────────┐   TTL=0    ┌──────────────┐  10,000 queries  ┌──────────┐
  │ 10,000 req │──────────► │ Redis: empty │ ────────────────► │ PG: 💥  │
  └────────────┘   MISS!    └──────────────┘                   └──────────┘
```

```java
// Solution: Mutex Lock — only ONE request rebuilds the cache
public Product getProductWithMutex(Long id) throws InterruptedException {
    String key     = "product:" + id;
    String lockKey = "lock:product:" + id;

    // 1. Fast path: try cache without lock
    Product cached = redis.opsForValue().get(key);
    if (cached != null) return cached;

    // 2. Slow path: race to acquire the rebuild lock
    Boolean acquired = redis.opsForValue()
        .setIfAbsent(lockKey, "1", Duration.ofSeconds(5));  // NX EX 5

    if (Boolean.TRUE.equals(acquired)) {
        try {
            // 3. We won the race — load from DB and populate cache
            Product product = productRepo.findById(id).orElseThrow(...);
            redis.opsForValue().set(key, product, Duration.ofMinutes(15));
            return product;
        } finally {
            redis.delete(lockKey);   // always release the lock
        }
    } else {
        // 4. We lost the race — someone else is rebuilding; wait and retry
        Thread.sleep(50);
        return getProductWithMutex(id);   // recursive retry (bounded by lock TTL)
    }
}
```

---

### Distributed Lock with Lua Script

```bash
# Acquire: SET key value NX EX seconds
# NX = only set if Not eXists (atomic check-and-set — no race between check and set)
# EX = auto-expire in N seconds (auto-release if lock holder crashes)
SET payment:lock:order:123 "worker-uuid-abc" NX EX 30
# Returns: OK (acquired) or nil (already locked)
```

```lua
-- Release: Lua script executes atomically (GET + conditional DEL in one step)
-- Without Lua: GET then DEL are two separate commands — another worker can
-- acquire the lock between our GET and our DEL, and we'd delete their lock.
local owner = redis.call("GET", KEYS[1])
if owner == ARGV[1] then
    return redis.call("DEL", KEYS[1])   -- it's still our lock → release it
else
    return 0   -- lock expired or acquired by another worker → don't touch it
end
```

```java
// Production: use Redisson (implements Redlock algorithm with Lua release)
RLock lock = redissonClient.getLock("payment:order:" + orderId);
try {
    boolean acquired = lock.tryLock(
        5,  TimeUnit.SECONDS,   // wait up to 5s to acquire
        30, TimeUnit.SECONDS    // auto-expire lock after 30s
    );
    if (acquired) {
        processPayment(orderId);
    } else {
        throw new LockAcquisitionException("Payment already being processed");
    }
} finally {
    if (lock.isHeldByCurrentThread()) {
        lock.unlock();   // Redisson uses the Lua release script internally
    }
}
```

> 💡 **Interview:** "Why do we need a Lua script to release a Redis lock?"
> Without Lua, releasing involves two commands: GET (check owner) + DEL (delete).
> Between GET and DEL, another process could acquire the lock (their EX expired the
> old key and they SET a new one). Our DEL would then delete their lock — a bug.
> Lua scripts run atomically in Redis (no other command executes between lines).
> The GET and DEL in the Lua script are an indivisible unit.

---

### HyperLogLog — Approximate Unique Counting

HyperLogLog counts unique values with only 12KB of memory regardless of
cardinality. Standard error: 0.81%. Perfect for analytics at scale.

```bash
# Add elements (duplicates automatically handled)
PFADD daily:visitors:2024-01-15 "user:1" "user:2" "user:3" "user:1"
PFCOUNT daily:visitors:2024-01-15   # returns 3 (user:1 counted once)

# Merge multiple HyperLogLogs (e.g., weekly from daily)
PFMERGE weekly:visitors:2024-W03 \
    daily:visitors:2024-01-15 \
    daily:visitors:2024-01-16 \
    daily:visitors:2024-01-17
PFCOUNT weekly:visitors:2024-W03   # approximate unique weekly visitors
```

```
Memory comparison for counting 10 million unique user IDs:

  Regular SET:   10,000,000 × ~20 bytes per ID = ~200MB
  HyperLogLog:   always exactly 12KB — 16,000× smaller

Trade-off: HyperLogLog gives you ~0.81% error.
  For 10M visitors, that's ±81,000 — acceptable for analytics dashboards.
  Not acceptable for billing or exact counts — use a SET or COUNT(DISTINCT) for those.
```

---

### Redis Persistence

```
RDB (Redis Database Dump — Point-in-Time Snapshot):
  How:  Forks the Redis process, serialises the entire dataset to a .rdb file
  When: Configurable intervals: save 60 10000 (if 10,000 changes in 60 seconds)
  Pro:  Compact binary file; fast restart (load one file); good for backups
  Con:  Data since the last snapshot is lost on crash (up to minutes of loss)

AOF (Append-Only File):
  How:  Every write command is appended to an aof file; replayed on restart
  When: Three fsync modes:
          always    → fsync after every write (safest, slowest: ~10k writes/sec)
          everysec  → fsync once per second (balanced: at most 1 second of loss)
          no        → OS decides when to fsync (fastest, least safe)
  Pro:  Minimal data loss (1 second max with everysec)
  Con:  Larger files; slower restart (replays all commands from the beginning)

Production recommendation:
  Enable BOTH:
    RDB for fast restarts and point-in-time backups
    AOF with everysec for durability (at most 1 second data loss)
  Redis 7+ supports RDB-AOF hybrid format (best of both)
```

---

### Redis Cluster

```
Consistent Hashing with 16,384 Hash Slots:

  Every key is assigned a slot: HASH_SLOT = CRC16(key) mod 16384
  Slots are distributed across nodes:
    Node A: slots    0 – 5460   (1/3 of keyspace)
    Node B: slots 5461 – 10922  (1/3)
    Node C: slots 10923 – 16383 (1/3)
  Each node has N replicas for fault tolerance.

  CLUSTER KEYSLOT orders:123   → 4792 → routed to Node A
  CLUSTER KEYSLOT product:42   → 7832 → routed to Node B

Client sends command to wrong node → MOVED redirection:
  Client → Node B: GET orders:123
  Node B → Client: MOVED 4792 192.168.1.10:6379
  Client → Node A: GET orders:123   (redirects and caches the mapping)

Hash tags force keys to the same slot (needed for multi-key operations):
  {user:1}:session   }
  {user:1}:cart      }  both hash on "user:1" → same slot → same node
  {user:1}:profile   }

Adding a new node (online, zero downtime):
  1. New node joins the cluster
  2. Admin reassigns a portion of slots to the new node
  3. Keys in those slots migrate atomically (one slot at a time)
  4. Clients are redirected transparently via MOVED responses
```

---

## Chapter 4: Database Migrations with Flyway

### Why Migrations Are Non-Negotiable

**Without migrations:**
- Each developer's local database drifts in structure over time.
- "It works on my machine" becomes a schema issue, not just a code issue.
- Production deployments require manual SQL execution — a human error risk.
- Rolling back a bad schema change is undocumented and inconsistent.

**With Flyway:**
- Every environment runs the same versioned SQL scripts in the same order.
- The schema lives in Git, reviewed in PRs, tested in CI.
- Flyway tracks exactly which scripts have been applied in `flyway_schema_history`.
- Running `flyway migrate` is idempotent — safe to run multiple times.

---

### Spring Boot Integration

```xml
<!-- pom.xml: add Flyway dependency -->
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-database-postgresql</artifactId>
</dependency>
```

```yaml
# application.yml
spring:
  datasource:
    url:      jdbc:postgresql://localhost:5432/orderdb
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  flyway:
    enabled:             true
    locations:           classpath:db/migration
    baseline-on-migrate: true    # for databases that predate Flyway
    validate-on-migrate: true    # verify checksums match before running
  jpa:
    hibernate:
      ddl-auto: validate         # Flyway owns the schema; Hibernate only validates
```

**Migration file naming convention:**

```
src/main/resources/db/migration/
  V1__init_schema.sql             ← V{version}__{description}.sql
  V2__add_product_sku.sql             two underscores between version and name
  V3__add_order_tracking.sql
  V4__create_audit_log_table.sql
  R__update_product_summary_view.sql  ← R__{name}.sql (repeatable — re-runs on change)
```

```sql
-- V1__init_schema.sql
CREATE TABLE users (
    id         BIGSERIAL    PRIMARY KEY,
    email      VARCHAR(255) UNIQUE NOT NULL,
    username   VARCHAR(50)  UNIQUE NOT NULL,
    created_at TIMESTAMP    NOT NULL DEFAULT NOW()
);
CREATE TABLE products (id BIGSERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, price DECIMAL(10,2));
CREATE TABLE orders   (id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users(id));
CREATE TABLE order_items (id BIGSERIAL PRIMARY KEY, order_id BIGINT NOT NULL REFERENCES orders(id));

-- V2__add_product_sku.sql
ALTER TABLE products ADD COLUMN sku VARCHAR(50);
CREATE UNIQUE INDEX idx_products_sku ON products(sku);

-- V3__add_order_tracking.sql
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100);
ALTER TABLE orders ADD COLUMN shipped_at      TIMESTAMP;
```

Flyway records every applied migration in `flyway_schema_history`:

```sql
SELECT version, description, installed_on, execution_time, success
FROM   flyway_schema_history
ORDER BY installed_rank;

-- version | description          | installed_on        | execution_time | success
-- 1       | init schema          | 2024-01-10 09:00:00 | 234            | true
-- 2       | add product sku      | 2024-01-15 14:22:00 | 45             | true
-- 3       | add order tracking   | 2024-02-01 10:05:00 | 38             | true
```

---

### Zero-Downtime Migration Patterns

**Pattern 1 — Adding a NOT NULL column to a large table**

```sql
-- WRONG: locks the entire table for the duration of the backfill
-- On a table with 10M rows this could take minutes — full downtime.
ALTER TABLE orders ADD COLUMN region VARCHAR(50) NOT NULL DEFAULT 'INDIA';
```

**The safe approach: three migrations across three deployments.**

```sql
-- Migration V10: add the column as nullable (instant — no row rewriting)
ALTER TABLE orders ADD COLUMN region VARCHAR(50);
```

```
Deploy App v2: code writes `region` on all new inserts, reads it with a fallback.
```

```sql
-- Migration V11: backfill existing rows (run in batches to avoid long locks)
DO $$
DECLARE
    batch_size INT := 10000;
    rows_updated INT;
BEGIN
    LOOP
        UPDATE orders
        SET    region = 'INDIA'
        WHERE  region IS NULL
        AND    ctid IN (
            SELECT ctid FROM orders WHERE region IS NULL LIMIT batch_size
        );
        GET DIAGNOSTICS rows_updated = ROW_COUNT;
        EXIT WHEN rows_updated = 0;
        PERFORM pg_sleep(0.1);  -- brief pause between batches
    END LOOP;
END $$;
```

```sql
-- Migration V12: now all rows have a value; add NOT NULL safely
ALTER TABLE orders ALTER COLUMN region SET NOT NULL;
ALTER TABLE orders ALTER COLUMN region SET DEFAULT 'INDIA';
```

**Pattern 2 — Renaming a column (never rename directly)**

A direct `RENAME COLUMN` breaks running application code instantly.

```sql
-- Step 1 (V20): add the new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(100);
```
```
Deploy App v2: writes to BOTH old column and new full_name.
               Reads from new full_name with fallback to old.
```
```sql
-- Step 2 (V21): backfill
UPDATE users SET full_name = first_name || ' ' || last_name WHERE full_name IS NULL;
ALTER TABLE users ALTER COLUMN full_name SET NOT NULL;
```
```
Deploy App v3: reads exclusively from full_name. Old columns never referenced.
```
```sql
-- Step 3 (V22): drop the old columns (after verifying no code reads them)
ALTER TABLE users DROP COLUMN first_name;
ALTER TABLE users DROP COLUMN last_name;
```

**Pattern 3 — Adding an index without locking**

```sql
-- WRONG: locks the table while building the index — potentially minutes of downtime
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- CORRECT: builds the index without holding a table lock
-- Reads and writes continue normally during the build (takes longer to complete)
CREATE INDEX CONCURRENTLY idx_orders_created_at ON orders(created_at);

-- Note: CONCURRENTLY cannot run inside a transaction block (BEGIN...COMMIT)
-- It must be a standalone statement.
```

> 💡 **Interview:** "How do you add a NOT NULL column to a 50M-row production table?"
> Three deployments: (1) add as nullable, (2) backfill in batches, (3) add NOT NULL.
> Never in one step — `ALTER TABLE ADD COLUMN NOT NULL DEFAULT` rewrites every row
> while holding an exclusive lock. For large tables that means minutes of full downtime.

---

## Chapter 5: NoSQL Fundamentals

### When NOT to Use PostgreSQL

PostgreSQL handles the vast majority of workloads. Consider NoSQL when:

| Signal | Consider |
|--------|----------|
| >50,000 writes/sec, single-node PostgreSQL saturated | Cassandra, DynamoDB |
| Schema changes every sprint, migration overhead is a bottleneck | MongoDB |
| Data is naturally document-shaped (nested, variable per record) | MongoDB |
| Multi-region active-active writes required | Cassandra, DynamoDB |
| Time-series at scale (billions of sensor readings) | InfluxDB, TimescaleDB |
| Full-text search with relevance ranking | Elasticsearch |

Relational databases win when you need: ACID transactions, complex joins,
ad-hoc queries, a stable schema, or referential integrity enforcement.

---

### MongoDB — Document Store

MongoDB stores BSON (Binary JSON) documents. Each document in a collection
can have a different shape — no fixed schema. Related data is often *embedded*
inside a document instead of normalised into separate tables (avoiding JOINs).

```javascript
// Insert a product with nested attributes — no schema declaration needed
db.products.insertOne({
  _id: ObjectId("507f1f77bcf86cd799439011"),
  name: "Laptop",
  price: 75000,
  attributes: {             // nested object — queried as "attributes.ram"
    brand: "ThinkPad",
    ram:   "16GB",
    storage: "512GB SSD"
  },
  tags: ["electronics", "laptop"],   // multi-valued array
  reviews: [                          // embedded array of sub-documents
    { user: "alice", rating: 5, comment: "Excellent!" },
    { user: "bob",   rating: 4 }
  ]
});

// Query with nested document field:
db.products.find({ "attributes.ram": "16GB", price: { $lt: 80000 } });

// Query inside an array:
db.products.find({ "reviews.rating": { $gte: 4 } });

// Aggregation pipeline: MongoDB's equivalent of GROUP BY + JOINs
db.orders.aggregate([
  { $match:  { status: "DELIVERED" } },                           // WHERE
  { $group:  {
      _id:   "$user_id",
      total: { $sum: "$total_amount" },
      count: { $sum: 1 }
  }},                                                             // GROUP BY
  { $sort:   { total: -1 } },                                     // ORDER BY
  { $limit:  10 }                                                  // LIMIT
]);

// $lookup: the MongoDB equivalent of JOIN
db.orders.aggregate([
  { $lookup: {
      from:         "users",
      localField:   "user_id",
      foreignField: "_id",
      as:           "user"
  }},
  { $unwind: "$user" }
]);
```

**When to choose MongoDB:**
- Product catalogs (different attributes per category — Electronics has RAM; Furniture has dimensions)
- CMS (articles with variable structure — not all articles have a video embed)
- Event logs (each event type carries different fields)
- User-generated content where schema evolves every sprint

**MongoDB indexing:**

```javascript
// Single field index
db.products.createIndex({ price: -1 });   // -1 = descending

// Compound index (left-prefix rule applies — same as PostgreSQL B-tree)
db.orders.createIndex({ user_id: 1, created_at: -1 });

// Text index for full-text search
db.products.createIndex({ name: "text", description: "text" });
db.products.find({ $text: { $search: "gaming laptop" } });
```

---

### Cassandra — Wide-Column Store

Cassandra is designed for massive write throughput and horizontal scale.
Its fundamental design constraint: **every query must include the partition key**.

```sql
-- Cassandra CQL (SQL-like syntax, very different execution model)

-- DESIGN RULE: schema is driven by your query access patterns, NOT entity relationships.
-- Ask: "What queries will I run?" THEN design the table.

-- Access pattern: "Get all orders for a user, sorted by date, most recent first"
CREATE TABLE orders_by_user (
    user_id    UUID,
    order_date TIMESTAMP,
    order_id   UUID,
    status     TEXT,
    total      DECIMAL,
    PRIMARY KEY (user_id, order_date, order_id)
);
-- PRIMARY KEY breakdown:
--   user_id    = partition key   → determines which node stores these rows
--   order_date = clustering key  → rows within a partition sorted by this
--   order_id   = additional clustering key for uniqueness

-- This query is optimised (partition key provided):
SELECT * FROM orders_by_user
WHERE user_id = ?
ORDER BY order_date DESC
LIMIT 20;

-- This query is FORBIDDEN in production (no partition key → full cluster scan):
SELECT * FROM orders_by_user WHERE status = 'DELIVERED';
-- Solution: create a SEPARATE table for this access pattern

CREATE TABLE orders_by_status (
    status     TEXT,
    order_date TIMESTAMP,
    user_id    UUID,
    order_id   UUID,
    PRIMARY KEY (status, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC);

-- When inserting an order, write to BOTH tables:
INSERT INTO orders_by_user   (user_id, order_date, order_id, status, total) VALUES (...);
INSERT INTO orders_by_status (status, order_date, user_id, order_id, total) VALUES (...);
-- This is Cassandra's denormalisation trade-off: multiple tables for multiple access patterns.
```

**Consistency levels:**

```
Replication Factor (RF) = 3: each row is stored on 3 nodes

Consistency Level | Reads from | Guarantees
──────────────────┼────────────┼───────────────────────────────────
ONE               | 1 replica  | Fastest; may read stale data
QUORUM            | 2 replicas | Balanced (RF/2 + 1); tolerates 1 node down
ALL               | 3 replicas | Slowest; most consistent; fails if any node down

Strong consistency trick:
  Write at QUORUM + Read at QUORUM
  → Overlap guaranteed: at least one node has the latest write
```

**When to choose Cassandra:**
- IoT sensor readings, application metrics, click streams (time-series, append-heavy)
- Multi-region active-active (Cassandra natively replicates across data centres)
- When eventual consistency is acceptable and write throughput matters most

---

### CAP Theorem — The Theoretical Foundation

Eric Brewer's CAP theorem: in the presence of a **network partition** (nodes
cannot communicate), a distributed system must choose between **Consistency**
and **Availability**. It cannot have both.

```
           Consistency (C)
           Every read gets the most
           recent write or an error
                   /\
                  /  \
                 / CP \     PostgreSQL + synchronous replication
                /      \    HBase, Zookeeper
               /────────\
              /    CA    \   Single-node RDBMS (no partition possible)
             / (single   \
            /   node)     \
           /────────────────\
          /        AP        \   Cassandra, DynamoDB, CouchDB
         /  Available during  \
        /  partition; eventual \
       /  consistency          \
      ─────────────────────────
     Partition Tolerance (P)
     System continues despite
     network splits

You must always have P in a distributed system — networks fail.
So the real choice is: C or A when a partition occurs.
```

| Database | CAP Position | Behaviour During Partition |
|----------|-------------|---------------------------|
| PostgreSQL (primary) | CP | Refuses writes to non-primary; may be unavailable |
| Cassandra | AP | Serves reads and writes from both sides; eventual consistency |
| Redis Cluster | AP (reads) / CP (writes) | Reads from replica (may be stale); writes to primary |
| DynamoDB | AP by default | Serves eventually-consistent reads; strong consistency optional per-read |

> 💡 **Interview:** "You're designing an order history service that must handle
> 500,000 writes/second globally. Which database and why?"
>
> "Cassandra. Order history is append-heavy (new orders only), queries are
> always by user_id (the natural partition key), and we can tolerate eventual
> consistency — a user seeing their order appear 200ms after placing it is fine.
> Cassandra's AP model gives us availability during network partitions and
> linear write scalability by adding nodes. PostgreSQL could not absorb 500K
> writes/second on a single primary, and sharding PostgreSQL manually is complex."
>
> This is the quality of answer that distinguishes an SDE-2 from an SDE-1.
> You named the technology, justified it against the requirement, and explained
> what you give up (eventual consistency) and why that's acceptable here.

---

## Appendix: SDE-2 Interview Cheat Sheet

### SQL

| Concept | One-Line Answer |
|---------|----------------|
| WHERE vs HAVING | WHERE filters rows before grouping; HAVING filters groups after aggregation |
| INNER vs LEFT JOIN | INNER: only matching rows; LEFT: all left rows, NULLs where no match |
| RANK vs DENSE_RANK | RANK skips after ties (1,1,3); DENSE_RANK never skips (1,1,2) |
| ROW_NUMBER | Unique sequential number per partition — never ties, always 1,2,3... |
| EXISTS vs IN | EXISTS short-circuits on first match; IN materialises the full subquery result |
| NOT IN with NULLs | Danger: if subquery returns any NULL, NOT IN returns zero rows. Use NOT EXISTS. |
| SQL execution order | FROM → WHERE → GROUP BY → aggregates → HAVING → SELECT → ORDER BY → LIMIT |
| CTE vs subquery | Same performance in PostgreSQL; CTE is more readable and reusable in one query |
| Recursive CTE | Anchor UNION ALL recursive case; needs depth limit to prevent infinite loop |

### Database Internals

| Concept | One-Line Answer |
|---------|----------------|
| B-tree height | Height = log₁₀₀(n); 100M rows = height 4; always 3-5 disk reads |
| Left-prefix rule | Composite index (a,b,c) usable by queries on a, a+b, a+b+c — not b or c alone |
| Covering index | Index contains all columns the query needs → Index Only Scan, zero heap reads |
| MVCC | Readers see row versions from their snapshot; writers create new versions; no reader-writer locks |
| VACUUM | Removes dead tuple versions accumulated by MVCC; without it tables grow unboundedly |
| Optimistic locking | Version column: update WHERE version=read_version; 0 rows = conflict, retry |
| Pessimistic locking | SELECT FOR UPDATE: holds row lock until COMMIT; use FOR SKIP LOCKED for queues |
| WAL purpose | Enables atomicity (rollback uncommitted) and durability (replay committed on crash) |
| When seq scan beats index | When query returns > ~5-10% of table rows (random I/O for index > sequential scan) |

### Redis

| Concept | One-Line Answer |
|---------|----------------|
| Why Redis is fast | All data in RAM + single-threaded (no lock overhead) + I/O multiplexing |
| Single-threaded why? | No lock contention; commands are atomic; blocked by I/O multiplexing not threads |
| STRING INCR | Atomic read-increment-write; no race condition; used for counters and rate limiting |
| HASH vs STRING | HASH allows partial field updates; STRING requires deserialise-modify-reserialise the whole object |
| ZADD use cases | Leaderboard, priority queue, delayed jobs (score = timestamp), rate limiting sliding window |
| Cache-Aside | App: check cache → miss → query DB → populate cache. Most common pattern. |
| Write-Through | Every write updates both cache and DB; cache always fresh; double write latency |
| Write-Behind | Write cache immediately, flush to DB async; fast writes; risk of data loss on Redis crash |
| Cache stampede | Many concurrent misses → all hit DB. Fix: mutex lock or probabilistic early expiry |
| Distributed lock | SET key value NX EX ttl; release with Lua script (check owner before DEL) |
| HyperLogLog | Approximate unique count in 12KB regardless of cardinality; 0.81% error |
| RDB vs AOF | RDB: compact snapshot, data loss risk; AOF: every write logged, minimal loss |

### NoSQL and CAP

| Concept | One-Line Answer |
|---------|----------------|
| CAP theorem | During partition: choose Consistency (reject requests) or Availability (serve stale data) |
| PostgreSQL CAP | CP — refuses writes to non-primary; data never stale but may be unavailable |
| Cassandra CAP | AP — serves from both sides during partition; eventual consistency |
| Cassandra partition key | Determines which node stores the row; every query must include it |
| Cassandra clustering key | Sort order within a partition; can range-scan within a partition |
| MongoDB vs PostgreSQL | MongoDB: flexible schema, embedded docs, variable structure; PG: ACID, joins, stability |
| When to use NoSQL | >50K writes/sec, schema evolves rapidly, data is document-shaped, multi-region active-active |
| Zero-downtime column add | (1) Add nullable, (2) backfill in batches, (3) add NOT NULL — three separate deployments |
| Index CONCURRENTLY | Builds index without table lock; reads and writes continue; must be outside transaction |
