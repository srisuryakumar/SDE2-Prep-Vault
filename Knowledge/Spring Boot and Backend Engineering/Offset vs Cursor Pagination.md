---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 2 — REST API Design Principles"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [rest, pagination, database, performance]
---

# Offset vs Cursor Pagination

## Intuition
There are two fundamentally different strategies for paginating a large collection. This is a common system design interview topic.

## 1. Offset Pagination
`?page=2&size=20` (translates to `LIMIT 20 OFFSET 40`).
- **Pros:** Simple to implement. Clients can jump directly to "page 7". Good for admin dashboards.
- **Cons:** Slow at scale. `OFFSET 10000` forces the DB to scan and discard 10,000 rows before returning the next 20. It also suffers from "page drift" (items skip or duplicate if a new row is inserted concurrently while a client is paging).

## 2. Cursor Pagination
`?after=9001&size=20` (translates to `WHERE id > 9001 ORDER BY id LIMIT 20`).
- **Pros:** Fast at any depth. The DB uses an index to jump straight to `id > 9001` without scanning previous rows. Stable under concurrent writes.
- **Cons:** Client cannot jump to arbitrary pages, only "next" or "previous". Requires a sortable, stable, unique column to cursor on (like an auto-increment ID or high-precision timestamp).

## Interview Scenario
> "Your `/v1/products` endpoint is slow on high page numbers, but fast on early pages. Why, and how do you fix it without changing the DB schema?"

**Answer:** This is a symptom of offset pagination on a large table. The DB index helps with ordering, not skipping. The fix is to switch the pagination strategy to cursor-based. The client sends the last ID they saw, and the query becomes `WHERE id > :lastSeenId ORDER BY id LIMIT 20`. The DB jumps straight there using the existing index.
