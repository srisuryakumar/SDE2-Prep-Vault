# Chapter 4 (Part 1 of 6): Entities and JPA

This is where the Order Management API stops being a skeleton and starts being an actual application. Chapter 4 is split across six files — entities, repositories, the N+1 problem, the service layer, the controller layer, and validation/exception handling — because together they're genuinely a whole book's worth of material on their own. This first part is about getting the data model right, because every layer above it depends on these mappings being correct.

## 4.1 Bringing in JPA, and a real database

Add Spring Data JPA, the PostgreSQL driver, and H2 (for tests only, for now) to the `pom.xml` from Chapter 3:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>
```

We're reaching for a real PostgreSQL instance from the very first chapter that touches persistence, rather than the more common tutorial shortcut of an in-memory H2 database for "real" development. That's a deliberate choice, not extra ceremony for its own sake: H2 doesn't speak the same SQL dialect as Postgres, doesn't enforce constraints identically, and doesn't support several Postgres-specific features we'll use later (`FOR UPDATE SKIP LOCKED` in Chapter 4's repository section, for one). Code that "works" against H2 can fail in genuinely surprising ways against the database you actually deploy to — which is exactly the discussion in Chapter 6 about why this book reaches for Testcontainers over H2 for serious tests. H2 still earns a place in this project, in Chapter 6, specifically as a fast, zero-dependency option for one narrow kind of test — but it never plays the role of "the database the app runs against."

Run Postgres locally with Docker Compose:

**`docker-compose.yml`**
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: orderdb
      POSTGRES_USER: orderapp
      POSTGRES_PASSWORD: orderapp_dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

`docker compose up -d` and Postgres is listening on `localhost:5432`. Now extend `application.yml`:

**`src/main/resources/application.yml`** (full file, accumulated)
```yaml
server:
  port: 8080

spring:
  application:
    name: order-management
  datasource:
    url: jdbc:postgresql://localhost:5432/orderdb
    username: orderapp
    password: orderapp_dev_password
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        format_sql: true
    open-in-view: false

ordermanagement:
  name: "Order Management API"
  support-email: "support@ordermanagement.com"
  max-items-per-order: 50

logging:
  level:
    com.example.ordermanagement: DEBUG
    org.hibernate.SQL: DEBUG
```

Three settings deserve a flag before we move on, because each is a common source of confusion later:

`ddl-auto: update` tells Hibernate to inspect your entity mappings at startup and alter the schema to match — convenient for this stage of development, genuinely dangerous in production (it can silently drop columns it thinks are no longer needed). Chapter 9 replaces this entirely with Flyway-managed migrations and switches this setting to `validate` — Hibernate checking the schema matches your entities without ever being allowed to change it itself.

`show-sql: true` (plus the `org.hibernate.SQL: DEBUG` logger) prints every generated SQL statement to the console. This sounds like a minor convenience now; it's the exact mechanism we use to *catch the N+1 problem with our own eyes* in this chapter's third part.

`open-in-view: false` turns off Spring Boot's "Open Session in View" pattern, which — left at its default of `true` — keeps the Hibernate session open for the entire HTTP request, including while the view/serialization layer is rendering the response, specifically so that lazy associations can still be fetched at that point without throwing. It's convenient, and it's also a trap: it hides exactly the kind of lazy-loading and N+1 problems this chapter is about to teach you to find, by quietly papering over them with extra queries issued during serialization, far from the code that triggered them. We disable it deliberately so that any lazy-loading mistake fails loudly, close to where it was made, instead of working by accident in development and then failing in some subtly different way under load in production.

## 4.2 The five entities

### `Role` and `OrderStatus`

```java
package com.example.ordermanagement.entity;

public enum Role {
    CUSTOMER,
    ADMIN
}
```

```java
package com.example.ordermanagement.entity;

