# Chapter 9: Flyway and Database Migrations in Spring Boot

## 9.1 The problem with `ddl-auto: update`

Throughout the book we've used `spring.jpa.hibernate.ddl-auto: update`, which tells Hibernate to inspect the entity mappings at startup and issue `ALTER TABLE` statements to bring the schema in line with what the entities describe. For a tutorial, this is convenient — you add a field to an entity, the column appears in the table the next time you start the app. In production, it's a trap:

**It can drop data.** If you rename a field in your entity, Hibernate sees "old column gone, new column needed" and may issue `DROP COLUMN old_name; ADD COLUMN new_name`. The data in the old column is gone.

**It can't express complex transformations.** Splitting one column into two, migrating data from one table to another, adding an index on a specific subset of rows — these operations cannot be expressed by Hibernate's schema-update mechanism at all.

**It's not repeatable or auditable.** There's no record of what changes were made or when. "What does the schema look like on the production database right now?" is genuinely hard to answer.

**It's not safe for multiple instances.** Two instances of the application starting simultaneously could both try to `ALTER TABLE` at the same time, producing a race condition.

The industry solution is **migration files** — versioned, numbered SQL scripts that each make one schema change, executed in order, exactly once, tracked in a metadata table, and never modified after being committed.

## 9.2 Adding Flyway

```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-database-postgresql</artifactId>
</dependency>
```

That's the entire addition. Spring Boot auto-configures Flyway when it finds:
- `flyway-core` on the classpath
- A configured `DataSource`
- Migration files in the default location (`classpath:db/migration`)

At startup — before Hibernate validates or the application accepts requests — Flyway:
1. Connects to the database.
2. Reads the `flyway_schema_history` table (creating it if this is the first run).
3. Finds every applied migration's checksum in that table.
4. Scans `classpath:db/migration` for pending migration files.
5. Executes each pending migration in version order, recording the result in the history table.
6. If any migration fails, it marks it as failed and throws an exception — Spring Boot startup aborts, the application never becomes ready, and the failed migration state is visible in the history table for debugging.

Change `application.yml` to use `validate` instead of `update`:

```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: validate   # Hibernate checks schema matches entities; NEVER modifies it
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: false  # true only if applying Flyway to an existing non-empty schema
```

## 9.3 Migration file naming convention

```
V{version}__{description}.sql
│                │
│                └── Human-readable description; spaces become underscores
└── Version number: integer, can use dots for sub-versions (V1.1, V1.2, ...)
```

Flyway executes files in version order and errors if a file that was previously applied has been modified (checksum mismatch) — this enforces the immutability guarantee: once a migration is committed and deployed, it's permanent. If you need to undo a change, you add a new migration that reverses it; you never edit the original.

```
src/main/resources/db/migration/
├── V1__create_initial_schema.sql
├── V2__add_idempotency_records_table.sql
├── V3__add_order_status_index.sql
├── V4__add_product_search_index.sql
└── V5__rename_users_display_name.sql
```

## 9.4 The complete initial migration

This replaces Hibernate's auto-created tables with explicit, controlled SQL:

**`src/main/resources/db/migration/V1__create_initial_schema.sql`**
```sql
-- Users table
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    username    VARCHAR(50) NOT NULL UNIQUE,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        VARCHAR(20) NOT NULL CHECK (role IN ('CUSTOMER', 'ADMIN')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Products table
CREATE TABLE products (
    id          BIGSERIAL PRIMARY KEY,
    sku         VARCHAR(50) NOT NULL UNIQUE,
    name        VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    price       NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Inventory table (one row per product)
CREATE TABLE inventory (
    id                  BIGSERIAL PRIMARY KEY,
    product_id          BIGINT NOT NULL UNIQUE REFERENCES products(id),
    quantity_available  INTEGER NOT NULL CHECK (quantity_available >= 0),
    version             BIGINT NOT NULL DEFAULT 0   -- optimistic locking token
);

-- Orders table
CREATE TABLE orders (
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT NOT NULL REFERENCES users(id),
    status       VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                     CHECK (status IN ('PENDING','CONFIRMED','SHIPPED','DELIVERED','CANCELLED')),
    total_amount NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
    version      BIGINT NOT NULL DEFAULT 0,         -- optimistic locking token
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Order items table
CREATE TABLE order_items (
    id          BIGSERIAL PRIMARY KEY,
    order_id    BIGINT NOT NULL REFERENCES orders(id),
    product_id  BIGINT NOT NULL REFERENCES products(id),
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0)
);

-- Idempotency records table
CREATE TABLE idempotency_records (
    idempotency_key VARCHAR(100) PRIMARY KEY,
    response_body   TEXT NOT NULL,
    http_status     INTEGER NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes: covering the most frequent queries from Chapter 4
CREATE INDEX idx_orders_user_id        ON orders(user_id);
CREATE INDEX idx_orders_status         ON orders(status);
CREATE INDEX idx_orders_created_at     ON orders(created_at DESC);
CREATE INDEX idx_order_items_order_id  ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_inventory_product_id  ON inventory(product_id);

-- Automatic updated_at maintenance (PostgreSQL trigger function)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

**`src/main/resources/db/migration/V2__add_idempotency_expiry_index.sql`**
```sql
-- Allow efficient cleanup of old idempotency records
CREATE INDEX idx_idempotency_created_at ON idempotency_records(created_at);
```

**`src/main/resources/db/migration/V3__add_product_full_text_search.sql`**
```sql
-- PostgreSQL full-text search index on product name + description
-- This enables much faster ILIKE-equivalent search via tsvector
ALTER TABLE products
    ADD COLUMN search_vector TSVECTOR
        GENERATED ALWAYS AS (
            to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))
        ) STORED;

