# Chapter 6: Testing the Application

## 6.1 The testing pyramid

The testing pyramid is a heuristic about the mix of test types a well-tested application should have:

```
              /\
             /  \
            / E2E\
           /──────\
          /        \
         /Integration\
        /────────────\
       /              \
      /   Unit Tests   \
     /──────────────────\
```

**Unit tests** are at the base — they're the majority. They test a single class in isolation, with all dependencies replaced by controlled substitutes (mocks). They're fast (milliseconds), have no external dependencies, and pinpoint failures to a single class. `OrderService.createOrder()` with mocked repositories is a unit test.

**Integration tests** are in the middle — fewer, slower, but they verify that components work *together*. `@WebMvcTest` (testing the controller layer with real request parsing but mocked service) and `@DataJpaTest` (testing the repository layer against a real database) are both integration tests.

**End-to-end tests** are at the top — the fewest, slowest, and most expensive to maintain. They exercise the full system from the outside as a real client would — `POST /v1/orders` against a running application with real database, real JWT, the whole stack. `@SpringBootTest` with a `TestRestTemplate` is Spring Boot's answer to this.

The shape of the pyramid matters: a codebase where most tests are E2E tests has a test suite that's slow, flaky, expensive to maintain, and bad at pinpointing failures. A codebase where every test is a unit test has a suite that's fast and precise but misses integration problems (the database query that works in code but fails against a real schema, the security filter that's not configured correctly, the Jackson serialization edge case). Both extremes are real failure modes on real teams.

## 6.2 A note on `@MockitoBean` vs. the deprecated `@MockBean`

Spring Boot 3.4 deprecated `@MockBean` and `@SpyBean` in favor of `@MockitoBean` and `@MockitoSpyBean`. The behavior is identical — they both create a Mockito mock and register it as the Spring bean for that type in the test application context, replacing any real bean of that type. The rename is purely to decouple the feature from the Spring Boot testing layer and to align with Spring Framework 6.2's direct Mockito integration.

This book uses `@MockitoBean` throughout. If you encounter older tutorials or codebases using `@MockBean`, they're referring to the same mechanism under the old name — the only thing that changes is which annotation you write.

## 6.3 `@WebMvcTest`: controller unit tests

`@WebMvcTest` loads *only* the web layer: the `DispatcherServlet`, MVC configuration, request/response serialization (Jackson), filter chain, and any `@ControllerAdvice` classes — but **not** the `ApplicationContext`'s service or repository beans. Any service you depend on must be mocked. This makes `@WebMvcTest` fast (sub-second startup in most cases) and focused: a test failure here means the HTTP layer has a bug.

**Dependencies for testing:**

```xml
<!-- Already in pom.xml from Chapter 3 as spring-boot-starter-test.
     Explicitly listing what that starter includes: -->
<!-- junit-jupiter, mockito-core, mockito-junit-jupiter,
     spring-test, spring-boot-test,
     assertj-core, hamcrest, jsonpath, jackson-databind -->

<!-- Add for Testcontainers (Chapter 6.6): -->
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
```

Add the Testcontainers BOM to the `<dependencyManagement>` section so you don't need versions on each artifact:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>testcontainers-bom</artifactId>
            <version>1.20.4</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**`OrderControllerTest`:**

```java
package com.example.ordermanagement.controller;

import com.example.ordermanagement.dto.request.CreateOrderRequest;
import com.example.ordermanagement.dto.response.OrderResponse;
import com.example.ordermanagement.entity.OrderStatus;
import com.example.ordermanagement.entity.User;
import com.example.ordermanagement.exception.InsufficientStockException;
import com.example.ordermanagement.exception.ResourceNotFoundException;
import com.example.ordermanagement.security.JwtService;
import com.example.ordermanagement.service.IdempotencyService;
import com.example.ordermanagement.service.OrderService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.isNull;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    // @MockitoBean replaces the real bean in the test context
    @MockitoBean
    private OrderService orderService;

    @MockitoBean
    private IdempotencyService idempotencyService;

    // @WebMvcTest loads Spring Security — JwtService is needed by the filter
    @MockitoBean
    private JwtService jwtService;

    private User testUser;
    private OrderResponse testOrderResponse;

    @BeforeEach
    void setUp() {
        testUser = new User("alice", "alice@example.com", "hashed", com.example.ordermanagement.entity.Role.CUSTOMER);
        // Use reflection to set ID since there's no setter (we could add a package-private one for tests)
        // In practice, using a builder or test factory is cleaner. Here we use Mockito:
        testUser = org.mockito.Mockito.spy(testUser);
        org.mockito.Mockito.when(testUser.getId()).thenReturn(1L);

        testOrderResponse = new OrderResponse(
                9001L, 1L, OrderStatus.PENDING, new BigDecimal("145.50"),
                List.of(new OrderResponse.OrderItemResponse(1L, 42L, "Widget", 2, new BigDecimal("50.00"))),
                Instant.now()
        );
    }

    @Test
    @WithMockUser(username = "alice@example.com", roles = "CUSTOMER")
    void getOrder_whenOrderExists_returns200WithBody() throws Exception {
        when(orderService.getOrderById(9001L)).thenReturn(testOrderResponse);

        mockMvc.perform(get("/v1/orders/9001")
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(9001))
                .andExpect(jsonPath("$.status").value("PENDING"))
                .andExpect(jsonPath("$.totalAmount").value(145.50))
                .andExpect(jsonPath("$.items[0].productName").value("Widget"));
    }

    @Test
    @WithMockUser(roles = "CUSTOMER")
    void getOrder_whenOrderNotFound_returns404() throws Exception {
        when(orderService.getOrderById(anyLong()))
                .thenThrow(new ResourceNotFoundException("Order", 999L));

        mockMvc.perform(get("/v1/orders/999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.error").value("Not Found"));
    }

    @Test
    void getOrder_withoutAuthentication_returns401() throws Exception {
        mockMvc.perform(get("/v1/orders/9001"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void createOrder_withValidRequest_returns201WithLocation() throws Exception {
        when(idempotencyService.findExistingRecord(any())).thenReturn(Optional.empty());
        when(orderService.createOrder(anyLong(), any())).thenReturn(testOrderResponse);

        var request = new CreateOrderRequest(
                List.of(new CreateOrderRequest.OrderItemRequest(42L, 2)));
        String requestJson = objectMapper.writeValueAsString(request);

        mockMvc.perform(post("/v1/orders")
                        .with(user(testUser))   // inject our User entity as the principal
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestJson))
                .andExpect(status().isCreated())
                .andExpect(header().exists("Location"))
                .andExpect(jsonPath("$.id").value(9001));
    }

    @Test
    void createOrder_withEmptyItems_returns422() throws Exception {
        var request = new CreateOrderRequest(List.of());
        String requestJson = objectMapper.writeValueAsString(request);

        mockMvc.perform(post("/v1/orders")
                        .with(user(testUser))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestJson))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.validationErrors").exists());
    }

    @Test
    void createOrder_withInsufficientStock_returns422() throws Exception {
        when(idempotencyService.findExistingRecord(any())).thenReturn(Optional.empty());
        when(orderService.createOrder(anyLong(), any()))
                .thenThrow(new InsufficientStockException("WIDGET-001", 5, 2));

        var request = new CreateOrderRequest(
                List.of(new CreateOrderRequest.OrderItemRequest(42L, 5)));
        String requestJson = objectMapper.writeValueAsString(request);

        mockMvc.perform(post("/v1/orders")
                        .with(user(testUser))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestJson))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.message").value(
                        org.hamcrest.Matchers.containsString("Insufficient stock")));
    }
}
```

## 6.4 `@DataJpaTest`: repository layer tests

`@DataJpaTest` loads only the JPA infrastructure: repositories, the `EntityManager`, the datasource, Hibernate — no web layer, no services. By default it replaces the real database with an in-memory H2 database and runs each test in a transaction that is rolled back at the end. This gives you a fast, isolated, zero-cleanup test environment for query logic.

The limitation: H2 doesn't speak PostgreSQL SQL. Features we use — `ILIKE`, Postgres-specific functions — will fail in H2. For those, Testcontainers (Section 6.6) is the answer. For pure JPQL and derived queries that work identically on any database, `@DataJpaTest` + H2 is a pragmatic default that's fast and dependency-free.

```java
package com.example.ordermanagement.repository;

import com.example.ordermanagement.entity.Order;
import com.example.ordermanagement.entity.OrderStatus;
import com.example.ordermanagement.entity.Role;
import com.example.ordermanagement.entity.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
class OrderRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private OrderRepository orderRepository;

    private User alice;
    private User bob;

    @BeforeEach
    void setUp() {
        alice = entityManager.persistAndFlush(
                new User("alice", "alice@example.com", "hash", Role.CUSTOMER));
        bob = entityManager.persistAndFlush(
                new User("bob", "bob@example.com", "hash", Role.CUSTOMER));

        Order o1 = new Order(alice);
        o1.setStatus(OrderStatus.PENDING);
        entityManager.persistAndFlush(o1);

        Order o2 = new Order(alice);
        o2.setStatus(OrderStatus.SHIPPED);
        entityManager.persistAndFlush(o2);

        Order o3 = new Order(bob);
        o3.setStatus(OrderStatus.PENDING);
        entityManager.persistAndFlush(o3);

        entityManager.clear(); // clear first-level cache — subsequent reads go to DB
    }

    @Test
    void findByUserId_returnsOnlyThatUsersOrders() {
        Page<Order> page = orderRepository.findByUserId(alice.getId(), PageRequest.of(0, 10));

        assertThat(page.getTotalElements()).isEqualTo(2);
        assertThat(page.getContent())
                .allMatch(o -> o.getUser().getId().equals(alice.getId()));
    }

    @Test
    void findByUserIdAndStatus_filtersCorrectly() {
        Page<Order> page = orderRepository.findByUserIdAndStatus(
                alice.getId(), OrderStatus.PENDING, PageRequest.of(0, 10));

        assertThat(page.getTotalElements()).isEqualTo(1);
        assertThat(page.getContent().get(0).getStatus()).isEqualTo(OrderStatus.PENDING);
    }

    @Test
    void findByIdWithItemsAndProducts_returnsEmpty_whenNotFound() {
        Optional<Order> result = orderRepository.findByIdWithItemsAndProducts(999L);
        assertThat(result).isEmpty();
    }
}
```

`TestEntityManager` is a Spring-provided wrapper around the JPA `EntityManager` that's more convenient in tests: `persistAndFlush()` saves an entity and immediately flushes to the database (essential because without it, Hibernate batches the INSERT and your subsequent reads might still see the cached, not-yet-written entity). `entityManager.clear()` after setup removes entities from the first-level cache, ensuring subsequent `findBy*` calls genuinely hit the database.

## 6.5 `@SpringBootTest`: full integration test

`@SpringBootTest` loads the complete `ApplicationContext` — every bean, every configuration, the full web server. It's the most faithful test of the real application, and the most expensive.

```java
package com.example.ordermanagement;

import com.example.ordermanagement.dto.request.LoginRequest;
import com.example.ordermanagement.dto.request.RegisterRequest;
import com.example.ordermanagement.dto.response.AuthResponse;
import com.example.ordermanagement.dto.response.OrderResponse;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.ActiveProfiles;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class OrderManagementIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void registerAndLoginFlow_returnsTokensSuccessfully() {
        // Register
        var registerRequest = new RegisterRequest("testuser", "testuser@example.com", "password123");
        ResponseEntity<AuthResponse> registerResponse = restTemplate.postForEntity(
                "/v1/auth/register", registerRequest, AuthResponse.class);

        assertThat(registerResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(registerResponse.getBody()).isNotNull();
        assertThat(registerResponse.getBody().accessToken()).isNotBlank();

        // Login
        var loginRequest = new LoginRequest("testuser@example.com", "password123");
        ResponseEntity<AuthResponse> loginResponse = restTemplate.postForEntity(
                "/v1/auth/login", loginRequest, AuthResponse.class);

        assertThat(loginResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(loginResponse.getBody().accessToken()).isNotBlank();
    }

    @Test
    void getOrder_withoutToken_returns401() {
        ResponseEntity<String> response = restTemplate.getForEntity(
                "/v1/orders/1", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.UNAUTHORIZED);
    }

    @Test
    void getOrder_withValidToken_returns404ForMissingOrder() {
        // First register and get a token
        var registerRequest = new RegisterRequest("finduser", "finduser@example.com", "password123");
        AuthResponse auth = restTemplate.postForEntity(
                "/v1/auth/register", registerRequest, AuthResponse.class).getBody();

        assertThat(auth).isNotNull();

        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(auth.accessToken());
        HttpEntity<Void> entity = new HttpEntity<>(headers);

        ResponseEntity<OrderResponse> response = restTemplate.exchange(
                "/v1/orders/999999", HttpMethod.GET, entity, OrderResponse.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }
}
```

`WebEnvironment.RANDOM_PORT` starts the server on a random available port — avoiding port conflicts when multiple test suites run simultaneously. `TestRestTemplate` is a test-friendly `RestTemplate` that handles the port binding automatically and doesn't throw on 4xx/5xx (it returns the `ResponseEntity` instead, which is what you want in tests — you're asserting on the status code, not catching an exception).