public enum OrderStatus {
    PENDING,
    CONFIRMED,
    SHIPPED,
    DELIVERED,
    CANCELLED
}
```

### `User`

```java
package com.example.ordermanagement.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String username;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    /** Always a BCrypt hash — see Chapter 5. Never the plaintext password. */
    @Column(nullable = false)
    private String password;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private Role role;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    public User(String username, String email, String password, Role role) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.role = role;
    }
}
```

The table is explicitly named `users`, not left to default to `user` — Hibernate's default naming strategy would otherwise turn the class name `User` straight into the table name `user`, and `user` is a reserved word in PostgreSQL (it's a built-in function that returns the current session's user). Letting Hibernate generate that table name unquoted produces a working-until-it-doesn't situation depending on exactly how it's quoted in the generated DDL — explicitly naming it sidesteps the whole question.

### `Product` and `Inventory`

```java
package com.example.ordermanagement.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "products")
@Getter
@Setter
@NoArgsConstructor
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String sku;

    @Column(nullable = false, length = 200)
    private String name;

    @Column(length = 2000)
    private String description;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal price;

    @OneToOne(mappedBy = "product", fetch = FetchType.LAZY)
    private Inventory inventory;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(nullable = false)
    private Instant updatedAt;

    public Product(String sku, String name, String description, BigDecimal price) {
        this.sku = sku;
        this.name = name;
        this.description = description;
        this.price = price;
    }
}
```

```java
package com.example.ordermanagement.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import jakarta.persistence.Version;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "inventory")
@Getter
@Setter
@NoArgsConstructor
public class Inventory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false, unique = true)
    private Product product;

    @Column(name = "quantity_available", nullable = false)
    private Integer quantityAvailable;

    /** Optimistic-locking token — see section 4.4 below. */
    @Version
    private Long version;

    public Inventory(Product product, Integer quantityAvailable) {
        this.product = product;
        this.quantityAvailable = quantityAvailable;
    }
}
```

We model `Inventory` as its own entity rather than just a `quantityAvailable` column directly on `Product`, on purpose. It's not strictly necessary for an app this size — but it mirrors how real systems usually evolve (inventory tracking tends to grow its own concerns: warehouses, reservations, reorder thresholds) and it gives us a clean `@OneToOne` to map, plus the most natural possible home for the `@Version` field we'll lean on heavily in the service layer.

### `Order` and `OrderItem`

```java
package com.example.ordermanagement.entity;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.persistence.Version;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "orders")
@Getter
@Setter
@NoArgsConstructor
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private OrderStatus status = OrderStatus.PENDING;

    @Column(name = "total_amount", nullable = false, precision = 10, scale = 2)
    private BigDecimal totalAmount = BigDecimal.ZERO;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    /** Optimistic-locking token — guards against two concurrent updates to the same order. */
    @Version
    private Long version;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(nullable = false)
    private Instant updatedAt;

    public Order(User user) {
        this.user = user;
    }

    /** Keeps both sides of the bidirectional association in sync — see section 4.3. */
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);
        this.totalAmount = this.totalAmount.add(
                item.getUnitPrice().multiply(BigDecimal.valueOf(item.getQuantity())));
    }
}
```

```java
package com.example.ordermanagement.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;

