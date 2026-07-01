---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 5 — Security JWT"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [spring, security, authorization]
---

# Method-Level Security (@PreAuthorize)

## Intuition
Instead of hardcoding role checks inside service or controller methods, Spring Security provides `@PreAuthorize` to evaluate authorization declaratively using SpEL (Spring Expression Language).
Requires `@EnableMethodSecurity` on your configuration class.

## Examples
- **Role Check:** `@PreAuthorize("hasRole('ADMIN')")`. Spring automatically prefixes this with `ROLE_` and matches it against the authorities of the authenticated user in the `SecurityContext`.
- **Complex Checks:** `@PreAuthorize("#userId == authentication.principal.id or hasRole('ADMIN')")`. You can refer to method parameters (`#userId`) and compare them to properties of the currently authenticated principal.
