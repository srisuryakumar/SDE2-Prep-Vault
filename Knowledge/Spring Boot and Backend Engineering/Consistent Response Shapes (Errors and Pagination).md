---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 2 — REST API Design Principles"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [rest, api-design, error-handling, pagination]
---

# Consistent Response Shapes (Errors and Pagination)

## Intuition
Every endpoint in an API should look like it was designed by the same person. This applies heavily to Error Responses and Pagination Metadata.

## Consistent Error Format
Every error response should have the exact same shape, so clients can write *one* error-handling code path.
```json
{
  "timestamp": "2026-06-18T09:15:30Z",
  "status": 404,
  "error": "Not Found",
  "message": "Order with id 9001 not found",
  "path": "/v1/orders/9001"
}
```
In Spring, this is achieved with a single global `@RestControllerAdvice` applied to all controllers.

## Pagination Metadata
A list endpoint must tell the client where they are in the collection, not just the rows.
```json
{
  "content": [ { "id": 1 }, { "id": 2 } ],
  "page": 0,
  "size": 20,
  "totalElements": 487,
  "totalPages": 25,
  "last": false
}
```
This is what Spring Data's `Page<T>` serializes to by default.
