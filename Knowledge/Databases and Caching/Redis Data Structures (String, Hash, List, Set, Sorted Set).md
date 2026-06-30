---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 3 — Redis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [redis, data-structures, cache]
---

# Redis Data Structures (String, Hash, List, Set, Sorted Set)

## Intuition
Redis stores data in RAM and serves requests in 0.1–1ms (10-100x faster than disk-based databases). It provides 5 core data structures.

## 1. STRING — The Universal Type
One key maps to one value (up to 512MB). Numbers stored as strings support atomic increments.
- **Commands:** `SET`, `GET`, `SETEX`, `TTL`, `INCR`, `INCRBY`
- **NX Flag:** `SET lock:123 "worker" NX EX 30` (Atomic check-and-set).
- **Use cases:** Session tokens, API rate limit counters, distributed locks, simple caching.

## 2. HASH — Object Storage
Maps string fields to string values under one key. Useful for partial updates without deserializing an entire object.
- **Commands:** `HSET`, `HGET`, `HMGET`, `HGETALL`, `HDEL`
- **Use cases:** User profiles, product metadata, shopping carts.

## 3. LIST — Ordered Sequences
A doubly-linked list ($O(1)$ push/pop at ends, $O(n)$ random access). Functions as a queue (`RPUSH` + `LPOP`) or stack (`LPUSH` + `LPOP`).
- **Commands:** `RPUSH`, `LPUSH`, `LRANGE`, `LPOP`, `BLPOP` (Blocking pop).
- **Bounded list:** `LTRIM` keeps only the most recent N items.
- **Use cases:** Activity feeds, job queues, chat message history.

## 4. SET — Unique Collections
An unordered collection that guarantees uniqueness. `SISMEMBER` is $O(1)$. Supports union, intersection, and difference.
- **Commands:** `SADD`, `SISMEMBER`, `SMEMBERS`, `SINTERSTORE`, `SUNIONSTORE`, `SDIFF`
- **Use cases:** Product tags, unique visitors per day, mutual friends.

## 5. SORTED SET — Ranked Collections
Stores unique members, each with a floating-point score. Ordered by score. Updates are $O(\log n)$.
- **Commands:** `ZADD`, `ZRANGE`, `ZREVRANGE`, `ZRANK`, `ZINCRBY`, `ZPOPMIN`
- **Use cases:** Leaderboards, priority queues, rate limiting (sliding window).
