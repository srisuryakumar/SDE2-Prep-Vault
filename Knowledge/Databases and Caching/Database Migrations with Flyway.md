---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 4 — Database Migrations with Flyway"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [database, migration, flyway, ci-cd]
---

# Database Migrations with Flyway

## Intuition
Without migrations, a database schema drifts. "It works on my machine" becomes a database problem. Flyway solves this by ensuring every environment runs the exact same versioned SQL scripts in the same order.
- The schema lives in Git, reviewed in PRs.
- Flyway tracks applied scripts in the `flyway_schema_history` table.
- Running migrations is idempotent.

## Migration File Naming Convention
```
src/main/resources/db/migration/
  V1__init_schema.sql             <-- V{version}__{description}.sql
  V2__add_product_sku.sql         (two underscores between version and name)
  R__update_view.sql              <-- R__{name}.sql (repeatable, re-runs on change)
```

## Spring Boot Integration
Add the `flyway-core` dependency and configure `application.yml`:
```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
  jpa:
    hibernate:
      ddl-auto: validate   # Flyway owns the schema; Hibernate ONLY validates
```
