---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [spring, validation]
---

# Custom Constraint Annotations

## Intuition
When built-in annotations (`@NotBlank`, `@Min`, etc.) aren't enough (e.g. validating that a String is a valid enum value), you write a custom constraint.

## The Pattern
It requires two pieces:
1. **The Annotation:** A custom annotation meta-annotated with `@Constraint(validatedBy = MyCustomValidator.class)`.
2. **The Validator:** A class implementing `ConstraintValidator<MyAnnotation, TargetType>` with the boolean `isValid()` logic.

Spring calls your `isValid()` method automatically when validating the DTO.
