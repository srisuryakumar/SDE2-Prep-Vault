---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, mvc, annotations]
---

# Request Mapping Annotations

## Intuition
Four primary annotations are used to extract data from an incoming HTTP request in a Spring controller:

1. **`@PathVariable`**: Binds a segment of the URL path.
   - Example: `@GetMapping("/{id}")` -> `public void get(@PathVariable Long id)` binds `id` from the URL path.
2. **`@RequestParam`**: Binds a URL query string parameter (or form data).
   - Example: `@RequestParam(defaultValue = "0") int page` binds `?page=2`.
3. **`@RequestBody`**: Deserializes the request body (e.g. JSON) into a Java object using Jackson.
   - Example: `@RequestBody CreateOrderRequest request`. If JSON is malformed, Spring automatically returns `400 Bad Request`.
4. **`@RequestHeader`**: Binds a specific HTTP header value.
   - Example: `@RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey`.
