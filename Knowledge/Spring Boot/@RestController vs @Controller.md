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

# @RestController vs @Controller

## Intuition
`@RestController` is a meta-annotation that combines two things:
1. **`@Controller`**: Marks the class as a Spring MVC controller, routing HTTP requests to its methods.
2. **`@ResponseBody`**: Tells Spring to serialize the return value of every method directly into the HTTP response body (usually as JSON using Jackson), rather than interpreting the return value as a view name (like an HTML template).

Use `@RestController` for REST APIs. Use `@Controller` for applications that render server-side HTML templates.