@Entity
@Table(name = "order_items")
@Getter
@Setter
@NoArgsConstructor
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    @Column(nullable = false)
    private Integer quantity;

    /** Price at the moment of purchase — deliberately decoupled from Product.price, which changes over time. */
    @Column(name = "unit_price", nullable = false, precision = 10, scale = 2)
    private BigDecimal unitPrice;

    public OrderItem(Product product, Integer quantity, BigDecimal unitPrice) {
        this.product = product;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }
}
```

`orders` is named explicitly for the same reason `users` was — `ORDER` (as in `ORDER BY`) is a reserved SQL keyword, and sidestepping that question entirely is simpler than relying on correct automatic quoting.

`unitPrice` on `OrderItem` is the detail most worth lingering on, because it's a real, recurring modeling mistake when people are new to this domain: if you only stored `Product.price` and looked it up at display time, every historical order's total would silently change every time you updated a product's price — last month's $50 item would retroactively become $60 on an already-completed order, the moment you increased the product's price. Capturing `unitPrice` on the `OrderItem` at the moment the order is placed is what makes an order an honest historical record instead of a moving target.

## 4.3 The relationships, explained properly

We're using exactly three kinds of associations, and between them they cover what you'll see in the overwhelming majority of real schemas:

```
User    (1) ──────< Order      (N)        @OneToMany / @ManyToOne
Order   (1) ──────< OrderItem  (N)        @OneToMany / @ManyToOne
Product (1) ──────< OrderItem  (N)        @ManyToOne (unidirectional from OrderItem)
Product (1) ───────── Inventory (1)       @OneToOne
```

**`@ManyToOne`** is always the side that holds the actual foreign-key column — `OrderItem.order` is mapped with `@JoinColumn(name = "order_id")`, meaning the `order_items` table genuinely has an `order_id` column pointing back at `orders`. This is, by a wide margin, the most common and the most efficient association to navigate: "give me this item's order" is one indexed lookup.

**`@OneToMany(mappedBy = "order")`** on `Order.items` is the *inverse* side of that exact same relationship — `mappedBy` tells Hibernate "don't create a second foreign key for this; the `order` field on `OrderItem` already owns it, I'm just exposing the reverse navigation." Get this backwards — omit `mappedBy`, or point it at the wrong field name — and Hibernate assumes it owns the relationship too, and silently creates a *second*, useless join table to track it, which is a genuinely common and confusing bug for people new to JPA.

**`cascade = CascadeType.ALL, orphanRemoval = true`** on `Order.items` means: persist, update, and delete operations on an `Order` automatically cascade to its `OrderItem`s, and removing an item from the `items` list (rather than deleting the whole order) deletes that orphaned `OrderItem` row from the database too. This is the right call specifically because an `OrderItem` has no independent existence or meaning outside its parent `Order` — nobody queries `OrderItem`s on their own; they only ever matter in the context of the order they belong to. Contrast this with `OrderItem.product`, which has no cascade at all: deleting an `OrderItem` should obviously never cascade to delete the `Product` it references — a product has an entirely independent lifecycle from any one order that happens to reference it.

**`@OneToOne`** between `Product` and `Inventory` is the one relationship type with a genuine, well-known gotcha attached to it, covered fully in the next section.

> **Interview Question — SDE-2:** "What actually goes wrong if you forget `mappedBy` on one side of a bidirectional `@OneToMany`/`@ManyToOne`?"
>
> **Answer:** Without `mappedBy`, Hibernate has no way to know the two sides describe the *same* relationship — it treats `Order.items` as an independent, Hibernate-owned-and-managed collection, which for a `@OneToMany` without an explicit `@JoinColumn` means it creates a separate join table (something like `order_order_items`) to track the association, entirely distinct from the `order_id` foreign key that `OrderItem.order`'s `@ManyToOne` is already maintaining. You end up with two separate, disconnected representations of the same logical relationship in the schema, and depending on which side of the entity graph you update, only one of them gets kept in sync — a frustrating, intermittent bug that usually surfaces as "I set this and saved it, but querying it back doesn't show the change."

## 4.4 Fetch types: the default everyone gets wrong

Every association has a fetch type — `EAGER` (load it immediately, as part of loading the owning entity) or `LAZY` (don't touch the database for it until something actually calls the getter). The defaults are not what most people assume, and getting this wrong is one of the most common sources of real production performance bugs in any JPA codebase:

| Association | Default fetch type |
|---|---|
| `@OneToMany` | `LAZY` |
| `@ManyToMany` | `LAZY` |
| `@ManyToOne` | **`EAGER`** |
| `@OneToOne` | **`EAGER`** |

The two *-to-one relationships default to `EAGER`, and that default is a trap: it means that, unless you override it, every time you load an `OrderItem`, Hibernate also immediately, silently loads its `Order` and its `Product` — even in a query path that never intended to look at either. This is exactly why every `@ManyToOne` and `@OneToOne` in this chapter's entities is annotated explicitly with `fetch = FetchType.LAZY` — overriding a default that's wrong often enough that this book treats "always declare your fetch type explicitly, and default to LAZY" as a non-negotiable house rule, not a style preference.

The cost of getting this wrong compounds: it's the root cause behind the N+1 problem covered in this chapter's third part — if `@ManyToOne` associations default to eager loading, then fetching a list of orders and touching each one's user *should* trigger one query per order regardless, by design, unless you explicitly tell Hibernate to fetch them together. Understanding the eager/lazy default table above is the prerequisite for the entire next section making sense.

Going lazy everywhere has its own sharp edge, though: a lazy association is backed by a Hibernate-generated proxy object, and that proxy can only actually go fetch its data while the originating Hibernate `Session` is still open. Touch a lazy field — call `order.getItems().size()`, for instance — *after* the transaction that loaded `order` has already committed and the session has closed, and you get a `LazyInitializationException`: `could not initialize proxy — no Session`. This shows up constantly for people new to JPA the moment they try to access a lazy collection from inside a controller, after the `@Transactional` service method that loaded the entity has already returned and closed its session. The fix is never "make it eager so the error goes away" — that just trades a loud, obvious failure for a silent, possibly large performance cost, paid on every single load whether you need that data or not. The real fix is to fetch exactly what you need, inside the transaction, using the techniques in this chapter's third part — `JOIN FETCH`, `@EntityGraph`, or restructuring the query — so the data is already loaded by the time the transaction (and the session with it) closes.

> **Interview Question — SDE-2:** "Why does `@ManyToOne` default to `EAGER` when `@OneToMany` defaults to `LAZY` — isn't that inconsistent?"
>
> **Answer:** It's a historical default rooted in cost-per-object, not a logical inconsistency once you see the reasoning: a `@ManyToOne` points at exactly *one* related row, so the JPA spec's authors assumed eagerly fetching it was cheap and rarely worth the complexity of a proxy. A `@OneToMany` points at a potentially unbounded collection, where eagerly loading it could mean pulling in thousands of rows you didn't ask for — clearly too risky to default to eager. In practice, the `@ManyToOne` default turns out to be the wrong call far more often than the spec's authors anticipated, specifically because of the N+1 problem: eagerly loading one related row per parent row, across a *list* of parents, multiplies that "cheap" single fetch by however many parent rows you loaded. That's exactly why production codebases — including this one — override the default to `LAZY` across the board and fetch eagerly only deliberately, via an explicit join, when a specific query path actually needs it.

A second, subtler gotcha shows up specifically on the *inverse* (`mappedBy`) side of a `@OneToOne`, and it's worth knowing even though it won't bite you in this project's code: declaring `fetch = FetchType.LAZY` on `Product.inventory` (the `mappedBy` side) doesn't reliably produce lazy behavior in plain Hibernate, without bytecode enhancement enabled. The owning side (`Inventory.product`, which holds the actual foreign key) *can* be lazily proxied cheaply, because Hibernate already knows the foreign key value from the row it just loaded and can build a proxy around it without hitting the database again. The inverse side has no local foreign key to build a proxy from — to know whether a `Product` even *has* an associated `Inventory` row at all, Hibernate has to go query the `inventory` table by `product_id`, which means it often ends up doing that eagerly in practice regardless of what `fetch` says, unless you've opted into Hibernate's bytecode enhancement feature. It's a well-known enough rough edge that it's worth being able to name in an interview, even though, practically, this project never navigates from `Product` to `Inventory` lazily in a way that the distinction matters for.

## 4.5 `@Version` and optimistic locking

`@Version` is a single column (`Long` works, as does `int` or a `Timestamp`) that Hibernate manages entirely on your behalf, and it's the mechanism that prevents **lost updates** — two concurrent transactions each reading a row, each making a change based on what they read, and the second one's write silently overwriting the first one's, with no error, no warning, and no way to even know it happened.

Here's the mechanism precisely, because "it prevents lost updates" without the *how* isn't an SDE-2-level answer:

1. A transaction reads an `Inventory` row: `quantityAvailable = 5`, `version = 12`.
2. It computes a new value — say, decrementing to `4` — and issues an update.
3. Hibernate doesn't generate `UPDATE inventory SET quantity_available = 4 WHERE id = 7`. It generates `UPDATE inventory SET quantity_available = 4, version = 13 WHERE id = 7 AND version = 12` — the version the transaction *originally read* is baked directly into the `WHERE` clause, and the new version is incremented as part of the same statement.
4. If no other transaction touched this row in between, exactly one row matches that `WHERE` clause, the update succeeds, and the row's version is now `13`.
5. If a *different* transaction already updated this same row in the meantime — bumping the version to `13` itself — then this transaction's `WHERE id = 7 AND version = 12` matches **zero rows**, because the version in the database is no longer `12`. Hibernate checks the affected-row count after the update; zero rows affected on a query that should have matched exactly one is the signal that someone else got there first, and Hibernate raises an `OptimisticLockException` (surfacing, in Spring, as `ObjectOptimisticLockingFailureException` — Section 3.6 covered why `@Repository`'s exception translation is what makes that the exception you actually see, rather than Hibernate's native one).

This is precisely the scenario described in this book's README: two customers racing for the last unit of a product. Both read `quantityAvailable = 1, version = 12`. Both compute "decrement to 0." Whichever transaction's `UPDATE ... WHERE version = 12` commits first wins and the version moves to `13`; the second transaction's identical-looking update now matches zero rows, fails with an optimistic lock exception, and — as built out fully in this chapter's fourth part, the service layer — that failure becomes a `409 Conflict` response to the losing customer, instead of both customers' orders silently succeeding against stock that only existed once.

It's called *optimistic* locking specifically in contrast to *pessimistic* locking (`SELECT ... FOR UPDATE`, which takes a real database-level row lock for the duration of the transaction, blocking any other transaction from even reading-for-update that row until the first one commits or rolls back). Optimistic locking assumes conflicts are rare and cheap to detect after the fact, rather than expensive to prevent up front — it never blocks anyone; it just occasionally tells the loser of a race to retry. For a "many reads, occasional concurrent write" workload like inventory checks during checkout, that assumption holds well and avoids the throughput cost of holding row locks. We touch on when you'd reach for pessimistic locking instead in the next part of this chapter.

> **Interview Question — SDE-2:** "Walk through exactly what SQL gets generated when an optimistic lock check fails, and what exception ends up in your controller."
>
> **Answer:** The generated SQL is an ordinary `UPDATE` statement with the previously-read version value folded into the `WHERE` clause — `UPDATE inventory SET quantity_available = ?, version = ? WHERE id = ? AND version = ?` — there's no special "locking" SQL syntax involved at all; the entire mechanism is just a conditional update plus a row-count check. Hibernate inspects the JDBC driver's reported affected-row count after executing it; if that count is zero on a statement that, by primary key, should have matched exactly one row, Hibernate concludes someone else updated the row first and the version it had in memory is stale. It throws `OptimisticLockException` (or, depending on the exact code path, Hibernate's `StaleObjectStateException`), which Spring's `@Repository`-triggered exception translation converts into `ObjectOptimisticLockingFailureException` (specifically its JPA-aware subtype, `JpaOptimisticLockingFailureException`) by the time it reaches your service or controller code — which is the exception this book's global exception handler, in this chapter's sixth part, catches and turns into a `409 Conflict`.

### `@Version` — Optimistic Locking Deep Dive

The `@Version` explanation above covered the *mechanism* — now here's the complete, production-grade implementation, from entity to retry loop to exception handler, so you can see the full picture of how optimistic locking works in practice:

```java
// ─── @Version — Optimistic Locking Deep Dive ────────────────────────────────

