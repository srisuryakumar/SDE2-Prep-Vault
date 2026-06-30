# Chapter 7: API Documentation and Production Readiness

## 7.1 OpenAPI / Swagger with springdoc

OpenAPI (formerly Swagger) is a specification for describing REST APIs in a machine-readable format (JSON or YAML). `springdoc-openapi` reads your Spring Boot annotations — `@RestController`, `@GetMapping`, DTOs, validation constraints — and generates this specification at `/v3/api-docs` automatically. It also serves a browser-based interactive UI at `/swagger-ui.html` where anyone can read your endpoint documentation and execute requests directly, including requests that require a JWT.

Add the dependency:

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.8</version>
</dependency>
```

With just this dependency, `http://localhost:8080/swagger-ui.html` is already live. The auto-generated documentation is correct and complete for simple cases. For a polished, public-facing API, you add annotations to fill in descriptions, examples, and authentication schemes.

## 7.2 OpenAPI configuration

```java
package com.example.ordermanagement.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Value("${spring.application.name}")
    private String appName;

    @Bean
    public OpenAPI orderManagementOpenAPI() {
        final String securitySchemeName = "bearerAuth";

        return new OpenAPI()
                .info(new Info()
                        .title("Order Management API")
                        .description("A production-grade REST API for managing orders, products, and users.")
                        .version("v1.0.0")
                        .contact(new Contact()
                                .name("Order Management Team")
                                .email("support@ordermanagement.com"))
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")))
                .servers(List.of(
                        new Server().url("http://localhost:8080").description("Local development"),
                        new Server().url("https://api.ordermanagement.com").description("Production")
                ))
                // Declare the JWT bearer auth scheme
                .components(new Components()
                        .addSecuritySchemes(securitySchemeName,
                                new SecurityScheme()
                                        .name(securitySchemeName)
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("Paste your JWT access token here. " +
                                                "Obtain one from POST /v1/auth/login.")))
                // Apply the auth scheme globally — every endpoint requires a JWT by default
                // unless overridden at the operation level with @SecurityRequirements({})
                .addSecurityItem(new SecurityRequirement().addList(securitySchemeName));
    }
}
```

## 7.3 Annotating controllers and DTOs

The OpenAPI spec auto-generated from Spring annotations is functional, but adding descriptions and examples makes the Swagger UI genuinely useful for a first-time reader:

```java
// OrderController — selected annotations shown

@RestController
@RequestMapping("/v1")
@Tag(name = "Orders", description = "Create, retrieve, and cancel customer orders")
@RequiredArgsConstructor
public class OrderController {

    @GetMapping("/orders/{id}")
    @Operation(
            summary = "Get an order by ID",
            description = "Returns the full order, including all line items and their products. " +
                          "Requires authentication. Users can only retrieve their own orders; " +
                          "ADMIN role can retrieve any order."
    )
    @ApiResponse(responseCode = "200", description = "Order found",
            content = @Content(schema = @Schema(implementation = OrderResponse.class)))
    @ApiResponse(responseCode = "401", description = "Missing or invalid JWT")
    @ApiResponse(responseCode = "404", description = "Order not found")
    public ResponseEntity<OrderResponse> getOrder(@Parameter(description = "Order ID") @PathVariable Long id) {
        return ResponseEntity.ok(orderService.getOrderById(id));
    }
```

For DTOs, `@Schema` adds description and example values:

```java
// OrderResponse record — with OpenAPI annotations
public record OrderResponse(
        @Schema(description = "Unique order identifier", example = "9001")
        Long id,

        @Schema(description = "ID of the user who placed the order", example = "42")
        Long userId,

        @Schema(description = "Current order status", example = "PENDING")
        OrderStatus status,

        @Schema(description = "Total order amount in USD", example = "145.50")
        BigDecimal totalAmount,

        List<OrderItemResponse> items,

        @Schema(description = "When the order was placed (UTC)", example = "2026-06-18T09:15:30Z")
        Instant createdAt
) { ... }
```

```yaml
# application.yml — springdoc settings
springdoc:
  swagger-ui:
    path: /swagger-ui.html
    display-request-duration: true
    operations-sorter: method
    tags-sorter: alpha
    try-it-out-enabled: true
  api-docs:
    path: /v3/api-docs
  show-actuator: false
```

## 7.4 Spring Boot Actuator

Actuator adds a set of production-ready HTTP endpoints that expose the operational health of the application — not business data, but infrastructure state: is the database reachable, how much memory is in use, what are the last N log entries.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

With the dependency added, `/actuator/health` is available immediately, returning:

```json
{
  "status": "UP",
  "components": {
    "db": { "status": "UP", "details": { "database": "PostgreSQL", "validationQuery": "isValid()" } },
    "diskSpace": { "status": "UP", "details": { "total": 499963174912, "free": 321854210048 } },
    "ping": { "status": "UP" }
  }
}
```

Configure which endpoints are exposed and secured:

```yaml
# application.yml (accumulated)
management:
  endpoints:
    web:
      exposure:
        include: health, info, metrics, prometheus
      base-path: /actuator
  endpoint:
    health:
      show-details: when-authorized   # Full details for authenticated users, UP/DOWN for others
      show-components: when-authorized
    info:
      enabled: true
  info:
    env:
      enabled: true
    build:
      enabled: true

# Info endpoint content
info:
  application:
    name: Order Management API
    version: "@project.version@"     # Maven property — interpolated at build time
    description: Production-grade REST API for order management
```

The `@project.version@` syntax is resource filtering — Maven replaces it with the actual version from `pom.xml` during the build, so the info endpoint always shows the deployed artifact version without manual updates.

## 7.5 Custom health indicator

Spring Boot auto-configures health checks for its own managed resources (database, disk space). For external dependencies *your* code talks to — a third-party payment gateway, a shipping provider's API — write your own:

```java
package com.example.ordermanagement.health;

import lombok.RequiredArgsConstructor;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Component("orderDb")
@RequiredArgsConstructor
public class OrderDatabaseHealthIndicator implements HealthIndicator {

    private final JdbcTemplate jdbcTemplate;

    @Override
    public Health health() {
        try {
            Long count = jdbcTemplate.queryForObject(
                    "SELECT COUNT(*) FROM orders", Long.class);
            return Health.up()
                    .withDetail("totalOrders", count)
                    .withDetail("connectionPool", "HikariCP")
                    .build();
        } catch (Exception e) {
            return Health.down()
                    .withDetail("error", e.getMessage())
                    .build();
        }
    }
}
```

The component name (`"orderDb"`) becomes the key in the health response's `components` map. Spring Boot calls `health()` each time `/actuator/health` is requested (or on a configurable schedule with health caching). A `Health.down()` response causes the aggregate status to become `DOWN`, which is what Kubernetes liveness probes read to decide whether to restart a pod.

## 7.6 Prometheus metrics

`/actuator/prometheus` (from the Micrometer library, auto-configured when `io.micrometer:micrometer-registry-prometheus` is on the classpath) exposes metrics in Prometheus text format, ready for scraping by a Prometheus server and visualization in Grafana:

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

Out of the box you get JVM metrics (`jvm_memory_used_bytes`, `jvm_gc_pause_seconds`), HTTP request metrics (`http_server_requests_seconds_count`, `http_server_requests_seconds_sum` — from which p95/p99 latency is computable), HikariCP pool metrics (`hikaricp_connections_active`, `hikaricp_connections_pending`), and more.

Custom application metrics with Micrometer:

```java
package com.example.ordermanagement.service;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class MetricsService {

    private final Counter orderCreatedCounter;
    private final Counter orderCancelledCounter;
    private final Timer orderCreationTimer;

    public MetricsService(MeterRegistry registry) {
        this.orderCreatedCounter = Counter.builder("orders.created")
                .description("Total number of orders created successfully")
                .register(registry);

        this.orderCancelledCounter = Counter.builder("orders.cancelled")
                .description("Total number of orders cancelled")
                .register(registry);

        this.orderCreationTimer = Timer.builder("orders.creation.duration")
                .description("Time taken to create an order")
                .register(registry);
    }

    public void recordOrderCreated() { orderCreatedCounter.increment(); }
    public void recordOrderCancelled() { orderCancelledCounter.increment(); }
    public Timer.Sample startOrderCreationTimer() { return Timer.start(); }
    public void stopOrderCreationTimer(Timer.Sample sample) {
        sample.stop(orderCreationTimer);
    }
}
```

Inject `MetricsService` into `OrderService` and call `recordOrderCreated()` after a successful save — five minutes of work that gives you a queryable, graphable counter of "how many orders per minute is this application creating?" in production.

## 7.7 Profiles: local, staging, production

Spring profiles let you maintain different configurations per environment without maintaining different codebases or hardcoding environment checks:

```yaml
# src/main/resources/application.yml — base defaults, all environments
server:
  port: 8080
spring:
  application:
    name: order-management
  jpa:
    open-in-view: false
  jackson:
    default-property-inclusion: non_null
    serialization:
      write-dates-as-timestamps: false
```

