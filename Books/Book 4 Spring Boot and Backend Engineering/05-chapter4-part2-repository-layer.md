# Chapter 4 (Part 2 of 6): The Repository Layer

## 4.6 What `JpaRepository` gives you for free

Spring Data JPA's `JpaRepository<T, ID>` is an interface that comes with a full CRUD implementation — no concrete class of your own is needed. The interface hierarchy is worth knowing:

```
Repository<T, ID>               (marker only)
 └─ CrudRepository<T, ID>       (save, findById, findAll, delete, count, existsById)
     └─ PagingAndSortingRepository<T, ID>  (findAll(Sort), findAll(Pageable))
         └─ JpaRepository<T, ID>           (flush, saveAndFlush, deleteAllInBatch, getById)
```

Extend it, parameterize it with your entity and its ID type, annotate the interface with `@Repository`, and Spring Data JPA generates a concrete proxy implementation at startup that fulfills every method from the hierarchy above, wired to your `DataSource`, without you writing a single line of SQL.

**`UserRepository`:**
```java
package com.example.ordermanagement.repository;

import com.example.ordermanagement.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    Optional<User> findByUsername(String username);
    boolean existsByEmail(String email);
    boolean existsByUsername(String username);
}
```

**`ProductRepository`:**
```java
package com.example.ordermanagement.repository;

import com.example.ordermanagement.entity.Product;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    Optional<Product> findBySku(String sku);
    boolean existsBySku(String sku);
    Page<Product> findByNameContainingIgnoreCase(String name, Pageable pageable);
}
```

**`InventoryRepository`:**
```java
package com.example.ordermanagement.repository;

import com.example.ordermanagement.entity.Inventory;
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface InventoryRepository extends JpaRepository<Inventory, Long> {

    Optional<Inventory> findByProductId(Long productId);

    /** Pessimistic write lock — used when we cannot afford to retry (e.g., payment gateway already charged). */
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT i FROM Inventory i WHERE i.product.id = :productId")
    Optional<Inventory> findByProductIdForUpdate(@Param("productId") Long productId);
}
```

**`OrderItemRepository`:**
```java
package com.example.ordermanagement.repository;

import com.example.ordermanagement.entity.OrderItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface OrderItemRepository extends JpaRepository<OrderItem, Long> {
}
```

## 4.7 Derived query methods

Spring Data JPA reads the method name itself and generates a query from it — no SQL required. The parser breaks the method name at keywords (`findBy`, `And`, `Or`, `After`, `Before`, `LessThan`, `GreaterThan`, `Containing`, `IgnoreCase`, `OrderBy`) and maps each segment to a field name on the entity. `findByEmail(String email)` becomes `SELECT u FROM User u WHERE u.email = :email`. The mapping is case-sensitive toward field names — `findByEmail` works because the field is `email`; `findByEMAIL` would fail to parse at startup.

