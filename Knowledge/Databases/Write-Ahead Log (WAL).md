---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 2 — Database Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, internals, wal, durability]
---

# Write-Ahead Log (WAL)

## Intuition
The **WAL (Write-Ahead Log)** is PostgreSQL's mechanism for both **Atomicity** and **Durability**. It is a sequential, append-only file on disk. 

Because random I/O (modifying a specific data page) is slow and risky (what if a crash happens halfway through?), PostgreSQL writes the *description* of the change sequentially to the WAL first. Sequential writes are very fast.

## The Commit Sequence
1. Application sends `UPDATE`.
2. PostgreSQL appends WAL record: `"orders id=1: PENDING -> SHIPPED"`.
3. PostgreSQL applies the change to the in-memory buffer page (it is now "dirty").
4. PostgreSQL `fsync()`s the WAL file to disk.
5. PostgreSQL returns `COMMIT SUCCESS` to the application.
6. [Asynchronously, later]: The modified buffer pages are flushed to actual data files on disk (checkpointing).

## Crash Recovery
If the server crashes at any point, on restart it reads the WAL from the last checkpoint. It redoes all committed transactions whose data pages weren't flushed, and undoes all uncommitted transactions. The database is restored to a consistent state.