@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Version
    private Long version;  // JPA auto-increments on every successful update

    private String status;
    private BigDecimal totalAmount;

    // No need to manually manage 'version' — JPA handles it entirely
}

// What JPA generates for every save():
// SQL: UPDATE orders
//      SET status = ?, total_amount = ?, version = 3    ← version incremented
//      WHERE id = 42 AND version = 2                    ← version checked
//
// If another transaction already updated this row (version is now 3, not 2):
// UPDATE matches 0 rows → JPA throws OptimisticLockException

// ─── Service with Retry Loop ─────────────────────────────────────────────────

@Service
@Slf4j
public class OrderService {

    @Autowired private OrderRepository orderRepo;

    // Version 1: Simple — throws immediately on conflict
    @Transactional
    public Order updateStatus(Long orderId, String newStatus) {
        Order order = orderRepo.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
        order.setStatus(newStatus);
        return orderRepo.save(order);
        // Throws OptimisticLockException if version mismatch
    }

    // Version 2: With retry loop — appropriate for low-contention updates
    public Order updateStatusWithRetry(Long orderId, String newStatus) {
        int maxAttempts = 3;
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return doUpdateStatus(orderId, newStatus);
            } catch (OptimisticLockException | ObjectOptimisticLockingFailureException e) {
                if (attempt == maxAttempts) {
                    log.error("Failed to update order {} after {} attempts", orderId, maxAttempts);
                    throw new OrderUpdateConflictException(
                        "Order " + orderId + " is being modified by another process");
                }
                log.warn("Optimistic lock conflict on order {}. Attempt {}/{}. Retrying...",
                    orderId, attempt, maxAttempts);
                try {
                    Thread.sleep(50L * attempt); // exponential backoff: 50ms, 100ms, 150ms
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new OrderUpdateConflictException("Interrupted during retry");
                }
            }
        }
        throw new IllegalStateException("Should never reach here");
    }

    @Transactional
    private Order doUpdateStatus(Long orderId, String newStatus) {
        Order order = orderRepo.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
        order.setStatus(newStatus);
        return orderRepo.save(order);
    }
}

