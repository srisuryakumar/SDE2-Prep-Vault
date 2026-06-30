---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 2 — Database Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, acid, transactions]
---

# ACID Properties

## Intuition
ACID guarantees that concurrent database access produces correct results. Without it, money disappears and inventory goes negative.

## The 4 Properties
- **Atomicity (All or Nothing):** Either all operations in a transaction succeed, or none do. Handled via the Write-Ahead Log (WAL). If the system crashes mid-transaction, PostgreSQL replays the WAL on restart and rolls back uncommitted changes.
- **Consistency (Rules are Never Violated):** The database guarantees that constraints (e.g., `CHECK (balance >= 0)`) are strictly adhered to. If a transaction violates a constraint, it is immediately aborted.
- **Isolation (Concurrent Snapshots):** Concurrent transactions do not interfere with each other. In Read Committed (PostgreSQL default), a query sees a snapshot of the data. Changes from uncommitted transactions are completely invisible.
- **Durability (Committed Data Survives Crashes):** Once a `COMMIT` is acknowledged, the data is safe. PostgreSQL `fsync()`s the WAL to disk before acknowledging the commit. If the machine loses power one millisecond later, the WAL is replayed on restart.
