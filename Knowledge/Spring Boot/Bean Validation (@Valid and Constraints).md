---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, validation, mvc]
---

# Bean Validation (@Valid and Constraints)

## Intuition
Bean Validation (Hibernate Validator) provides declarative, annotation-based validation on any object's fields.

## The Annotations
- `@NotNull`: Field is not null (passes for empty strings `""`).
- `@NotEmpty`: Field is not null AND not empty (fails on `""` or `[]`).
- `@NotBlank`: Field is not null, not empty, and not all-whitespace. **The right choice for any String that must contain meaningful content.**
- `@Size(min, max)`: String length or collection size.
- `@Min(value)` / `@Max(value)`: Numeric bounds.
- `@Valid`: Cascades validation into nested objects (e.g. a list of nested records).

## How it's Triggered
Place `@Valid` on a controller method's `@RequestBody` parameter.
Spring validates the deserialized object *before* the method body runs. If validation fails, Spring throws a `MethodArgumentNotValidException` immediately, which your global exception handler catches to return a `422 Unprocessable Entity` containing the list of field violations.
