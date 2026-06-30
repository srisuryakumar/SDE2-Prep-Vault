---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 6 — Testing"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [testing, architecture]
---

# The Testing Pyramid

## Intuition
The testing pyramid is a heuristic about the mix of test types a well-tested application should have:
1. **Unit Tests (Base):** The majority of tests. Test a single class in isolation, mocking dependencies. Fast, no external dependencies, highly precise.
2. **Integration Tests (Middle):** Fewer, slower. Verify that components work together (e.g. testing a repository against a real database, or a controller's web layer with mocked services).
3. **End-to-End Tests (Top):** The fewest, slowest, most expensive. Exercise the full system from the outside (real HTTP requests, real database, full stack).

## Why it matters
- A suite with only E2E tests is slow, flaky, expensive, and bad at pinpointing the exact line of code that failed.
- A suite with only Unit tests is fast but misses integration bugs (e.g. a SQL query that fails against the real schema, or a misconfigured JSON serializer).
