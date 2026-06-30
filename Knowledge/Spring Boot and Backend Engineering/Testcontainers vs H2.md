---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 6 — Testing"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [testing, database, docker, testcontainers]
---

# Testcontainers vs H2

## Intuition
H2 is a fast, in-memory database often used for testing (`@DataJpaTest`). But H2 is not PostgreSQL/MySQL. It has a different SQL dialect, different constraint enforcement, and misses specific features (`ON CONFLICT`, `FOR UPDATE SKIP LOCKED`).
Tests that pass on H2 can fail in production against a real database.

## Testcontainers
Testcontainers solves this fidelity problem by spinning up a **real database container** (via Docker) for the test run.

```java
@Testcontainers
class MyIntegrationTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        // Bridges the randomly assigned Docker port to Spring's properties
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

## The Trade-off
Testcontainers is much slower to start (2–5 seconds vs milliseconds for H2) and requires Docker to be running on the host machine/CI. 
**Best Practice:** Use H2 for fast unit-level repository tests of simple JPQL. Use Testcontainers for full end-to-end integration tests or when using database-specific SQL features.
