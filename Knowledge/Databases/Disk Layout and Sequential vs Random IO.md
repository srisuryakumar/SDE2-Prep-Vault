---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 2 — Database Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, internals, io, storage]
---

# Disk Layout and Sequential vs Random I/O

## Intuition
Understanding how data physically lives on disk is critical for database performance tuning. PostgreSQL reads and writes in **pages** of 8KB, never individual rows. Even fetching one row requires reading the entire 8KB page containing it.

## Sequential vs Random I/O
- **Sequential scan:** Reads pages in order from disk. The OS prefetches ahead. Fast on SSD (~500 MB/s).
- **Index scan:** Jumps to specific pages by address. Each jump is a **random read**. Expensive on spinning disk (~5ms per seek).

**Counterintuitive fact:** For a query returning 20%+ of a table's rows, a sequential full-table scan is often **faster** than using an index, because the index generates thousands of random reads versus one continuous sweep of sequential pages. The query planner knows this and chooses accordingly.
