---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 7 — Documentation & Production"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [spring, configuration]
---

# Spring Profiles

## Intuition
Spring profiles allow you to maintain different configurations per environment (local, staging, production) without maintaining different codebases or writing if-else checks.

## How it works
You define a base `application.yml` with defaults. Then you define `application-local.yml` and `application-prod.yml` with overrides (e.g. different database URLs, different logging levels).
You activate a profile at startup using a system property or environment variable:
`SPRING_PROFILES_ACTIVE=prod java -jar app.jar`

## Common Overrides
- **Local:** `show-sql: true`, `ddl-auto: update`, Hikari pool size of 10.
- **Production:** `show-sql: false`, `ddl-auto: validate` (never let Hibernate alter schema in prod!), Hikari pool size based on traffic, no stack traces in errors.