CREATE INDEX idx_products_search ON products USING GIN(search_vector);
```

## 9.5 Zero-downtime migration strategies

When deploying a schema change to a live production system, the goal is to avoid any downtime and avoid any window where the schema is inconsistent with the running code. The hard constraint: Flyway runs the migration *at the start of the new application instance*, but the *old instances are still running* against the old schema for however long the rolling deployment takes.

The fundamental rule: **schema changes must be backward-compatible with the previous version of the code**. A migration that adds a new optional column with a default is safe — old code ignores the column, new code uses it. A migration that renames or drops a column that old code is still referencing is not safe.

The standard approach for breaking changes is a **three-phase expand-contract migration**:

**Phase 1 — Expand (safe for old and new code)**
```sql
-- V10__add_display_name_column.sql
-- Adds the new column. Old code ignores it; new code can write to it.
ALTER TABLE users ADD COLUMN display_name VARCHAR(100);
UPDATE users SET display_name = username WHERE display_name IS NULL;
```
Deploy new code that *reads from new column if populated, falls back to old*. Also writes to both old and new for a transition period.

**Phase 2 — Migrate data (after all instances run new code)**
```sql
-- V11__backfill_display_name.sql
-- All instances are now on new code. Ensure all rows are backfilled.
UPDATE users SET display_name = username WHERE display_name IS NULL;
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;
```

**Phase 3 — Contract (after Phase 2 is fully deployed)**
Deploy code that only reads from the new column. After all instances are updated, remove the old column:
```sql
-- V12__drop_username_column.sql
-- Old code is fully gone. Safe to remove the old column now.
ALTER TABLE users DROP COLUMN username;
```

This three-deployment approach trades speed for safety. For a small team or a low-traffic API, you might compress phases 1 and 2 — but for any system where old instances are running while new ones are deploying, the three-phase structure is the only genuinely zero-downtime approach.

**Adding a non-null column** deserves specific treatment because it's a common gotcha: `ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(50) NOT NULL` immediately fails if any existing rows are present (they'd violate the `NOT NULL` constraint). The safe sequence is always: add the column as nullable, backfill it, then add the constraint:

```sql
-- V13__add_tracking_number.sql
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(50);
UPDATE orders SET tracking_number = 'UNKNOWN-' || id::text WHERE tracking_number IS NULL;
ALTER TABLE orders ALTER COLUMN tracking_number SET NOT NULL;
```

**Adding an index on a large table** should use `CREATE INDEX CONCURRENTLY` in PostgreSQL — the non-concurrent form takes an exclusive lock that blocks reads and writes on the table for the duration of the index build, which can be minutes. The concurrent form takes a much lighter lock, allowing reads and writes to continue. The trade-off is that concurrent index creation takes longer and cannot run inside a transaction. Because Flyway wraps each migration in a transaction by default, this requires `flyway.mixed=true` (allowing non-transactional statements in a migration) or splitting the index creation into its own migration marked with a special comment:

```sql
-- V4__add_product_search_index.sql
-- flyway:executeInTransaction=false
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_name ON products(name);
```

> **Interview Question — SDE-2:** "How does Flyway prevent two instances of the application from running the same migration simultaneously when they all start at the same time?"
>
> **Answer:** Flyway acquires a **database-level advisory lock** (or, depending on the database, a row-level lock on the `flyway_schema_history` table itself) at the start of the migration process. In PostgreSQL, it uses `SELECT pg_try_advisory_lock(?)` — a session-scoped lock that only one connection can hold at a time. The first instance to start acquires the lock, runs any pending migrations, and releases the lock. Any other instance that starts simultaneously blocks on the lock acquisition until the first one finishes, then re-reads the history table, finds no pending migrations, and proceeds to start normally. This is a real distributed lock — it works even if instances are on different machines — because the lock lives in the database, not in JVM memory. If the first instance crashes mid-migration, PostgreSQL automatically releases the lock when the connection is closed, allowing a subsequent instance to pick up and potentially detect the failed migration in the history table.

---

The API is now built on a properly version-controlled schema. Chapter 10 is the last chapter: making the Swagger UI publicly accessible so that the "try it live" link in your README actually works, and deploying the application so anyone can call your API from the internet.
