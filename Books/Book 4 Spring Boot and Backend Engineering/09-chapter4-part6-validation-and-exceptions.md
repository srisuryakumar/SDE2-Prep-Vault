# Chapter 4 (Part 6 of 6): Validation and Global Exception Handling

## 4.26 Bean Validation: `@Valid` and constraint annotations

Bean Validation (the Jakarta standard, implemented by Hibernate Validator, auto-configured by `spring-boot-starter-validation`) provides declarative, annotation-based validation on any object's fields. The annotations live on the field; the enforcement happens when you annotate a controller parameter with `@Valid`.

The complete set of annotations used in this project, with precise semantics:

| Annotation | Checks |
|---|---|
| `@NotNull` | Field is not `null` — passes for empty strings and empty collections |
| `@NotEmpty` | Field is not `null` **and** not empty (empty string `""`, empty collection `[]`) |
| `@NotBlank` | Field is not `null`, not empty, and not all-whitespace — the right choice for any `String` that must contain meaningful content |
| `@Size(min, max)` | String length or collection size is within the bounds |
| `@Email` | String matches a valid email address format |
| `@Min(value)` | Numeric value is greater than or equal to `value` |
| `@Max(value)` | Numeric value is less than or equal to `value` |
| `@DecimalMin(value)` | Decimal value is greater than or equal to `value` (also works for `BigDecimal`) |
| `@Pattern(regexp)` | String matches the given regular expression |
| `@Positive` | Numeric value is strictly greater than zero |
| `@PositiveOrZero` | Numeric value is zero or greater |
| `@Valid` | Cascades validation into nested objects (a list of nested records, or an embedded object) |

`@Valid` on a controller method's `@RequestBody` parameter triggers validation of the deserialized object *before* the method body runs. If validation fails, Spring throws `MethodArgumentNotValidException` immediately, with a list of every constraint violation, and never calls your method at all.

`@Valid` on a field inside a DTO (like `@Valid List<OrderItemRequest> items`) cascades validation into each element of that list — Bean Validation won't recurse into nested objects automatically unless you tell it to.

**Adding validation to `CreateOrderRequest.OrderItemRequest`:**

```java
package com.example.ordermanagement.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.util.List;

public record CreateOrderRequest(
        @NotEmpty(message = "Order must contain at least one item")
        @Size(max = 50, message = "Order cannot exceed 50 items")
        @Valid
        List<OrderItemRequest> items
) {
    public record OrderItemRequest(
            @NotNull(message = "Product ID is required")
            Long productId,

            @NotNull(message = "Quantity is required")
            @Min(value = 1, message = "Quantity must be at least 1")
            Integer quantity
    ) {}
}
```

## 4.27 Custom constraint annotations

The built-in annotations cover the common cases. When you need a validation that doesn't fit any standard annotation — for example, validating that a `String` value is a valid member of a known enum — write your own:

```java
package com.example.ordermanagement.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Documented
@Constraint(validatedBy = ValidOrderStatusValidator.class)
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidOrderStatus {
    String message() default "Invalid order status";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

```java
package com.example.ordermanagement.validation;