`@ActiveProfiles("test")` activates `application-test.yml` (or `application-test.properties`), allowing a test-specific datasource configuration (pointing to an in-memory H2 or, better, a Testcontainers PostgreSQL).

## 6.6 Testcontainers: why it beats H2 for serious tests

The `@DataJpaTest` + H2 combination has a fundamental limitation: H2 is not PostgreSQL. It doesn't support PostgreSQL-specific SQL syntax, it doesn't enforce constraints identically (PostgreSQL's `UNIQUE` and foreign key constraint violation behavior differs in subtle ways), and it doesn't support features like `FOR UPDATE SKIP LOCKED` used in some of our queries. Code that passes all H2 tests can still fail against PostgreSQL in ways you won't discover until deployment.

Testcontainers fixes this by spinning up a **real PostgreSQL container** (via Docker) for each test run. It's slower than H2 (seconds to start a container vs. milliseconds for H2), but it's testing against the exact database you deploy to.

```java
package com.example.ordermanagement;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import static org.assertj.core.api.Assertions.assertThat;

@Testcontainers
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class OrderManagementContainerTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
            .withDatabaseName("orderdb_test")
            .withUsername("test")
            .withPassword("test");

    /**
     * @DynamicPropertySource overrides spring.datasource.* properties at test startup,
     * using the actual port the container is listening on (which Docker assigns randomly).
     * This is how the test application context learns to connect to the test container
     * rather than to the URL in application.yml.
     */
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        // Use create-drop in tests so the schema is created fresh on each run
        registry.add("spring.jpa.hibernate.ddl-auto", () -> "create-drop");
    }

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void healthEndpoint_returnsUp() {
        ResponseEntity<String> response = restTemplate.getForEntity("/actuator/health", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }

    @Test
    void unauthenticatedRequest_to_protectedEndpoint_returns401() {
        ResponseEntity<String> response = restTemplate.getForEntity("/v1/orders/1", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.UNAUTHORIZED);
    }
}
```

The `@Container` annotation on a `static` field means the container is started once for the entire test class and shared across all test methods (faster than per-test containers). `@DynamicPropertySource` is the mechanism that bridges the dynamically-assigned container port to Spring's property system — without it, `spring.datasource.url` would still point at `localhost:5432` instead of wherever Docker bound the container.

## 6.7 `application-test.yml`

```yaml
# src/test/resources/application-test.yml
spring:
  jpa:
    show-sql: true
    hibernate:
      ddl-auto: create-drop
    properties:
      hibernate:
        format_sql: true
  # Datasource is overridden by @DynamicPropertySource in Testcontainers tests.
  # For tests that don't use Testcontainers, override here:
  datasource:
    url: jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=PostgreSQL
    driver-class-name: org.h2.Driver
    username: sa
    password:

logging:
  level:
    com.example.ordermanagement: DEBUG
    org.hibernate.SQL: DEBUG
```

`MODE=PostgreSQL` is H2's attempt to emulate PostgreSQL syntax — it helps for basic cases but doesn't cover everything. It's useful for `@DataJpaTest` tests that test pure JPQL queries; for anything PostgreSQL-specific, use Testcontainers.

> **Interview Question — SDE-2:** "Why would you use Testcontainers instead of H2 for integration tests, and what's the cost?"
>
> **Answer:** The core reason is fidelity: H2 is a different database with a different SQL dialect, different constraint semantics, and missing features. Tests that pass on H2 can fail on PostgreSQL for reasons that are genuinely hard to trace — a unique constraint violation that H2 silently ignores but PostgreSQL enforces, a query that uses PostgreSQL syntax H2 doesn't recognize, a `RETURNING` clause or `ON CONFLICT` that H2 simply doesn't support. Testcontainers runs the actual PostgreSQL binary in Docker, so the tests run against the exact same database engine as production. The cost is startup time — a PostgreSQL container takes 2–5 seconds to start vs. milliseconds for H2, and Docker must be installed and running on every developer machine and in CI. Those costs are real but bounded: the container is started once per test class, and CI environments with Docker support are standard. The pragmatic approach most teams reach is: use H2 for fast unit-level repository tests of simple JPQL, use Testcontainers for any test that touches PostgreSQL-specific SQL, complex constraints, or end-to-end order flows.

---

The application is tested. Chapter 7 documents it and makes it production-ready — adding Swagger UI, Actuator health endpoints, profiles for different environments, and a graceful shutdown that doesn't drop in-flight requests.
