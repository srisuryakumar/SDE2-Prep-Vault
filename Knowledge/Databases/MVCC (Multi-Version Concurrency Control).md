---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 2 — Database Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, internals, mvcc, concurrency]
---

# MVCC (Multi-Version Concurrency Control)

## Intuition
In a naive locking system, every read must acquire a shared lock, and every write must wait for readers to finish. Under high concurrency, this grinds to a halt.
**MVCC's insight:** Keep multiple versions of each row. Readers see the version that existed when their transaction started. Writers create new versions. **Readers never block writers, and writers never block readers.**

## How it works
Each row has hidden headers: `xmin` (transaction ID that created the row) and `xmax` (transaction ID that deleted/updated it).
When a transaction requests a row, PostgreSQL checks the visibility rules based on the transaction's snapshot. 
- If the row was created before the snapshot and not deleted (or deleted after the snapshot), it is visible.
- If a row is deleted or updated, the old version remains on disk until a `VACUUM` process reclaims it.

## VACUUM
Because MVCC keeps old row versions around for concurrent readers, dead row versions accumulate over time. PostgreSQL's background `autovacuum` process periodically scans tables and reclaims dead tuple space. Without it, tables would grow indefinitely.
