---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 3 — Redis"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [redis, distributed-lock, concurrency]
---

# Cache Stampede and Distributed Locks

## Cache Stampede (Thundering Herd)
A popular cache key expires at $T=0$. Immediately, 10,000 concurrent requests all get a cache MISS simultaneously. All 10,000 query the database at the exact same time, overwhelming the database and causing a cascade failure.

**Solution:** Use a **Mutex Lock**. Only ONE request acquires the lock to rebuild the cache from the database. The other 9,999 requests fail to acquire the lock and recursively sleep/retry until the cache is populated.

## Distributed Locks in Redis
**Acquiring a Lock:**
Use `SET NX EX` (Atomic check-and-set with expiry).
```bash
SET payment:lock:order:123 "worker-uuid-abc" NX EX 30
```
- `NX`: Only set if it does not exist.
- `EX`: Auto-expire (prevents deadlocks if the worker crashes).

**Releasing a Lock:**
We MUST use a **Lua Script** to release the lock atomically.
```lua
local owner = redis.call("GET", KEYS[1])
if owner == ARGV[1] then
    return redis.call("DEL", KEYS[1])   -- It's still our lock, release it
else
    return 0   -- Lock expired or acquired by another worker, do nothing
end
```
**Why Lua?** If we used a separate `GET` and `DEL` command, another worker could acquire the lock between our `GET` and `DEL` (if our lock expired naturally in that split second). Our `DEL` would then accidentally delete the new worker's lock! Lua scripts execute atomically in Redis, making `GET + DEL` an indivisible unit.