**`OrderRepository`** is the most feature-rich repository in this application:
```java
package com.example.ordermanagement.repository;

import com.example.ordermanagement.entity.Order;
import com.example.ordermanagement.entity.OrderStatus;
import com.example.ordermanagement.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    // ── Derived query methods ──────────────────────────────────────────────

    Page<Order> findByUser(User user, Pageable pageable);

    Page<Order> findByUserId(Long userId, Pageable pageable);

    Page<Order> findByStatus(OrderStatus status, Pageable pageable);

    Page<Order> findByUserIdAndStatus(Long userId, OrderStatus status, Pageable pageable);

    List<Order> findByStatusAndCreatedAtBefore(OrderStatus status, Instant createdBefore);

    // ── JPQL queries ───────────────────────────────────────────────────────

    /**
     * JOIN FETCH loads Order + items + each item's product in a single SQL query.
     * This is the primary tool for avoiding N+1 on the order detail path.
     * See Chapter 4 Part 3 for the full breakdown.
     */
    @Query("""
            SELECT DISTINCT o FROM Order o
            LEFT JOIN FETCH o.items i
            LEFT JOIN FETCH i.product
            WHERE o.id = :orderId
            """)
    Optional<Order> findByIdWithItemsAndProducts(@Param("orderId") Long orderId);

    /**
     * JOIN FETCH on a collection (items) combined with Pageable is a known
     * problem in JPQL: mixing pagination with fetch joins causes Hibernate to
     * load ALL matching rows into memory and paginate in Java, which it warns
     * about at runtime. The split query below is the correct fix — see Part 3.
     */
    @Query("""
            SELECT DISTINCT o FROM Order o
            LEFT JOIN FETCH o.items i
            LEFT JOIN FETCH i.product
            WHERE o.user.id = :userId
            """)
    List<Order> findByUserIdWithItemsAndProducts(@Param("userId") Long userId);

    // ── EntityGraph ────────────────────────────────────────────────────────

    /**
     * @EntityGraph avoids the N+1 problem without a JOIN FETCH string.
     * Hibernate issues a LEFT OUTER JOIN covering exactly the named paths.
     */
    @EntityGraph(attributePaths = {"items", "items.product"})
    Page<Order> findByUserIdAndStatusWithGraph(Long userId, OrderStatus status, Pageable pageable);

    // ── Bulk update ────────────────────────────────────────────────────────

    /**
     * Marks all PENDING orders older than a given timestamp as CANCELLED —
     * a batch job use-case. @Modifying tells Spring Data this is a write query.
     * Must be called within a transaction — see note on @Transactional in Part 4.
     */
    @Modifying
    @Query("""
            UPDATE Order o SET o.status = :newStatus
            WHERE o.status = :currentStatus AND o.createdAt < :before
            """)
    int bulkUpdateStatus(@Param("newStatus") OrderStatus newStatus,
                         @Param("currentStatus") OrderStatus currentStatus,
                         @Param("before") Instant before);

    // ── Native SQL ─────────────────────────────────────────────────────────

    /**
     * Uses PostgreSQL's ILIKE for case-insensitive pattern matching — not
     * available in JPQL. nativeQuery = true bypasses the JPQL parser and sends
     * the SQL straight to the driver.
     */
    @Query(value = """
            SELECT o.* FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE u.email ILIKE :emailPattern
            ORDER BY o.created_at DESC
            LIMIT :limit
            """,
            nativeQuery = true)
    List<Order> findRecentByUserEmailPattern(@Param("emailPattern") String emailPattern,
                                              @Param("limit") int limit);
}
```

## 4.8 `@Query`: JPQL vs. native SQL

**JPQL** (Jakarta Persistence Query Language) looks like SQL but operates on **entity objects and field names**, not table names and column names. `SELECT o FROM Order o WHERE o.user.id = :userId` references the `Order` Java class and its `user` field (which Hibernate maps to the `user_id` column), not the `orders` table directly. The advantages are that JPQL queries survive a table rename (as long as you rename the entity mapping too), and the syntax is validated against the entity model at deployment time rather than discovered to be wrong at runtime. The disadvantage is that some SQL features — PostgreSQL's `ILIKE`, window functions, `ON CONFLICT DO NOTHING`, recursive CTEs — don't exist in JPQL, because JPQL is database-agnostic.

**Native SQL** (`nativeQuery = true`) bypasses the entity model and JPQL parser entirely and sends the SQL string directly to the JDBC driver. Use it when you genuinely need a database-specific feature, but be aware of what you lose: the query no longer benefits from JPQL's startup-time validation, it will silently break if a table or column is renamed, and it bypasses Hibernate's entity cache — entities loaded via a native query are not automatically merged into the first-level cache the way JPQL results are.

## 4.9 `@Modifying` and the transactional context it requires

`@Modifying` is required on any `@Query` that issues a DML statement (`UPDATE`, `DELETE`, `INSERT INTO ... SELECT`). Without it, Spring Data JPA refuses to execute the query, on the principle that a method returning `void` or `int` *could* be a mistake — a `SELECT` query wrapped in `@Query` accidentally assigned to a void method. `@Modifying` is the explicit declaration that this is intentional.

