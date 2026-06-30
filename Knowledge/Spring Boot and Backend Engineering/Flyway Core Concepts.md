---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 9 — Flyway"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, spring, flyway, migrations]
---

# Flyway Core Concepts

## Intuition
Flyway is a database migration tool that uses versioned, numbered SQL scripts to predictably evolve a database schema.

## How it works at Startup
Before the application accepts requests, Flyway:
1. Obtains a distributed **database-level lock** (e.g., PostgreSQL advisory lock) so multiple instances starting simultaneously don't race.
2. Reads the `flyway_schema_history` table to see which migrations have already run.
3. Scans `classpath:db/migration` for new `V*__*.sql` files.
4. Executes pending migrations in version order.
5. Records their success in the history table and releases the lock.

## Immutability Rule
Once a migration is committed and applied, you **never edit it**. If you need to undo or fix a change, you write a *new* migration (e.g. `V6__undo_v5.sql`). Flyway verifies checksums of previously run scripts and will fail to start if an old script was modified.
