---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 9 — Flyway"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Flyway Core Concepts", "Zero-Downtime Database Migrations"]
tags: [database, spring, hibernate, migrations]
---

# The Problem with ddl-auto update

## Intuition
Setting `spring.jpa.hibernate.ddl-auto: update` is great for tutorials but a trap for production.

## Why it is dangerous in production
1. **Data Loss:** If you rename a field, Hibernate might issue a `DROP COLUMN` for the old name and `ADD COLUMN` for the new one, destroying all data in that column.
2. **Cannot express complex migrations:** It can't handle splitting a column into two, migrating data between tables, or adding partial indexes.
3. **No audit trail:** You have no history of what schema changes were run when.
4. **Race conditions:** Multiple application instances starting simultaneously might all try to run `ALTER TABLE` at once.

## The Solution
Use a migration tool like Flyway and set `ddl-auto: validate` so Hibernate only verifies the schema without attempting to modify it.
