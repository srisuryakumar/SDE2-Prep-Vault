---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 3 — Redis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [redis, persistence, aof, rdb]
---

# Redis Persistence (RDB and AOF)

## Intuition
By default, Redis stores data in RAM. If it crashes, all data is lost. Persistence allows Redis to be used as a source of truth.

## 1. RDB (Redis Database Dump)
Point-in-time snapshot.
- **How:** Forks the Redis process, serializes the entire dataset to a `.rdb` binary file.
- **When:** Configurable intervals (e.g., save if 10,000 changes in 60 seconds).
- **Pros:** Compact binary file. Very fast restart (just load one file). Good for backups.
- **Cons:** Data since the last snapshot is lost on crash (could be minutes of data loss).

## 2. AOF (Append-Only File)
- **How:** Every write command is appended to an `.aof` file; replayed on restart.
- **When:** Three `fsync` modes:
  - `always`: fsync after every write (safest, slowest).
  - `everysec`: fsync once per second (balanced). At most 1 second of data loss.
  - `no`: OS decides when to fsync (fastest, least safe).
- **Pros:** Minimal data loss (1 second max with `everysec`).
- **Cons:** Larger files. Slower restart (must replay all commands from the beginning).

## Production Recommendation
Enable BOTH:
- **RDB** for fast restarts and point-in-time backups.
- **AOF** with `everysec` for durability (at most 1s data loss).
Redis 7+ supports an RDB-AOF hybrid format combining the best of both.
