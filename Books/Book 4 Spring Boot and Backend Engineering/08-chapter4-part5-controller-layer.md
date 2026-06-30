# Chapter 4 (Part 5 of 6): The Controller Layer

## 4.22 `@RestController` = `@Controller` + `@ResponseBody`

`@RestController` is another meta-annotation convenience, combining two things:

**`@Controller`** marks the class as a Spring MVC controller, meaning Spring's `DispatcherServlet` will route HTTP requests to methods in this class based on the `@RequestMapping` annotations on them.

**`@ResponseBody`** on the class level means: for every handler method in this class, serialize the return value directly into the HTTP response body, using whatever `HttpMessageConverter` matches the request's `Accept` header. Without `@ResponseBody`, Spring MVC interprets the return value as a *view name* — a string like `"orderDetail"` that it would try to resolve against a template engine. With `@ResponseBody`, the return value is the response content itself. For a `@Bean` of type `OrderResponse`, Jackson (the JSON library Spring Boot auto-configures) serializes it as `application/json`.

`@RestController` is the right annotation for every controller in a pure REST API. `@Controller` (without `@ResponseBody`) belongs in applications that render server-side HTML templates — not what we're building.

## 4.23 Request mapping anatomy

`@RequestMapping` at the class level establishes a URL prefix for all methods in the class. The method-level annotations (`@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping`) are shorthand forms of `@RequestMapping(method = RequestMethod.GET/POST/...)` — they exist purely for readability, not for any additional functionality.

```java
@RestController
@RequestMapping("/v1/orders")   // Every method in this class is under /v1/orders
public class OrderController {

    @GetMapping("/{id}")        // GET /v1/orders/{id}
    @PostMapping                // POST /v1/orders
    @PatchMapping("/{id}/cancel") // PATCH /v1/orders/{id}/cancel
}
```

The four parameter annotations used to extract data from a request:

**`@PathVariable`** — binds a segment of the URL path. `@GetMapping("/{id}")` with `@PathVariable Long id` binds `id` from whatever value appears in that segment of the actual URL. The variable name in the path template must match the parameter name (or use `@PathVariable("id")` to be explicit).

**`@RequestParam`** — binds a URL query parameter. `@RequestParam(defaultValue = "0") int page` binds `?page=2` from the URL, with 0 as the default if the parameter is absent. Can also be used to bind form fields. `required = false` makes the parameter optional; `defaultValue` implies `required = false`.

**`@RequestBody`** — deserializes the request body into a Java object. Spring Boot has Jackson on the classpath by default, so `@RequestBody CreateOrderRequest request` parses the incoming JSON into a `CreateOrderRequest` record. If the JSON is malformed (unparseable), Spring returns a `400 Bad Request` before your method is even called. Adding `@Valid` alongside it triggers Bean Validation on the deserialized object (Chapter 4 Part 6 covers this).

**`@RequestHeader`** — binds a specific HTTP header value to a parameter. `@RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey` reads the `Idempotency-Key` header, optionally.

## 4.24 `ResponseEntity`: full control

Returning a plain object from a handler method (`OrderResponse`) is a shortcut that produces a `200 OK` response with a serialized body. When you need to control the status code, or add headers, `ResponseEntity<T>` is the explicit form:

```java
// Equivalent to returning an OrderResponse directly — implicit 200 OK
return ResponseEntity.ok(response);

// 201 Created with a Location header
return ResponseEntity.created(URI.create("/v1/orders/" + orderId))
                     .body(response);

// 202 Accepted — async operation queued
return ResponseEntity.accepted().body(new AsyncOperationResponse(trackingId));

// 204 No Content — e.g., a successful DELETE
return ResponseEntity.noContent().build();

// 409 Conflict — explicit status code
return ResponseEntity.status(HttpStatus.CONFLICT).body(errorResponse);
```

The `201 Created` + `Location` header pattern is worth always using for any POST that creates a new resource. It's not just good practice — it's the HTTP specification's intended model for how a client discovers the canonical URL of a resource it just created, without having to parse the response body.

## 4.25 Complete controllers

**`ProductController`:**

