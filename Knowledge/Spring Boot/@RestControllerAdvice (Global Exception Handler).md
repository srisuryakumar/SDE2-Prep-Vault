---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, exceptions, mvc]
---

# @RestControllerAdvice (Global Exception Handler)

## Intuition
`@RestControllerAdvice` combines `@ControllerAdvice` (applies to every controller) with `@ResponseBody` (serializes return values directly to JSON). It allows you to handle exceptions globally in one place without cluttering your controllers with `try/catch` blocks.

## Mechanics
You define methods annotated with `@ExceptionHandler(SomeException.class)`.
When a controller throws an exception, Spring's `ExceptionHandlerExceptionResolver` scans your advice classes for a matching exception type. It picks the most specific match (an exact match wins over a superclass). 
The matched method's return value (e.g. a `ResponseEntity<ErrorResponse>`) is serialized as the HTTP response.

## Security Best Practice
**Always include a catch-all `Exception.class` handler at the bottom.**
If you don't, unhandled exceptions fall through to Spring Boot's default error handling, which might expose stack traces or implementation details in the response. Your catch-all handler should log the full stack trace internally, but return a generic 500 "Internal Server Error" message to the client to prevent information disclosure.
