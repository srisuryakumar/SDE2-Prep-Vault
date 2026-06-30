---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 6 — Testing"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [testing, spring, integration]
---

# @SpringBootTest (Integration Tests)

## Intuition
`@SpringBootTest` loads the complete `ApplicationContext` — every bean, every configuration, the database connections, and the full web server. 
It is the most faithful test of the real application, but also the slowest and most expensive to run.

## WebEnvironment.RANDOM_PORT
Typically used as `@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)`. This starts the embedded server on a random available port, preventing port conflicts when running multiple test suites in CI.

## TestRestTemplate
When running a full integration test, Spring provides `TestRestTemplate`. It's a test-friendly HTTP client that:
1. Automatically resolves relative URLs to the random port.
2. Does **not** throw exceptions on 4xx/5xx HTTP errors (it returns the `ResponseEntity`, allowing you to assert on the status code).
