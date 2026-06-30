---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 3 — Redis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [redis, caching, cache-aside, write-through]
---

# Caching Patterns

## Cache-Aside (Lazy Loading)
The most common pattern. The application manages both cache and DB.
- **Read:** App checks cache. On miss, it loads from DB, populates the cache, and returns.
- **Write:** App updates DB, then invalidates (deletes) the cache key.
- **Pros:** Only caches what is requested. DB is a fallback.
- **Cons:** First request hits DB (cold start latency spike).

## Read-Through
The cache layer itself is responsible for loading from DB on a miss. The application only talks to the cache.
- **Pros:** Simpler app code.
- **Cons:** Same cold-start miss as Cache-Aside.

## Write-Through
Every write updates BOTH the cache and the database in the same synchronous operation.
- **Pros:** Zero stale reads after writes. Cache is always current.
- **Cons:** Write latency doubles. May cache data that is never read. Best for frequently read data right after it is written.

## Write-Behind (Write-Back)
App writes to the cache immediately and returns. A background process flushes the dirty data to the DB asynchronously.
- **Pros:** Extremely fast writes. Can batch writes.
- **Cons:** **Risk of data loss** if Redis crashes before flushing. Use only for non-critical data (view counts, analytics).
