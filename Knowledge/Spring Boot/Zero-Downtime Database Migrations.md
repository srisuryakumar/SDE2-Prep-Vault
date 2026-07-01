---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 9 — Flyway"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Adding Columns Safely"]
tags: [database, deployment, architecture, migrations]
---

# Zero-Downtime Database Migrations

## Intuition
When deploying to a live system (rolling deployments), there is a window where *old code and new code are running simultaneously against the same database*. Therefore, **schema changes must be backward-compatible with the previous version of the code**.

## Expand and Contract Pattern
For breaking changes (e.g. renaming a column), you must use a three-phase deployment:
1. **Phase 1 (Expand):** Add the new column. Deploy code that reads from the new column if present, but falls back to the old one. Code writes to *both*.
2. **Phase 2 (Migrate Data):** Run a script to backfill data from the old column to the new column for any rows missed during the transition.
3. **Phase 3 (Contract):** Deploy code that only reads/writes the new column. Once deployed, run a script to `DROP` the old column.

If you skip these phases and just rename the column, the old instances currently serving traffic will crash because they are querying a column that no longer exists.