```java
package com.example.ordermanagement.controller;

import com.example.ordermanagement.dto.request.CreateProductRequest;
import com.example.ordermanagement.dto.response.ProductResponse;
import com.example.ordermanagement.service.ProductService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;

@RestController
@RequestMapping("/v1/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;

    @GetMapping
    public ResponseEntity<Page<ProductResponse>> listProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "") String nameFilter) {

        PageRequest pageable = PageRequest.of(page, size, Sort.by("name"));
        return ResponseEntity.ok(productService.listProducts(nameFilter, pageable));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProductResponse> getProduct(@PathVariable Long id) {
        return ResponseEntity.ok(productService.getProductById(id));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ProductResponse> createProduct(
            @Valid @RequestBody CreateProductRequest request) {

        ProductResponse created = productService.createProduct(request);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(created.id())
                .toUri();
        return ResponseEntity.created(location).body(created);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ProductResponse> updateProduct(
            @PathVariable Long id,
            @Valid @RequestBody CreateProductRequest request) {

        return ResponseEntity.ok(productService.updateProduct(id, request));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
        return ResponseEntity.noContent().build();
    }
}
```

**`OrderController`:**

```java
package com.example.ordermanagement.controller;

import com.example.ordermanagement.dto.request.CreateOrderRequest;
import com.example.ordermanagement.dto.response.OrderResponse;
import com.example.ordermanagement.entity.User;
import com.example.ordermanagement.service.IdempotencyService;
import com.example.ordermanagement.service.OrderService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;

@RestController
@RequestMapping("/v1")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;
    private final IdempotencyService idempotencyService;

    // GET /v1/users/{userId}/orders
    @GetMapping("/users/{userId}/orders")
    public ResponseEntity<Page<OrderResponse>> getUserOrders(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @AuthenticationPrincipal User currentUser) {

        PageRequest pageable = PageRequest.of(page, size,
                Sort.by(Sort.Direction.DESC, "createdAt"));
        return ResponseEntity.ok(orderService.getOrdersForUser(userId, pageable));
    }

    // GET /v1/orders/{id}
    @GetMapping("/orders/{id}")
    public ResponseEntity<OrderResponse> getOrder(@PathVariable Long id) {
        return ResponseEntity.ok(orderService.getOrderById(id));
    }

    // POST /v1/orders
    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> createOrder(
            @Valid @RequestBody CreateOrderRequest request,
            @AuthenticationPrincipal User currentUser,
            @RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey) {

        // Idempotency check — return cached result if this key was seen before
        if (idempotencyKey != null) {
            var existing = idempotencyService.findExistingRecord(idempotencyKey);
            if (existing.isPresent()) {
                // In a production implementation, deserialize the stored JSON back
                // to OrderResponse and return it with the original status code.
                // Simplified here to show the pattern clearly.
                return ResponseEntity.status(existing.get().getHttpStatus()).build();
            }
        }

        OrderResponse response = orderService.createOrder(currentUser.getId(), request);

        if (idempotencyKey != null) {
            idempotencyService.saveRecord(idempotencyKey, response, 201);
        }

        URI location = ServletUriComponentsBuilder
                .fromCurrentContextPath()
                .path("/v1/orders/{id}")
                .buildAndExpand(response.id())
                .toUri();

        return ResponseEntity.created(location).body(response);
    }

    // PATCH /v1/orders/{id}/cancel
    @PatchMapping("/orders/{id}/cancel")
    public ResponseEntity<OrderResponse> cancelOrder(
            @PathVariable Long id,
            @AuthenticationPrincipal User currentUser) {

        return ResponseEntity.ok(orderService.cancelOrder(id, currentUser.getId()));
    }
}
```

**`@AuthenticationPrincipal`** — injects the currently-authenticated user object directly into a controller method parameter. This is populated by Spring Security from the `SecurityContext`, which Chapter 5's `JwtAuthenticationFilter` fills in after validating the JWT. The object type (`User` — our own entity class, which will implement `UserDetails`) is determined by what the `JwtAuthenticationFilter` puts into the `SecurityContext`; casting to our own `User` entity lets us call `currentUser.getId()` without an extra database lookup.

**`ServletUriComponentsBuilder.fromCurrentRequest()`** vs. **`fromCurrentContextPath()`** — a subtle distinction: `fromCurrentRequest()` builds the URL based on the *current request's URL* (useful in `ProductController.createProduct` — `POST /v1/products` becomes `/v1/products/{id}`). `fromCurrentContextPath()` builds from just the scheme+host+context path, letting you specify the full resource path explicitly — useful in `OrderController.createOrder` where the POST is to `/v1/orders` but the created resource's canonical URL is also `/v1/orders/{id}`.

**`ProductService`** — the remaining service to complete the layer:

