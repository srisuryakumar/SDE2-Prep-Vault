# Spring Boot and Backend Engineering: Building Production-Grade REST APIs

A complete, self-contained learning book for an engineer who knows Java and databases but has never touched Spring Boot. By the end, you will have built — and be able to explain at an SDE-2 interview level — a fully tested, documented, production-ready **Order Management API**.

## How this book is organized

This is a multi-file book. Each file is self-contained enough to read on its own, but they build on each other in order, because the Order Management API itself is built incrementally, chapter by chapter, exactly like a real project would be.

| # | File | Covers |
|---|---|---|
| 1 | `01-chapter1-http-protocol.md` | HTTP request/response structure, methods, idempotency, status codes, headers, HTTP/1.1 vs HTTP/2, TLS |
| 2 | `02-chapter2-rest-api-design.md` | Resource naming, URL design, pagination, versioning, idempotency keys, Richardson Maturity Model |
| 3 | `03-chapter3-spring-boot-internals.md` | Auto-configuration, the IoC container, bean lifecycle, DI, bean scopes, startup sequence, configuration binding |
| 4 | `04-chapter4-part1-entities-and-jpa.md` | All five JPA entities for the Order Management API, relationships, fetch types, optimistic locking |
| 5 | `05-chapter4-part2-repository-layer.md` | `JpaRepository`, derived queries, JPQL/native `@Query`, bulk updates, pagination |
| 6 | `06-chapter4-part3-n-plus-one-problem.md` | Reproducing, detecting, and fixing the N+1 problem three different ways |
| 7 | `07-chapter4-part4-service-layer.md` | `@Transactional`, propagation, the self-invocation trap, business logic, optimistic-lock retries |
| 8 | `08-chapter4-part5-controller-layer.md` | `@RestController`, request mapping, `ResponseEntity`, the 201 + `Location` pattern |
| 9 | `09-chapter4-part6-validation-and-exceptions.md` | Bean Validation, custom constraints, `@RestControllerAdvice`, the standard error envelope |
| 10 | `10-chapter5-security-jwt.md` | Stateless auth, JWT internals, the auth filter, OAuth2 Resource Server, method security, CORS/CSRF |
| 11 | `11-chapter6-testing.md` | The testing pyramid, `@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest`, Testcontainers, async testing |
| 12 | `12-chapter7-documentation-production.md` | OpenAPI/Swagger, Actuator, health indicators, profiles, graceful shutdown |
| 13 | `13-chapter8-spring-aop.md` | What AOP solves, the proxy mechanism, writing a logging aspect, why self-invocation breaks it |
| 14 | `14-chapter9-flyway.md` | Versioned migrations, naming conventions, zero-downtime migration strategy |
| 15 | `15-chapter10-deployment.md` | Live Swagger UI, Dockerizing the app, deploying it publicly, the README badge interviewers click |

Chapter 4 in the original outline is enormous — entities, repositories, the N+1 problem, the service layer, the controller layer, validation, and exception handling are all "Chapter 4" conceptually. Splitting it into six files (4–9 above) keeps each one a readable sitting while preserving the original structure; each file's heading tells you which part of Chapter 4 it is.

## The application we build: Order Management API

Every chapter adds a layer to the same system, so there's never a throwaway example. The domain is intentionally small but realistic enough to need every concept the book teaches:

