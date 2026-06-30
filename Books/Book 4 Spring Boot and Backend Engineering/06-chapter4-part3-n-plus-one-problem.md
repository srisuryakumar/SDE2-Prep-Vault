# Chapter 4 (Part 3 of 6): The N+1 Problem

The N+1 problem is the single most commonly encountered performance issue in JPA applications, and also the one most commonly missed until it's causing actual production problems — because it produces correct results and is invisible unless you're watching the SQL. This chapter section is dedicated to it entirely: reproducing it deliberately so you can recognize the symptoms, understanding precisely why Hibernate generates those extra queries, and applying each of three different fixes, so you know which one to reach for in which situation.

## 4.11 Reproducing the problem

The setup: 10 orders in the database, each placed by a different user. We want to display a summary of each order (order ID, status, total amount, user email). The naive implementation:

```java
// In OrderService (simplified for the demo)
public List<OrderSummary> listAllOrders() {
    List<Order> orders = orderRepository.findAll();  // ← Query #1: SELECT * FROM orders LIMIT 10
    
    return orders.stream()
            .map(order -> new OrderSummary(
                    order.getId(),
                    order.getStatus(),
                    order.getTotalAmount(),
                    order.getUser().getEmail()  // ← Triggers Query #2 through #11: one per order
            ))
            .toList();
}
```

With `spring.jpa.show-sql=true` and `org.hibernate.SQL: DEBUG`, the console output reveals:

```sql
-- Query 1: load the orders
SELECT o.id, o.status, o.total_amount, o.user_id, o.created_at, ...
FROM orders o
LIMIT 10;

-- Query 2: load user for order 1
SELECT u.id, u.username, u.email, ...
FROM users u
WHERE u.id = 1;

-- Query 3: load user for order 2
SELECT u.id, u.username, u.email, ...
FROM users u
WHERE u.id = 2;

-- ... 8 more queries, one per order
```

**1 query for the list + N queries for the related entities = N+1 queries total**. For 10 orders: 11 queries. For 1,000 orders: 1,001 queries. The query count scales linearly with the number of parent rows — which is exactly what you don't want.