```java
package com.example.ordermanagement.service;

import com.example.ordermanagement.dto.request.CreateProductRequest;
import com.example.ordermanagement.dto.response.ProductResponse;
import com.example.ordermanagement.entity.Inventory;
import com.example.ordermanagement.entity.Product;
import com.example.ordermanagement.exception.DuplicateResourceException;
import com.example.ordermanagement.exception.ResourceNotFoundException;
import com.example.ordermanagement.repository.InventoryRepository;
import com.example.ordermanagement.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final InventoryRepository inventoryRepository;

    @Transactional(readOnly = true)
    public Page<ProductResponse> listProducts(String nameFilter, Pageable pageable) {
        if (nameFilter == null || nameFilter.isBlank()) {
            return productRepository.findAll(pageable).map(ProductResponse::from);
        }
        return productRepository.findByNameContainingIgnoreCase(nameFilter, pageable)
                .map(ProductResponse::from);
    }

    @Transactional(readOnly = true)
    public ProductResponse getProductById(Long id) {
        return productRepository.findById(id)
                .map(ProductResponse::from)
                .orElseThrow(() -> new ResourceNotFoundException("Product", id));
    }

    @Transactional
    public ProductResponse createProduct(CreateProductRequest request) {
        if (productRepository.existsBySku(request.sku())) {
            throw new DuplicateResourceException(
                    "Product with SKU '" + request.sku() + "' already exists");
        }
        Product product = new Product(
                request.sku(), request.name(), request.description(), request.price());
        Product saved = productRepository.save(product);

        Inventory inventory = new Inventory(saved, request.initialStock());
        inventoryRepository.save(inventory);

        return ProductResponse.from(saved);
    }

    @Transactional
    public ProductResponse updateProduct(Long id, CreateProductRequest request) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product", id));
        product.setName(request.name());
        product.setDescription(request.description());
        product.setPrice(request.price());
        // No explicit save() — dirty checking persists the changes at commit
        return ProductResponse.from(product);
    }

    @Transactional
    public void deleteProduct(Long id) {
        if (!productRepository.existsById(id)) {
            throw new ResourceNotFoundException("Product", id);
        }
        productRepository.deleteById(id);
    }
}
```

**`ProductResponse` and `CreateProductRequest` DTOs:**

```java
package com.example.ordermanagement.dto.response;

import com.example.ordermanagement.entity.Product;

import java.math.BigDecimal;
import java.time.Instant;

public record ProductResponse(
        Long id,
        String sku,
        String name,
        String description,
        BigDecimal price,
        Instant createdAt
) {
    public static ProductResponse from(Product product) {
        return new ProductResponse(
                product.getId(),
                product.getSku(),
                product.getName(),
                product.getDescription(),
                product.getPrice(),
                product.getCreatedAt()
        );
    }
}
```

```java
package com.example.ordermanagement.dto.request;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;

public record CreateProductRequest(
        @NotBlank(message = "SKU is required")
        @Size(max = 50, message = "SKU cannot exceed 50 characters")
        String sku,

        @NotBlank(message = "Product name is required")
        @Size(max = 200, message = "Product name cannot exceed 200 characters")
        String name,

        @Size(max = 2000, message = "Description cannot exceed 2000 characters")
        String description,

        @NotNull(message = "Price is required")
        @DecimalMin(value = "0.01", message = "Price must be greater than zero")
        BigDecimal price,

        @NotNull(message = "Initial stock is required")
        @Min(value = 0, message = "Initial stock cannot be negative")
        Integer initialStock
) {}
```

> **Interview Question — SDE-2:** "Why does `POST /v1/orders` return `201 Created` with a `Location` header, and what does the client do with that header?"
>
> **Answer:** `201 Created` signals that the request succeeded and a new resource was created — it's more informative than a generic `200 OK`, which is used for "request succeeded" generically including updates and reads. The `Location` header tells the client the canonical URL of the new resource — `/v1/orders/9001` in this case. This matters practically in two scenarios: if the client wants to immediately fetch the full order (perhaps to show a confirmation page), it can `GET` the `Location` URL directly rather than parsing the response body to extract the ID and constructing the URL itself; and if the creation response body was minimal or empty (some APIs return `201` with no body at all), `Location` gives the client a way to retrieve the resource without out-of-band knowledge of how order IDs are structured.

---

The controller layer handles the HTTP-to-Java translation. The last part of Chapter 4 adds the two most important cross-cutting concerns that apply across every endpoint: request validation and global exception handling.