import com.example.ordermanagement.entity.OrderStatus;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class ValidOrderStatusValidator
        implements ConstraintValidator<ValidOrderStatus, String> {

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) return true; // @NotNull handles the null case separately
        try {
            OrderStatus.valueOf(value.toUpperCase());
            return true;
        } catch (IllegalArgumentException e) {
            return false;
        }
    }
}
```

Usage:

```java
public record UpdateStatusRequest(
        @NotBlank
        @ValidOrderStatus
        String status
) {}
```

The pattern: a meta-annotation (`@Constraint(validatedBy = ...)`) links the annotation to its validator class; the validator implements `ConstraintValidator<AnnotationType, FieldType>` and provides the actual boolean logic. Bean Validation calls your `isValid()` at the appropriate moment — you never call it yourself.

## 4.28 The error response shape

Every error from the API, regardless of the cause, uses this exact JSON shape:

```json
{
  "timestamp": "2026-06-18T09:15:30.123456Z",
  "status": 422,
  "error": "Unprocessable Entity",
  "message": "Validation failed for 2 field(s)",
  "path": "/v1/orders",
  "validationErrors": {
    "items[0].quantity": "Quantity must be at least 1",
    "items": "Order must contain at least one item"
  }
}
```

The `validationErrors` field is only present for validation failures — other errors use the same envelope without it.

```java
package com.example.ordermanagement.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.Instant;
import java.util.Map;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record ErrorResponse(
        Instant timestamp,
        int status,
        String error,
        String message,
        String path,
        Map<String, String> validationErrors
) {
    /** Convenience factory for simple errors without field-level details. */
    public static ErrorResponse of(int status, String error, String message, String path) {
        return new ErrorResponse(Instant.now(), status, error, message, path, null);
    }

    /** Factory for validation errors, with per-field details. */
    public static ErrorResponse validationError(String message, String path,
                                                 Map<String, String> errors) {
        return new ErrorResponse(Instant.now(), 422, "Unprocessable Entity", message, path, errors);
    }
}
```

`@JsonInclude(JsonInclude.Include.NON_NULL)` tells Jackson to omit any field from the JSON output if its value is `null`. Without it, every simple error response would include `"validationErrors": null` — unnecessary noise. With it, `validationErrors` only appears when it has actual content.

## 4.29 `@RestControllerAdvice`: the global exception handler

`@RestControllerAdvice` = `@ControllerAdvice` (apply to every controller) + `@ResponseBody` (serialize return values as JSON). One class, one `@ExceptionHandler` method per exception type, and every controller in the application benefits from consistent error handling without any boilerplate in the controllers themselves.

The `HttpServletRequest` parameter (available in any `@ExceptionHandler` method) gives us the request path for the error envelope.

```java
package com.example.ordermanagement.exception;

import com.example.ordermanagement.dto.response.ErrorResponse;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.orm.ObjectOptimisticLockingFailureException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

import java.util.LinkedHashMap;
import java.util.Map;