```yaml
# src/main/resources/application-local.yml — local development overrides
spring:
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
logging:
  level:
    com.example.ordermanagement: DEBUG
    org.hibernate.SQL: DEBUG
```

```yaml
# src/main/resources/application-prod.yml — production overrides
spring:
  datasource:
    # Actual values come from environment variables — not committed to source control
    url: ${DATABASE_URL}
    username: ${DATABASE_USERNAME}
    password: ${DATABASE_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 10
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
  jpa:
    hibernate:
      ddl-auto: validate    # Never let Hibernate modify the schema in production
    show-sql: false
    properties:
      hibernate:
        generate_statistics: false

server:
  error:
    include-stacktrace: never   # Never expose stack traces in error responses

management:
  endpoints:
    web:
      exposure:
        include: health, prometheus   # No /info or /metrics in prod — scrape Prometheus instead
  endpoint:
    health:
      show-details: never    # Don't expose internal details to unauthenticated callers in prod

logging:
  level:
    root: WARN
    com.example.ordermanagement: INFO
```

Activate a profile:
```bash
# As a system property
java -jar order-management.jar --spring.profiles.active=local

# As an environment variable (Docker/Kubernetes)
SPRING_PROFILES_ACTIVE=prod java -jar order-management.jar
```

## 7.8 Graceful shutdown

When a container platform (Kubernetes, ECS) decides to replace a running instance of your application — whether for a deployment, autoscaling, or an instance failure — it sends a `SIGTERM` signal to the process. Without graceful shutdown, the JVM exits immediately, dropping any in-flight HTTP requests mid-response. With graceful shutdown, the process:

1. Stops accepting new requests (the OS closes the listening socket).
2. Waits for all in-flight requests to complete, up to a configurable timeout.
3. Runs `@PreDestroy` methods and closes managed resources.
4. Exits cleanly.

```yaml
# application.yml (and especially application-prod.yml)
server:
  shutdown: graceful   # Boot 2.3+ — replaces immediate shutdown with the above sequence

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s  # How long to wait for in-flight requests before forcing exit
```

Pair this with Kubernetes's `terminationGracePeriodSeconds` (set to slightly longer than your `timeout-per-shutdown-phase`, so Kubernetes doesn't force-kill the container before Spring's graceful shutdown completes) and a readiness probe that returns `DOWN` as soon as shutdown starts (which Kubernetes reads as "stop routing new traffic here" — Spring Boot automatically does this):

```yaml
# In Kubernetes deployment spec:
spec:
  containers:
    - name: order-management
      livenessProbe:
        httpGet:
          path: /actuator/health/liveness
          port: 8080
        initialDelaySeconds: 30
        periodSeconds: 10
      readinessProbe:
        httpGet:
          path: /actuator/health/readiness
          port: 8080
        initialDelaySeconds: 15
        periodSeconds: 5
  terminationGracePeriodSeconds: 60
```

Spring Boot 2.3+ exposes `/actuator/health/liveness` (is the application alive, or should it be restarted) and `/actuator/health/readiness` (is the application ready to serve traffic) as separate endpoints — exactly the split Kubernetes expects, where readiness failing doesn't necessarily mean the instance should be killed, just that traffic should stop being routed to it.

> **Interview Question — SDE-2:** "Walk through what happens to an in-flight request if Kubernetes sends a SIGTERM to the pod while `POST /v1/orders` is executing in the middle of the database transaction."
>
> **Answer:** With `server.shutdown=graceful` configured, the embedded Tomcat server receives the shutdown event and immediately stops accepting new connections — the socket is closed. Any already-executing request, including the `POST /v1/orders` transaction in progress, continues to completion. Tomcat's thread pool keeps the active threads running and the `timeout-per-shutdown-phase` sets the ceiling: if the order transaction finishes within that window (30 seconds in our configuration), it commits normally, the response is sent to the client, and the thread releases. The process then finishes the lifecycle shutdown (running `@PreDestroy` callbacks, closing the connection pool, etc.) and exits. If the request *doesn't* finish within the timeout window — which would be a bug, since an order creation that takes 30 seconds has other problems — Tomcat cancels it and exits anyway. The client receives an abrupt connection close, which it should treat as a retriable failure (using the idempotency key to safely retry, as implemented in Chapter 4). On the Kubernetes side, the readiness probe returns `DOWN` as soon as the shutdown sequence begins, so the load balancer stops routing new traffic to this instance before any of this happens — the SIGTERM doesn't come as a surprise to the load balancer.

---

The application is documented, observable, and deployed safely. Chapter 8 steps back to look at the mechanism that makes `@Transactional`, security filtering, and several of this chapter's observability patterns possible: Spring AOP.