`@Modifying` alone is not sufficient, though: a DML query requires a transaction to be active. The repository interface method itself doesn't declare `@Transactional` — the transaction comes from whoever calls it. In our architecture that's always a `@Service` method annotated `@Transactional`, which is the right division of responsibility: the repository executes queries; the service owns the transaction that wraps them. This is covered in full in Part 4. If you ever need to call `bulkUpdateStatus` directly (in a test or a scheduled task, for instance) and there's no enclosing transaction, adding `@Transactional` to the repository method itself is also valid — it'll create a transaction for that one query.

There's a subtle cache-staleness issue with `@Modifying` that trips people up in tests: when a `@Modifying @Query` executes, it hits the database directly via JDBC, bypassing Hibernate's first-level (persistence context) cache. Entities loaded earlier in the same transaction still hold the old state in memory. Annotating with `@Modifying(clearAutomatically = true)` instructs Hibernate to clear the first-level cache after the DML runs, so subsequent reads see the updated database state. In practice, most `@Modifying` operations in well-structured code are the *last* significant thing in a transaction, so this doesn't bite often — but it's important to know exists, especially when writing tests.

## 4.10 Pagination with `Pageable` and `Page<T>`

A `Pageable` parameter on any repository method causes Spring Data JPA to generate a paginated query. You don't have to specify it in the SQL or JPQL string — Spring Data handles the `LIMIT` and `OFFSET` SQL clauses for you, and the SQL is different per database dialect (PostgreSQL uses `LIMIT/OFFSET`; Oracle uses `ROWNUM` or `FETCH FIRST`; the repository abstraction is the same regardless).

The service layer constructs a `Pageable` from controller request parameters and passes it down:

```java
// Controller receives page and size as request params; service uses them like this:
Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
Page<Order> orderPage = orderRepository.findByUserId(userId, pageable);
```

`Page<T>` is a richer result than a plain `List<T>` — it carries the list of items for this page *plus* metadata:

```java
orderPage.getContent()       // List<Order> — the actual rows
orderPage.getTotalElements() // 487 — total matching rows across ALL pages
orderPage.getTotalPages()    // 25 — at size=20
orderPage.getNumber()        // 0 — current page index (zero-based)
orderPage.isLast()           // false
orderPage.isFirst()          // true
```

The controller and DTO layers in Part 5 and Part 6 show how this becomes the JSON pagination envelope from Chapter 2.

One important caveat: `Page<T>` triggers a separate `SELECT COUNT(*)` query in addition to the main paginated query — Hibernate needs the total count to calculate `totalPages` and `totalElements`. For tables with hundreds of millions of rows, a `COUNT(*)` over a complex filter can itself be expensive. In those cases, `Slice<T>` (another Spring Data return type) is the alternative — it only tells you "is there a next page?", not the full total count, which requires only knowing whether there are more rows beyond the current page's limit, answerable with `LIMIT (size + 1)` rather than a full count. `Slice<T>` maps naturally to cursor-based "infinite scroll" UIs; `Page<T>` maps to numbered pagination.

> **Interview Question — SDE-2:** "Why is there a `@Modifying(clearAutomatically = true)` option and when must you use it?"
>
> **Answer:** Hibernate maintains a first-level cache (the persistence context) for the duration of a transaction — every entity you load within a transaction is cached there, and Hibernate answers subsequent lookups for the same entity from the cache without hitting the database again. A `@Modifying @Query` bypasses this cache entirely: the SQL executes directly against the database, but Hibernate doesn't automatically invalidate the cached copies of affected entities in the current persistence context. If code later in the same transaction loads one of those entities (via `findById`, for example), Hibernate serves the old, pre-update version from cache — a silent stale-read. `clearAutomatically = true` tells Hibernate to empty the first-level cache immediately after the DML runs, so the next entity lookup goes to the database and gets fresh state. The trade-off is that clearing the entire first-level cache means any subsequent entity access must go back to the database even for entities the bulk update didn't touch — a mild performance cost in a transaction that does extensive reading after a bulk write.

---

The repositories give us SQL-without-SQL for straightforward queries — but there's a notorious performance trap waiting in the middle of Section 4.7 that deserves its own focused treatment. The next part of this chapter is dedicated entirely to the N+1 problem: reproducing it deliberately, understanding exactly why it happens, and fixing it three different ways, so you can recognize and solve it the moment you see it in any codebase.