Why does this happen? Because `Order.user` is mapped with `fetch = FetchType.LAZY` (as it should be). When `findAll()` loads the orders, Hibernate populates a *proxy* object for `user` on each one — a thin wrapper that knows the `user_id` foreign key value (it's in the `orders` row, so Hibernate already has it) but hasn't actually queried the `users` table yet. The moment the code calls `.getUser().getEmail()`, Hibernate realizes "I need to materialize this proxy," fires a `SELECT` against the `users` table for that specific `id`, and returns the real `User` object. Once per order. Every time.

The fact that `User` objects are likely duplicated across many orders (two orders could belong to the same user) is irrelevant — Hibernate fires a new query per-order, not per-unique-user, unless you teach it otherwise.

## 4.12 Fix 1: JOIN FETCH

The most direct fix: tell Hibernate, in the JPQL query itself, to load the association in the same query as the parent:

```java
// Already in OrderRepository from Part 2:
@Query("""
        SELECT DISTINCT o FROM Order o
        LEFT JOIN FETCH o.items i
        LEFT JOIN FETCH i.product
        WHERE o.id = :orderId
        """)
Optional<Order> findByIdWithItemsAndProducts(@Param("orderId") Long orderId);
```

A plain `JOIN FETCH` in JPQL generates a SQL `LEFT OUTER JOIN`, loading both the `Order` and its `items` collection (and each item's `product`) in a single round-trip to the database:

```sql
SELECT DISTINCT o.id, o.status, o.total_amount, ...,
                i.id, i.quantity, i.unit_price, ...,
                p.id, p.sku, p.name, ...
FROM orders o
LEFT OUTER JOIN order_items i ON i.order_id = o.id
LEFT OUTER JOIN products p    ON p.id = i.product_id
WHERE o.id = 7;
```

**One query** for the order, its items, and each item's product — regardless of how many items the order has.

The `DISTINCT` is necessary because a SQL join over a one-to-many relationship produces *duplicate rows* for the parent — a 3-item order produces 3 rows, all with the same `orders` columns. Without `DISTINCT`, Hibernate would map those 3 rows into 3 separate `Order` objects in the Java result instead of one `Order` with 3 items. The `DISTINCT` in JPQL instructs Hibernate to deduplicate at the Java object graph level (not necessarily in the generated SQL, though Hibernate often does add `SELECT DISTINCT` in SQL too).

**When to use JOIN FETCH:** point queries (looking up a single entity by ID) and queries where you *know* the calling code will always need the full associated data. It's the most explicit and most efficient fix — one query, all the data — but it lacks flexibility: you can't reuse the same query for a "just give me the order status, don't load items" code path.

**The JOIN FETCH + pagination problem.** There's a well-known and dangerous trap when you combine `JOIN FETCH` on a collection (`@OneToMany`) with `Pageable` (SQL `LIMIT`/`OFFSET`). Consider:

```java
// DON'T do this:
@Query("""
        SELECT DISTINCT o FROM Order o
        LEFT JOIN FETCH o.items
        WHERE o.user.id = :userId
        """)
Page<Order> findByUserIdWithItems(Long userId, Pageable pageable); // ← Problem
```

When you join `Order` to its `items` collection, the SQL result has *multiple rows per order* (one per item). Applying `LIMIT 20` to that multi-row result doesn't paginate by 20 *orders* — it paginates by 20 *join rows*, potentially splitting an order's items across page boundaries and producing partial, inconsistent results. Hibernate detects this situation, **loads all matching rows into memory** and paginates in Java, and emits a warning that should never be ignored:

```
HHH90003004: firstResult/maxResults specified with collection fetch; applying in memory
```

The correct fix for paginating a list of orders *with their items already loaded*:

```java
// Step 1: Get the paged IDs only (no join, clean pagination)
@Query(value = "SELECT o.id FROM orders o WHERE o.user_id = :userId ORDER BY o.created_at DESC",
       countQuery = "SELECT COUNT(*) FROM orders WHERE user_id = :userId",
       nativeQuery = true)
Page<Long> findOrderIdsByUserId(@Param("userId") Long userId, Pageable pageable);

// Step 2: Fetch those orders with JOIN FETCH (no LIMIT here — we already have exactly the IDs we want)
@Query("""
        SELECT DISTINCT o FROM Order o
        LEFT JOIN FETCH o.items i
        LEFT JOIN FETCH i.product
        WHERE o.id IN :ids
        """)
List<Order> findByIdsWithItemsAndProducts(@Param("ids") List<Long> ids);
```

Call `findOrderIdsByUserId` to get a `Page<Long>` (safely paginated, no join), then `findByIdsWithItemsAndProducts` to hydrate those specific IDs with their items in a second query. Two queries — not N+1, and not the memory-loading trap.

## 4.13 Fix 2: `@EntityGraph`

`@EntityGraph` provides a way to specify which associations to eagerly fetch, without writing a JOIN FETCH string, and can be applied on a per-invocation basis instead of baked into a specific query:

```java
// In OrderRepository:
@EntityGraph(attributePaths = {"items", "items.product"})
Page<Order> findByUserIdAndStatusWithGraph(Long userId, OrderStatus status, Pageable pageable);
```

Under the hood, `@EntityGraph` instructs Hibernate to generate a `LEFT OUTER JOIN` covering `items` and `items.product` — the same SQL as JOIN FETCH, just without you writing the JPQL join yourself. Spring Data JPA also handles the JOIN FETCH + Pageable problem automatically when the graph specifies a collection: it executes two SQL queries (first a paginated query for the parent IDs, then a join query for the associations) instead of the memory-loading fallback — provided the method uses `Page<T>` as its return type.

**When to use `@EntityGraph` vs JOIN FETCH:**

| Dimension | JOIN FETCH | @EntityGraph |
|---|---|---|
| Verbosity | More explicit | Less JPQL to write |
| Flexibility | Tied to a specific `@Query` | Can be added to a derived method or an existing query |
| Pagination safety | You handle the split-query pattern manually | Spring Data handles it for `Page<T>` automatically |
| Nested paths | Supported (`i.product`) | Supported (`"items.product"`) |
| Named entity graphs | N/A | Can also reference `@NamedEntityGraph` on the entity class |

The practical guidance: if you're writing a custom `@Query` and need to fetch associations, JOIN FETCH is clear and direct. If you have a derived query method (no `@Query` annotation) and want to augment it with eager loading, `@EntityGraph` is the natural fit.

## 4.14 Fix 3: `@BatchSize`

`@BatchSize` doesn't eliminate extra queries — it reduces the *number* of them, by batching proxy-initialization into chunks:

```java
// ─── N+1 Fix 3: @BatchSize ───────────────────────────────────────────────────
//
// Problem: loading 100 users, each with orders → 101 queries (1 + 100)
//
// WITHOUT @BatchSize (N+1 problem):
// Query 1:  SELECT * FROM users LIMIT 100
// Query 2:  SELECT * FROM orders WHERE user_id = 1
// Query 3:  SELECT * FROM orders WHERE user_id = 2
// ... (100 separate order queries)
// Query 101: SELECT * FROM orders WHERE user_id = 100
// Total: 101 queries

// WITH @BatchSize(size = 25):
// Query 1: SELECT * FROM users LIMIT 100
// Query 2: SELECT * FROM orders WHERE user_id IN (1,2,3,...,25)
// Query 3: SELECT * FROM orders WHERE user_id IN (26,27,...,50)
// Query 4: SELECT * FROM orders WHERE user_id IN (51,52,...,75)
// Query 5: SELECT * FROM orders WHERE user_id IN (76,77,...,100)
// Total: 5 queries → 20× improvement over N+1

@Entity
public class User {
    @Id
    private Long id;
    private String username;

    @OneToMany(mappedBy = "user", fetch = FetchType.LAZY)
    @BatchSize(size = 25)   // ← Hibernate loads 25 at a time via IN clause
    private List<Order> orders;
}

// When to use @BatchSize vs JOIN FETCH vs @EntityGraph:
//
// JOIN FETCH:
// - Use when: you ALWAYS need the collection for every request
// - Generates: SELECT u.*, o.* FROM users u JOIN orders o ON o.user_id = u.id
// - Warning: causes Cartesian product if multiple collections are JOIN FETCHed
//
// @EntityGraph:
// - Use when: you sometimes need the collection (configurable per query method)
// - Generates: same as JOIN FETCH but specified at query method level
// @EntityGraph(attributePaths = {"orders"})
// List<User> findByActiveTrue();
//
// @BatchSize:
// - Use when: loading lazily and you want to batch the lazy loads
// - Best for: deeply nested collections, avoiding Cartesian product issues
// - Generates: WHERE user_id IN (...) queries instead of one per user
//
// Global default (applies to all lazy collections):
// spring.jpa.properties.hibernate.default_batch_fetch_size=25

// Enabling query count logging (detect N+1 in development):
spring:
  datasource:
    hikari:
      connection-test-query: SELECT 1
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        generate_statistics: true   # enables query count in logs
logging:
  level:
    org.hibernate.stat: DEBUG       # logs query count per session
    org.hibernate.SQL: DEBUG        # logs each SQL statement
```

N+1 becomes roughly N/batchSize + 1, which for a batch size of 25 on 100 orders means 5 queries instead of 101. Still not as efficient as JOIN FETCH (which issues *one* query regardless of N), but useful when JOIN FETCH is impractical.

**When `@BatchSize` is the right tool:** when JOIN FETCH would produce a cartesian explosion (fetching two independent collections simultaneously with JOIN FETCH produces N×M rows — all orders' items *and* all orders' status history entries as a join would multiply), or when the association is navigated in ad hoc code that's spread across the codebase and it's not practical to push a JOIN FETCH through every path. `@BatchSize` can also be applied at the entity level with `@Entity @BatchSize(size = 25)`, which batches the loading of the entity itself when multiple instances are loaded as proxies (common when `@ManyToOne` associations are involved).

## 4.15 Which fix, when?

| Scenario | Use this fix |
|---|---|
| Point query (single entity by ID) needing all its associations | `JOIN FETCH` in `@Query` |
| List query with pagination needing associations — simple case | `@EntityGraph` with `Page<T>` |
| List query with pagination needing associations — two separate `@OneToMany` collections | Split query (IDs first, then JOIN FETCH by IN clause) |
| Code that navigates an association in unpredictable, scattered places | `@BatchSize` on the collection |
| Performance-critical read path where any extra query is unacceptable | `JOIN FETCH` (one round-trip, period) |

The most important meta-point: **measure first**. Turn on `show-sql` in local development and count the queries for any endpoint that touches a collection. A single-row query showing up 51 times in a test run is the N+1 signature — it never looks like a performance problem until the table has real data in it, and by then it can be genuinely expensive to fix under load.

> **Interview Question — SDE-2:** "You've just profiled a production endpoint and found it fires 51 SQL queries for a list of 50 orders. Walk through your diagnosis and the fixes you'd consider."
>
> **Answer:** 51 queries for 50 rows is classic N+1 — 1 query for the list plus 1 per row for some association being lazily loaded. First step is turning on SQL logging locally and reproducing the endpoint: which query is being repeated tells me exactly which association is causing it (look at the `WHERE` clause — if it's `WHERE user_id = ?` appearing 50 times, `Order.user` is the culprit). For a list endpoint like this, the fix depends on what data we actually need from that association. If it's one or two fields off a `@ManyToOne` (like `user.email`), JOIN FETCH in the query is the cleanest fix — one SQL query with a join instead of 51. If we're paginating and fetching a `@OneToMany` collection, I'd use `@EntityGraph` on the derived query method and let Spring Data handle the safe two-query pagination pattern. If the association is navigated from deeply within existing code that's hard to refactor, `@BatchSize` on the collection declaration reduces the overhead without touching every call site. I wouldn't reach for `@BatchSize` first on a new endpoint — JOIN FETCH or EntityGraph is unambiguously faster per request. `@BatchSize` is the pragmatic tool for improving existing, hard-to-refactor code.

---

The entities are mapped correctly and the repositories can query them efficiently. The next part builds the service layer — where transactions, business logic, and the actual order-creation workflow live.
