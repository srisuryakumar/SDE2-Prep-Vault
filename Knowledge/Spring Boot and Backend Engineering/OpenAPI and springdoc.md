---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 7 — Documentation & Production"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [spring, documentation, openapi]
---

# OpenAPI and springdoc

## Intuition
OpenAPI (formerly Swagger) is a specification for describing REST APIs in JSON/YAML. 
`springdoc-openapi` automatically reads your Spring Boot annotations (`@RestController`, `@GetMapping`, DTO constraints) and generates this spec at `/v3/api-docs`. 
It also serves an interactive Swagger UI at `/swagger-ui.html`.

## Key Annotations
While basic documentation is auto-generated, you can add OpenAPI annotations for a polished, public-facing API:
- `@Tag(name = "Orders", description = "...")`: Groups endpoints in the UI.
- `@Operation(summary = "...", description = "...")`: Describes a specific controller method.
- `@ApiResponse(responseCode = "200", description = "...")`: Documents the possible HTTP status codes.
- `@Schema(description = "...", example = "...")`: Documents fields on a DTO (request/response bodies).