- **User** — an account that can place orders. Has a `role` (`CUSTOMER` or `ADMIN`).
- **Product** — something that can be sold. Has a price and a SKU.
- **Inventory** — the stock count for a product. Kept as its own entity (not just a column on `Product`) specifically so we have a natural, realistic example for optimistic locking: two customers racing for the last unit of a product is exactly the scenario `@Version` exists to solve.
- **Order** — a purchase made by a `User`, made up of one or more `OrderItem`s, with a status that moves through `PENDING → CONFIRMED → SHIPPED → DELIVERED` (or `CANCELLED`).
- **OrderItem** — a line item: a product, a quantity, and the price *at the time of purchase* (which must be captured separately from `Product.price`, since prices change and historical orders shouldn't).

```
User (1) ──< Order (N) ──< OrderItem (N) >── Product (1) ──── Inventory (1)
```

By the end of the book, the project's file tree looks like this:

```
order-management/
├── pom.xml
├── docker-compose.yml
├── Dockerfile
├── src
│   ├── main
│   │   ├── java/com/example/ordermanagement
│   │   │   ├── OrderManagementApplication.java
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.java
│   │   │   │   └── OpenApiConfig.java
│   │   │   ├── controller/
│   │   │   │   ├── AuthController.java
│   │   │   │   ├── ProductController.java
│   │   │   │   └── OrderController.java
│   │   │   ├── service/
│   │   │   │   ├── AuthService.java
│   │   │   │   ├── ProductService.java
│   │   │   │   ├── OrderService.java
│   │   │   │   ├── InventoryService.java
│   │   │   │   ├── IdempotencyService.java
│   │   │   │   ├── NotificationService.java
│   │   │   │   └── CustomUserDetailsService.java
│   │   │   ├── repository/
│   │   │   │   ├── UserRepository.java
│   │   │   │   ├── ProductRepository.java
│   │   │   │   ├── InventoryRepository.java
│   │   │   │   ├── OrderRepository.java
│   │   │   │   ├── OrderItemRepository.java
│   │   │   │   └── IdempotencyRecordRepository.java
│   │   │   ├── entity/
│   │   │   │   ├── User.java, Product.java, Inventory.java
│   │   │   │   ├── Order.java, OrderItem.java, IdempotencyRecord.java
│   │   │   │   └── Role.java, OrderStatus.java   (enums)
│   │   │   ├── dto/
│   │   │   │   ├── request/  (CreateOrderRequest, RegisterRequest, ...)
│   │   │   │   └── response/ (OrderResponse, ErrorResponse, ...)
│   │   │   ├── exception/
│   │   │   │   ├── ResourceNotFoundException.java, InsufficientStockException.java
│   │   │   │   ├── DuplicateResourceException.java
│   │   │   │   └── GlobalExceptionHandler.java
│   │   │   ├── security/
│   │   │   │   ├── JwtService.java
│   │   │   │   └── JwtAuthenticationFilter.java
│   │   │   └── aspect/
│   │   │       └── PerformanceLoggingAspect.java
│   │   └── resources/
│   │       ├── application.yml, application-local.yml, application-prod.yml
│   │       └── db/migration/  (Flyway scripts, from Chapter 9 onward)
│   └── test/java/com/example/ordermanagement/...
```

You don't need to create this tree up front — it's built piece by piece, file by file, as each chapter introduces it. This is just the map for reference.

## A note on versions (and why they were chosen deliberately)

This book targets **Spring Boot 3.5.x, Spring Framework 6.x, Java 21 (LTS), and Maven**. That choice was checked against the current state of the ecosystem rather than assumed, and it's worth explaining briefly because version confusion is a real source of frustration when you're learning from any book or tutorial.

As of mid-2026, **Spring Boot 4.0 (built on Spring Framework 7 and Jakarta EE 11) has shipped** and is Spring's recommended line for brand-new projects. It is not a drop-in version bump — it's a genuinely substantial migration, arguably the biggest since the `javax.*` → `jakarta.*` rename in Boot 3.0. It raises the Java floor to 21, moves to Jackson 3.x, rewrites several Spring Security defaults (CSRF is now enforced by default on API-style configurations, `authorizeRequests()` is gone), renames a number of starter artifacts, and removes APIs that had been deprecated throughout the 3.x line — including `@MockBean`/`@SpyBean`, which is exactly why this book uses their replacement, `@MockitoBean`, from the start in Chapter 6.

Given that scope of change, and given that the overwhelming majority of production codebases, interview question banks, and existing documentation you'll encounter right now are still on the 3.x line (major enterprise frameworks take years, not months, to roll out across real companies), **3.5.x is the more useful version to learn on**. More importantly: every internal mechanism this book teaches — how the IoC container builds and wires beans, how the AOP proxy behind `@Transactional` actually works, how Hibernate translates entity relationships into SQL, how transaction propagation behaves — is conceptually unchanged between 3.x and 4.x. None of that is Boot-4-specific knowledge that will go stale. When you're ready to start a brand-new project on 4.x, generate it fresh from [start.spring.io](https://start.spring.io) (which will default to whatever Spring currently recommends) and read Spring's own migration guide for the mechanical, dependency-version parts — the concepts in this book transfer directly.

## Prerequisites

You should already be comfortable with: Java syntax including generics, interfaces, and lambdas; basic SQL (`SELECT`, `JOIN`, `INSERT`, transactions conceptually); and using a terminal and Git. You do **not** need any prior Spring experience — that's the entire point of this book.

You'll want: a JDK 21 installation, Maven (or just use the Maven wrapper Spring Initializr generates), Docker (for PostgreSQL locally and for Testcontainers), and an IDE (IntelliJ IDEA Community Edition is the most common choice for Spring work).

## How to read the code listings

Every code listing in this book is a **complete file**, not a fragment with `// ...` standing in for the boring parts. That's deliberate: you should be able to copy a listing straight into a file with the path given above it and have it compile as part of the wider project, once the surrounding files from earlier in the book exist. Where a listing only *adds* something to a file you already created in an earlier chapter (like `application.yml`, which grows throughout the book), the heading says so explicitly, and the full, accumulated file is shown — not just the delta — so you always have something pasteable.

Throughout the book you'll see boxes like this one after most major concepts:

> **Interview Question — SDE-2:** A representative question an interviewer might actually ask about the preceding concept.
>
> **Answer:** The depth of answer an SDE-2 candidate is expected to give — not just "what" the annotation does, but "how," internally.

Let's start with the protocol everything else sits on top of.