// ─── Exception Handler ────────────────────────────────────────────────────────

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ObjectOptimisticLockingFailureException.class)
    public ResponseEntity<ErrorResponse> handleOptimisticLock(
            ObjectOptimisticLockingFailureException ex) {
        return ResponseEntity
            .status(HttpStatus.CONFLICT)  // 409 Conflict
            .body(new ErrorResponse("CONFLICT",
                "This record was modified by another request. Please refresh and try again."));
    }
}

// ─── When to use Optimistic vs Pessimistic Locking ───────────────────────────

/*
 OPTIMISTIC (@Version):
 - Low contention: most reads, few writes, conflicts are rare
 - Use for: user profile updates, product description edits, order notes
 - Pro: no database lock held → high throughput, no deadlock risk
 - Con: must handle OptimisticLockException and potentially retry

 PESSIMISTIC (SELECT FOR UPDATE):
 - High contention: many concurrent writes fighting for the same row
 - Use for: concert ticket booking, limited edition product stock
 - Pro: guaranteed to succeed once you acquire the lock
 - Con: other transactions WAIT (reduced throughput), deadlock risk

 Decision rule:
 If you expect conflicts to be RARE → Optimistic
 If you expect conflicts to be FREQUENT → Pessimistic
*/
```

---

The entities exist and the relationships are correctly mapped — but nothing can query them yet. The next part of this chapter builds the repository layer that actually talks to the database.
