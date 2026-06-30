---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, mvc, rest]
---

# ResponseEntity (Controlling HTTP Responses)

## Intuition
Returning a plain DTO from a controller implicitly produces a `200 OK` response. When you need explicit control over the HTTP status code or headers, use `ResponseEntity<T>`.

## Common Uses
- **204 No Content:** For a successful DELETE.
  `return ResponseEntity.noContent().build();`
- **409 Conflict:**
  `return ResponseEntity.status(HttpStatus.CONFLICT).body(errorResponse);`

## 201 Created + Location Header
When creating a new resource via `POST`, it is best practice to return `201 Created` with a `Location` header pointing to the new resource's canonical URL.
```java
URI location = ServletUriComponentsBuilder.fromCurrentRequest()
        .path("/{id}")
        .buildAndExpand(createdId)
        .toUri();
return ResponseEntity.created(location).body(createdEntity);
```
**Why?** It tells the client the exact URL of the newly created resource without forcing them to parse the response body or guess how IDs are structured.
