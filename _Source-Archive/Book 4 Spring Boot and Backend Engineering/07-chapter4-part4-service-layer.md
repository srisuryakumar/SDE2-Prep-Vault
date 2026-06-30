# Chapter 4 (Part 4 of 6): The Service Layer

## 4.16 What the service layer is responsible for

The service layer is where business logic lives — the rules about what the application is actually *allowed* to do, not just how to store and retrieve data. The repository layer asks "give me rows matching this condition"; the service layer asks "is this operation valid *right now*, for *this user*, given the current state of everything?" Keeping these concerns separate is what makes each layer independently testable and replaceable.

Every public method in a service class that touches the database should be wrapped in a transaction. That's not bureaucracy — it's the guarantee that either everything in the method succeeds and is committed to the database together, or nothing is committed, with no half-finished intermediate state left visible to other transactions.

## 4.17 `@Transactional`: what it actually does

`@Transactional` is implemented via Spring AOP proxy (Chapter 8 covers the proxy mechanism in full — this section covers what the proxy *does* rather than how it's built). When the proxy intercepts a method call on a `@Transactional`-annotated method:

1. It checks whether a transaction is already active on the current thread (via a `ThreadLocal` resource managed by Spring's `TransactionSynchronizationManager`).
2. Depending on the `propagation` setting, it either joins that existing transaction or creates a new one.
3. It delegates the actual call to your real method.
4. If your method returns normally: it commits the transaction.
5. If your method throws an unchecked exception (`RuntimeException` or `Error`): it rolls back.
6. If your method throws a *checked* exception: by default it **commits** — the historical Spring default most people expect to be a rollback. Override this with `rollbackFor = Exception.class` if you want checked exceptions to trigger a rollback too.

The resource — the JDBC connection, the Hibernate `Session` — is bound to the thread for the duration of the method call, which is why any repository or entity manager call made from within that method participates in the same transaction automatically. No explicit connection-passing is required.

## 4.18 Transaction propagation

Propagation controls what happens when a `@Transactional` method is called while a transaction is *already active* on the current thread:

| Propagation | Behavior |
|---|---|
| `REQUIRED` (default) | Join the existing transaction if there is one; otherwise create a new one. The most common choice — "this work belongs to the same unit of work as whatever called me." |
| `REQUIRES_NEW` | **Always** create a brand-new transaction, suspending the caller's transaction if one exists. Changes committed in the inner transaction are visible even if the outer transaction later rolls back. Used for "audit this event regardless of whether the business operation succeeded." |
| `NOT_SUPPORTED` | Execute without a transaction, suspending any active one. Rare — used for operations that should not participate in a transaction at all (e.g., calling a metrics endpoint that reads loosely consistent data and doesn't care about isolation). |
| `MANDATORY` | A transaction **must already be active**; throw an exception if there isn't one. Used to enforce "this method must only ever be called from within an already-open transaction." |
| `NEVER` | Throw an exception if a transaction **is** active. The opposite of `MANDATORY` — "this must not participate in a transaction." |
| `NESTED` | Creates a *savepoint* within the existing transaction. If the nested method rolls back, it rolls back only to the savepoint, leaving the outer transaction intact. Requires a JDBC driver that supports savepoints (PostgreSQL does). Not the same as `REQUIRES_NEW` — the nested transaction is still part of the outer one and rolls back completely if the outer transaction rolls back. |

In practice, `REQUIRED` covers 90% of service methods. `REQUIRES_NEW` shows up for cross-cutting operations that must persist their own result regardless of the main operation's fate — the most common real example being an audit log or idempotency record that should be written even if the business operation it wraps fails and rolls back.

## 4.19 The self-invocation trap

This is the most important gotcha in all of Spring, and it comes up in almost every serious Spring interview. The rule is simple but the implication is surprising:

**`@Transactional` (and every other Spring AOP annotation) has no effect when one method in the same class calls another method in the same class.**

Here's the failure mode:

```java
@Service
public class OrderService {

    // This method HAS a transaction — it's called from outside the class, via proxy
    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {
        // ... business logic ...
        sendConfirmationEmail(order);  // ← Calls the method below directly on 'this'
        return buildResponse(order);
    }

    // This @Transactional annotation does NOTHING — called via 'this', not via the proxy
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendConfirmationEmail(Order order) {
        // Intended to run in its own separate transaction — doesn't.
        // Runs in the SAME transaction as createOrder(), silently.
    }
}
```

**Why?** Spring AOP works by wrapping your bean in a proxy object. When `OrderController` calls `orderService.createOrder(...)`, it's calling the *proxy* — the proxy intercepts the call, opens a transaction, delegates to the real `OrderService.createOrder()`, then commits or rolls back. But when `createOrder()` calls `sendConfirmationEmail(order)` internally, it's calling it on `this` — the *real* `OrderService` instance, not the proxy. The proxy never sees the call. No interception happens. The `@Transactional(propagation = REQUIRES_NEW)` on `sendConfirmationEmail` is completely ignored.

**The fixes:**

**Option 1 — Extract to a separate Spring-managed bean.** Move `sendConfirmationEmail` to a `NotificationService` bean. `OrderService` injects `NotificationService` and calls `notificationService.sendConfirmationEmail(order)`. Now the call goes through the `NotificationService` proxy, and its `@Transactional` works correctly. This is the cleanest fix and also the most architecturally sound — the two concerns probably belong in separate classes anyway.

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final NotificationService notificationService;

    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {
        // ...
        notificationService.sendConfirmationEmail(order); // ← Goes through proxy — works correctly
        return buildResponse(order);
    }
}
```

**Option 2 — Self-inject via `ApplicationContext`.** An `OrderService` bean injected with a reference to *itself* (obtained from the `ApplicationContext`) gets the proxy reference rather than `this`. Functional but ugly — it reads like a circular dependency, and the intent isn't obvious to the next reader.

```java
@Service
@RequiredArgsConstructor
public class OrderService implements ApplicationContextAware {
    private ApplicationContext applicationContext;

    @Override
    public void setApplicationContext(ApplicationContext ctx) {
        this.applicationContext = ctx;
    }

    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {
        // ...
        applicationContext.getBean(OrderService.class)
                          .sendConfirmationEmail(order); // ← Gets the proxy
        return buildResponse(order);
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendConfirmationEmail(Order order) { ... }
}
```

**Option 3 — Enable AspectJ compile-time or load-time weaving.** AspectJ weaves the aspect logic directly into the bytecode rather than using proxies, so `this.method()` calls are intercepted. This is a real configuration change (adding the AspectJ plugin to the build) and not what most Spring Boot applications do — mentioned for completeness, because the question "is there a way to make self-invocation work?" has an answer.

The practical takeaway: **Option 1 is always right**. If self-invocation seems necessary, that's a signal the class is doing too much and a method should move somewhere else. We apply this pattern throughout our service layer below.

> **Interview Question — SDE-2:** "Explain why `@Transactional` doesn't work when a method calls another method in the same class."
>
> **Answer:** Spring implements `@Transactional` through AOP proxies — at startup, any bean with `@Transactional` methods gets wrapped in a proxy object. All external callers hold a reference to the proxy, not the real bean. When an external caller invokes a method, the proxy intercepts the call, opens a transaction, delegates to the real instance, then commits or rolls back. But when a method on the real bean calls another method on the same bean, it does so via `this` — a direct reference to the real instance, bypassing the proxy entirely. The proxy never intercepts the internal call, so no transaction logic runs, no matter what's annotated. The standard fix is to move the second method to a separate Spring-managed bean, so the call goes through that bean's proxy and the annotation is honored.

## 4.20 `@Transactional(readOnly = true)`

Read-only transactions are an optimization hint, not a security constraint. When `readOnly = true`:

- Spring passes the hint to the JDBC driver, which may optimize the connection for read access (some drivers route reads to a replica).
- Hibernate skips "dirty checking" at the end of the transaction — the process where it compares every entity's current state to the snapshot it took when it loaded them, to generate `UPDATE` statements for anything that changed. On a read-only path, no entity should change, so this check is wasted work. Skipping it is faster, especially when many entities are loaded.
- If Hibernate detects that an entity actually *was* modified in a `readOnly = true` transaction, it won't flush those changes — they silently disappear. This can produce genuinely confusing behavior if a "read" method accidentally modifies an entity, so treat `readOnly = true` as a double-enforcement: it both optimizes the happy path and makes accidental writes harmless-but-silent.

Apply it to every service method that doesn't need to write:

```java
@Transactional(readOnly = true)
public Page<OrderResponse> getOrdersForUser(Long userId, Pageable pageable) {
    return orderRepository.findByUserId(userId, pageable)
            .map(OrderResponse::from);
}
```

## 4.21 The complete service layer

**`IdempotencyRecord` entity** — before the service classes, we need the entity that backs idempotency key storage. From Chapter 2's design: the server stores a key→result mapping, so a retry can return the cached response instead of reprocessing.

```java
package com.example.ordermanagement.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;

@Entity
@Table(name = "idempotency_records")
@Getter
@Setter
@NoArgsConstructor
public class IdempotencyRecord {

    @Id
    @Column(name = "idempotency_key", length = 100)
    private String idempotencyKey;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String responseBody;

    @Column(nullable = false)
    private Integer httpStatus;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    public IdempotencyRecord(String idempotencyKey, String responseBody, Integer httpStatus) {
        this.idempotencyKey = idempotencyKey;
        this.responseBody = responseBody;
        this.httpStatus = httpStatus;
    }
}
```

```java
package com.example.ordermanagement.repository;

import com.example.ordermanagement.entity.IdempotencyRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface IdempotencyRecordRepository extends JpaRepository<IdempotencyRecord, String> {
}
```

**DTOs** — the data transfer objects that cross the API boundary. These are distinct from entities deliberately: entities are the persistence model; DTOs are the API contract. Separating them means you can change your schema without changing the API shape (or vice versa), and you avoid accidentally exposing internal fields (like a hashed `password`) in a JSON response by omitting them from the DTO rather than by remembering to ignore them in every serializer.

```java
package com.example.ordermanagement.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

import java.util.List;

public record CreateOrderRequest(
        @NotEmpty(message = "Order must contain at least one item")
        @Size(max = 50, message = "Order cannot exceed 50 items")
        @Valid
        List<OrderItemRequest> items
) {
    public record OrderItemRequest(
            Long productId,
            Integer quantity
    ) {}
}
```

```java
package com.example.ordermanagement.dto.response;

import com.example.ordermanagement.entity.Order;
import com.example.ordermanagement.entity.OrderStatus;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

public record OrderResponse(
        Long id,
        Long userId,
        OrderStatus status,
        BigDecimal totalAmount,
        List<OrderItemResponse> items,
        Instant createdAt
) {
    public static OrderResponse from(Order order) {
        return new OrderResponse(
                order.getId(),
                order.getUser().getId(),
                order.getStatus(),
                order.getTotalAmount(),
                order.getItems().stream()
                        .map(item -> new OrderItemResponse(
                                item.getId(),
                                item.getProduct().getId(),
                                item.getProduct().getName(),
                                item.getQuantity(),
                                item.getUnitPrice()
                        ))
                        .toList(),
                order.getCreatedAt()
        );
    }

    public record OrderItemResponse(
            Long id,
            Long productId,
            String productName,
            Integer quantity,
            BigDecimal unitPrice
    ) {}
}
```

**Custom exceptions:**

```java
package com.example.ordermanagement.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) { super(message); }
    public ResourceNotFoundException(String resourceName, Long id) {
        super(resourceName + " with id " + id + " not found");
    }
}
```

```java
package com.example.ordermanagement.exception;

public class InsufficientStockException extends RuntimeException {
    public InsufficientStockException(String sku, int requested, int available) {
        super("Insufficient stock for product '" + sku + "': requested " + requested
                + ", available " + available);
    }
}
```

```java
package com.example.ordermanagement.exception;

public class DuplicateResourceException extends RuntimeException {
    public DuplicateResourceException(String message) { super(message); }
}
```

```java
package com.example.ordermanagement.exception;

public class InvalidOrderStateException extends RuntimeException {
    public InvalidOrderStateException(String message) { super(message); }
}
```

**`InventoryService`** — separated from `OrderService` (Option 1 above, applied proactively) so that inventory operations can have their own transactional scope:

```java
package com.example.ordermanagement.service;

import com.example.ordermanagement.entity.Inventory;
import com.example.ordermanagement.entity.Product;
import com.example.ordermanagement.exception.InsufficientStockException;
import com.example.ordermanagement.exception.ResourceNotFoundException;
import com.example.ordermanagement.repository.InventoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Slf4j
public class InventoryService {

    private final InventoryRepository inventoryRepository;

    @Transactional
    public void decrementStock(Product product, int quantity) {
        Inventory inventory = inventoryRepository.findByProductId(product.getId())
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Inventory for product", product.getId()));

        if (inventory.getQuantityAvailable() < quantity) {
            throw new InsufficientStockException(
                    product.getSku(), quantity, inventory.getQuantityAvailable());
        }

        inventory.setQuantityAvailable(inventory.getQuantityAvailable() - quantity);
        // No explicit save() call needed — Hibernate's dirty checking detects
        // the field change and issues an UPDATE at transaction commit.
        // If another transaction committed between our read and commit, the
        // @Version field on Inventory causes an OptimisticLockingFailureException.
        log.debug("Decremented stock for product {} by {}: now {}",
                product.getSku(), quantity, inventory.getQuantityAvailable());
    }

    @Transactional(readOnly = true)
    public int getAvailableStock(Long productId) {
        return inventoryRepository.findByProductId(productId)
                .map(Inventory::getQuantityAvailable)
                .orElseThrow(() -> new ResourceNotFoundException("Inventory for product", productId));
    }
}
```

**`NotificationService`** — separated from `OrderService` with `REQUIRES_NEW` so a notification failure doesn't roll back the order creation. In production this would dispatch to a message queue; here it logs:

```java
package com.example.ordermanagement.service;

import com.example.ordermanagement.entity.Order;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Service
@Slf4j
public class NotificationService {

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendOrderConfirmation(Order order) {
        try {
            log.info("Sending order confirmation for order {} to user {}",
                    order.getId(), order.getUser().getEmail());
            // In production: publish to SQS/Kafka, call email service, etc.
        } catch (Exception e) {
            // Log but don't rethrow — notification failure should not roll back the order.
            log.error("Failed to send confirmation for order {}: {}", order.getId(), e.getMessage());
        }
    }
}
```

**`IdempotencyService`:**

```java
package com.example.ordermanagement.service;

import com.example.ordermanagement.entity.IdempotencyRecord;
import com.example.ordermanagement.repository.IdempotencyRecordRepository;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class IdempotencyService {

    private final IdempotencyRecordRepository recordRepository;
    private final ObjectMapper objectMapper;

    @Transactional(readOnly = true)
    public Optional<IdempotencyRecord> findExistingRecord(String key) {
        return recordRepository.findById(key);
    }

    /**
     * Persists the idempotency record in its own transaction (REQUIRES_NEW) so that
     * it's committed regardless of what the outer order-creation transaction does.
     * The unique constraint on idempotency_key (the @Id column) handles the race:
     * two concurrent requests with the same key both try to INSERT; one succeeds,
     * the other gets a DataIntegrityViolationException, which the caller handles
     * by re-reading the record the winner just persisted.
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void saveRecord(String key, Object responseBody, int httpStatus) {
        try {
            String json = objectMapper.writeValueAsString(responseBody);
            IdempotencyRecord record = new IdempotencyRecord(key, json, httpStatus);
            recordRepository.save(record);
        } catch (DataIntegrityViolationException e) {
            log.debug("Concurrent duplicate for idempotency key {} — winner already committed.", key);
        } catch (JsonProcessingException e) {
            log.error("Could not serialize response for idempotency key {}", key, e);
        }
    }
}
```

**`OrderService`** — the heart of the application:

```java
package com.example.ordermanagement.service;

import com.example.ordermanagement.dto.request.CreateOrderRequest;
import com.example.ordermanagement.dto.response.OrderResponse;
import com.example.ordermanagement.entity.Order;
import com.example.ordermanagement.entity.OrderItem;
import com.example.ordermanagement.entity.OrderStatus;
import com.example.ordermanagement.entity.Product;
import com.example.ordermanagement.entity.User;
import com.example.ordermanagement.exception.InvalidOrderStateException;
import com.example.ordermanagement.exception.ResourceNotFoundException;
import com.example.ordermanagement.repository.OrderRepository;
import com.example.ordermanagement.repository.ProductRepository;
import com.example.ordermanagement.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.EnumSet;

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {

    private static final EnumSet<OrderStatus> CANCELLABLE_STATUSES =
            EnumSet.of(OrderStatus.PENDING, OrderStatus.CONFIRMED);

    private final OrderRepository orderRepository;
    private final UserRepository userRepository;
    private final ProductRepository productRepository;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    @Transactional
    public OrderResponse createOrder(Long userId, CreateOrderRequest request) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User", userId));

        Order order = new Order(user);

        for (CreateOrderRequest.OrderItemRequest itemRequest : request.items()) {
            Product product = productRepository.findById(itemRequest.productId())
                    .orElseThrow(() -> new ResourceNotFoundException("Product", itemRequest.productId()));

            // Decrement stock — raises InsufficientStockException if not enough,
            // or OptimisticLockingFailureException if concurrent update lost the race.
            inventoryService.decrementStock(product, itemRequest.quantity());

            OrderItem item = new OrderItem(product, itemRequest.quantity(), product.getPrice());
            order.addItem(item);  // totalAmount is accumulated inside addItem()
        }

        Order saved = orderRepository.save(order);

        // Notification runs in its own REQUIRES_NEW transaction — failure here
        // does not roll back the order. Called via injected bean, not 'this'.
        notificationService.sendOrderConfirmation(saved);

        log.info("Created order {} for user {}, total: {}",
                saved.getId(), userId, saved.getTotalAmount());
        return OrderResponse.from(saved);
    }

    @Transactional(readOnly = true)
    public OrderResponse getOrderById(Long orderId) {
        Order order = orderRepository.findByIdWithItemsAndProducts(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order", orderId));
        return OrderResponse.from(order);
    }

    @Transactional(readOnly = true)
    public Page<OrderResponse> getOrdersForUser(Long userId, Pageable pageable) {
        if (!userRepository.existsById(userId)) {
            throw new ResourceNotFoundException("User", userId);
        }
        return orderRepository.findByUserId(userId, pageable)
                .map(OrderResponse::from);
    }

    @Transactional
    public OrderResponse cancelOrder(Long orderId, Long requestingUserId) {
        Order order = orderRepository.findByIdWithItemsAndProducts(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order", orderId));

        if (!order.getUser().getId().equals(requestingUserId)) {
            throw new ResourceNotFoundException("Order", orderId); // 404, not 403 — don't confirm existence
        }

        if (!CANCELLABLE_STATUSES.contains(order.getStatus())) {
            throw new InvalidOrderStateException(
                    "Order " + orderId + " cannot be cancelled — current status: " + order.getStatus());
        }

        order.setStatus(OrderStatus.CANCELLED);
        // Restore inventory for each item
        for (OrderItem item : order.getItems()) {
            inventoryService.decrementStock(item.getProduct(), -item.getQuantity()); // negative = restore
        }

        return OrderResponse.from(order);
    }
}
```

One detail in `cancelOrder` worth flagging: when the requesting user doesn't own the order, we throw `ResourceNotFoundException` (which becomes a `404`) rather than an authorization-specific exception (which would become a `403`). This is a security pattern called "security through obscurity at the resource level" — confirming "you're not allowed to access *that specific order*" leaks the information that *that specific order exists at all*. Returning a 404 instead prevents an attacker from enumerating valid order IDs by probing the API and watching for 403s to appear instead of 404s. Whether this trade-off is worth it depends on your threat model; in an order management API, it usually is, because order IDs are sequential and guessable.

> **Interview Question — SDE-2:** "In `OrderService.createOrder`, the order is saved and then a notification is sent. If the notification throws an exception, what happens to the order?"
>
> **Answer:** Nothing — the order is committed. `notificationService.sendOrderConfirmation()` runs in its own `REQUIRES_NEW` transaction, because `NotificationService` is a separate Spring-managed bean (so the call goes through its proxy and the annotation is honored), and `REQUIRES_NEW` creates an independent transaction that either commits or rolls back independently of `createOrder`'s outer transaction. On top of that, the `sendOrderConfirmation` implementation itself catches and logs exceptions rather than rethrowing them, so no exception propagates back to `createOrder` to trigger *its* transaction's rollback either. The notification failure is logged, the order commit happens normally, and the user gets a successful response — which is the correct behavior. An email delivery failure should be an operational concern dealt with by a retry mechanism, not a reason to undo a completed order.

---

With the service layer wired up, the next part builds the controller layer — the HTTP-facing surface that receives requests, delegates to services, and shapes the responses.
