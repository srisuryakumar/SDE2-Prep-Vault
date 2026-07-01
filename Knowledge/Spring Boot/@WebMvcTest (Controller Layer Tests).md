---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 6 — Testing"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [testing, spring, mvc]
---

# @WebMvcTest (Controller Layer Tests)

## Intuition
`@WebMvcTest(MyController.class)` is a Spring Boot slice test. It loads *only* the web layer: the `DispatcherServlet`, Jackson serialization, the filter chain, and `@ControllerAdvice` classes.
It does **not** load the full `ApplicationContext` (no services, no repositories, no database).

## Use Case
It is used for fast integration testing of the HTTP layer. Any services that the controller depends on must be mocked (using `@MockitoBean`).
A test failure here pinpoints a bug in request routing, JSON serialization/deserialization, validation, or HTTP status codes.

*(Note: Because it loads the web layer, it also loads Spring Security filters. You may need to mock your `JwtService` or use `@WithMockUser` to bypass authentication).*