@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    // ── 404 Not Found ────────────────────────────────────────────────────────

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(
            ResourceNotFoundException ex, HttpServletRequest request) {

        log.debug("Resource not found: {}", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(ErrorResponse.of(404, "Not Found", ex.getMessage(),
                        request.getRequestURI()));
    }

    // ── 409 Conflict ─────────────────────────────────────────────────────────

    @ExceptionHandler(DuplicateResourceException.class)
    public ResponseEntity<ErrorResponse> handleConflict(
            DuplicateResourceException ex, HttpServletRequest request) {

        log.debug("Conflict: {}", ex.getMessage());
        return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(ErrorResponse.of(409, "Conflict", ex.getMessage(),
                        request.getRequestURI()));
    }

    @ExceptionHandler(ObjectOptimisticLockingFailureException.class)
    public ResponseEntity<ErrorResponse> handleOptimisticLock(
            ObjectOptimisticLockingFailureException ex, HttpServletRequest request) {

        log.warn("Optimistic lock conflict on {}", ex.getPersistentClassName());
        return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(ErrorResponse.of(409, "Conflict",
                        "This resource was modified concurrently. Please retry your request.",
                        request.getRequestURI()));
    }

    @ExceptionHandler(InvalidOrderStateException.class)
    public ResponseEntity<ErrorResponse> handleInvalidState(
            InvalidOrderStateException ex, HttpServletRequest request) {

        return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(ErrorResponse.of(409, "Conflict", ex.getMessage(),
                        request.getRequestURI()));
    }

    // ── 422 Unprocessable Entity ──────────────────────────────────────────────

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            MethodArgumentNotValidException ex, HttpServletRequest request) {

        Map<String, String> fieldErrors = new LinkedHashMap<>();
        ex.getBindingResult().getFieldErrors()
                .forEach(fe -> fieldErrors.put(fe.getField(), fe.getDefaultMessage()));
        ex.getBindingResult().getGlobalErrors()
                .forEach(ge -> fieldErrors.put(ge.getObjectName(), ge.getDefaultMessage()));

        String message = "Validation failed for " + fieldErrors.size() + " field(s)";
        log.debug("Validation failed: {}", fieldErrors);

        return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
                .body(ErrorResponse.validationError(message, request.getRequestURI(), fieldErrors));
    }

    @ExceptionHandler(InsufficientStockException.class)
    public ResponseEntity<ErrorResponse> handleInsufficientStock(
            InsufficientStockException ex, HttpServletRequest request) {

        return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
                .body(ErrorResponse.of(422, "Unprocessable Entity", ex.getMessage(),
                        request.getRequestURI()));
    }

    // ── 400 Bad Request ───────────────────────────────────────────────────────

    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public ResponseEntity<ErrorResponse> handleTypeMismatch(
            MethodArgumentTypeMismatchException ex, HttpServletRequest request) {

        String message = "Parameter '" + ex.getName() + "' should be of type "
                + (ex.getRequiredType() != null ? ex.getRequiredType().getSimpleName() : "unknown");
        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ErrorResponse.of(400, "Bad Request", message, request.getRequestURI()));
    }

    // ── 500 Internal Server Error ─────────────────────────────────────────────

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpected(
            Exception ex, HttpServletRequest request) {

        // Log the full stack trace internally — NEVER expose it in the response.
        log.error("Unexpected error on {} {}: {}",
                request.getMethod(), request.getRequestURI(), ex.getMessage(), ex);

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(ErrorResponse.of(500, "Internal Server Error",
                        "An unexpected error occurred. Please contact support.",
                        request.getRequestURI()));
    }
}
```

The `Exception.class` catch-all at the bottom is essential: it's the safety net for any exception that doesn't match a more specific handler. Without it, Spring Boot falls through to its own default error handling, which — depending on version and configuration — can expose stack traces or implementation details in the response. The generic message ("An unexpected error occurred") is intentional: telling an external client exactly what internal exception was thrown is an information-disclosure risk. Log the full exception internally where you can see it, and give the client just enough to open a support ticket.

> **Interview Question — SDE-2:** "How does `@RestControllerAdvice` work mechanically — how does Spring know which handler method to call for a given exception?"
>
> **Answer:** `@RestControllerAdvice` registers the annotated class with Spring's `ExceptionHandlerExceptionResolver`. When a controller method throws an uncaught exception, the `DispatcherServlet`'s exception-handling chain eventually reaches this resolver, which scans all registered advice classes for `@ExceptionHandler` methods whose parameter type is assignable from the thrown exception. It picks the most-specific matching type — an exact match wins over a superclass match — which is why a specific `ResourceNotFoundException` handler fires in preference to the catch-all `Exception` handler, even though the exception is technically an `Exception` too. If multiple advice classes have handlers for the same exception type, ordering is determined by `@Order` or `Ordered` implementation. The resolver then calls the matched handler method, and its return value is serialized and written to the response, exactly as if it were a controller method's return value.

---

## The complete `application.yml` as of Chapter 4 (accumulated)

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
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 30000
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        default_batch_fetch_size: 25
    open-in-view: false

ordermanagement:
  name: "Order Management API"
  support-email: "support@ordermanagement.com"
  max-items-per-order: 50

logging:
  level:
    com.example.ordermanagement: DEBUG
    org.hibernate.SQL: DEBUG
    org.hibernate.orm.jdbc.bind: TRACE
```

`default_batch_fetch_size: 25` is a global `@BatchSize` equivalent — any lazy association that doesn't have its own explicit `@BatchSize` annotation uses this value, giving us the batching benefit across the whole application without annotating every single collection. Think of it as a sensible project-wide default, overridable per-collection with an explicit annotation.

HikariCP settings (`maximum-pool-size: 10`, etc.) are covered in depth in Chapter 12's production-readiness section, but appear here because they're needed now that the application is actually making database calls: HikariCP is Spring Boot's default connection pool, auto-configured by `spring-boot-starter-data-jpa`, and its default pool size of 10 is appropriate for development but something you'll tune based on measured concurrency in production.

The API is now functionally complete — it can create orders, fetch them, cancel them, and handle all error cases consistently. Chapter 5 secures every endpoint that should require authentication.
