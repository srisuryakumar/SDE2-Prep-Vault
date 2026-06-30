# High-Level System Design
### From Capacity Estimation to Production Architectures

*A practical, from-scratch guide for backend engineers moving into system design interviews and real-world architecture work.*

---

## Table of Contents

1. The System Design Framework
2. Design Building Blocks
3. Design 1 — URL Shortener
4. Design 2 — Rate Limiter
5. Design 3 — Notification System
6. Design 4 — WhatsApp
7. Design 5 — Uber
8. Design 6 — Netflix
9. Design 7 — Payment System
10. Design 8 — Search Autocomplete
11. Design 9 — BookMyShow
12. Design 10 — Feed Generation (Instagram/Twitter)
13. Design 11 — Distributed Job Scheduler
14. System Design Trade-offs

---

# Chapter 1: The System Design Framework

## Why system design interviews exist

A coding interview tests whether you can solve a well-specified problem correctly. A system design interview tests something different: **can you take an ambiguous, large-scale problem and turn it into a working architecture under real constraints** — limited time, incomplete information, and trade-offs that have no single right answer.

The interviewer isn't grading you against a hidden "correct" diagram. They're watching *how you think*:

- Do you clarify scope before designing, or do you start drawing boxes immediately?
- Do you reason about scale with real numbers, or wave your hands at "a lot of users"?
- Can you go deep on one component when pushed, instead of staying at a buzzword level?
- Do you recognize trade-offs and justify your choice, instead of presenting one option as objectively best?

This is also precisely what you do on the job before writing a design doc. The interview is a compressed, adversarial version of that process.

## The five-step framework

Every design in this book follows the same five steps, in the same order. Skipping a step is the single most common reason candidates fail these interviews.

```
 1. REQUIREMENTS  →  2. ESTIMATION  →  3. HIGH-LEVEL DESIGN  →  4. DEEP DIVE  →  5. TRADE-OFFS
 (what to build)     (how big is it)    (boxes and arrows)      (the hard part)   (what did we give up)
```

1. **Requirements** — Separate *functional* (what the system does) from *non-functional* (how well it does it). This single conversation, done well, takes 5 minutes and saves you from designing the wrong system.
2. **Estimation** — Convert requirements into numbers: requests/sec, storage/year, bandwidth. These numbers *drive* your design decisions (e.g., "12,000 reads/sec" tells you that you need a cache; "90 TB over 5 years" tells you a single Postgres instance won't hold it).
3. **High-level design** — Draw the boxes: client, load balancer, API layer, cache, database, queue, workers. Get something end-to-end on the board before going deep anywhere.
4. **Deep dive** — The interviewer will pick one or two components and ask you to go deep (e.g., "how exactly does the short code get generated without collisions?"). This is where most of the signal comes from.
5. **Trade-offs** — Every decision (SQL vs NoSQL, sync vs async, strong vs eventual consistency) has a cost. State it explicitly rather than letting the interviewer find it.

## Functional vs non-functional requirements

| Type | Question it answers | Example | What it uncovers |
|---|---|---|---|
| Functional | What can the user do? | "Users can shorten a URL and get redirected" | The core features — defines your APIs |
| Non-functional | How well must it perform? | "100M shortens/day, p99 redirect latency < 100ms" | Scale, latency, consistency, availability targets that decide your architecture |

A common mistake is treating non-functional requirements as an afterthought. In practice they decide almost everything: a system needing **strong consistency** (payments) looks completely different from one that's fine with **eventual consistency** (social media likes), even if the functional requirements are similar in shape ("update a counter").

Good clarifying questions to ask in the first five minutes:
- What's the read:write ratio?
- Do we need strong consistency anywhere, or is eventual consistency acceptable?
- What's the expected scale (DAU, requests/sec, data volume)?
- Is this global or single-region?
- What's the acceptable latency (p50, p99)?

## Back-of-envelope estimation: the numbers every engineer must memorize

### Latency hierarchy

You don't need exact numbers — you need the right *order of magnitude*, because that's what decides whether something belongs in memory, on SSD, or behind a network call.

```
L1 cache reference                    0.5    ns
Branch mispredict                     5      ns
L2 cache reference                    7      ns      (~14x L1)
Mutex lock/unlock                     25     ns
Main memory reference (RAM)           100    ns      (~20x L2)
Compress 1 KB (fast codec)            3      µs
Send 1 KB over 1 Gbps network         10     µs
Read 4 KB randomly from SSD           150    µs
Read 1 MB sequentially from RAM       250    µs
Round trip within same datacenter     500    µs       (0.5 ms)
Read 1 MB sequentially from SSD       1      ms
Disk seek (HDD)                       10     ms
Read 1 MB sequentially from HDD       20     ms
Round trip, same continent            ~40    ms
Round trip, cross-continent           ~150   ms
```

**Takeaways that show up in every design:**
- Memory is ~100,000x faster than a disk seek. This is *the* reason caches exist.
- A same-datacenter round trip (0.5ms) is ~300x cheaper than a cross-continent one (150ms). This is why CDNs, edge caching, and regional deployments exist.
- SSD random reads (150µs) are fast enough for OLTP databases; HDD seeks (10ms) are not — this is why SSDs are now the default for transactional databases.

### Throughput estimates (single-node, realistic defaults)

| Component | Realistic single-node throughput | Notes |
|---|---|---|
| MySQL/Postgres (writes) | ~1,000–5,000 simple writes/sec | Depends on indexes, transaction size, disk |
| MySQL/Postgres (reads, no cache) | ~5,000–10,000 reads/sec | With proper indexing |
| Redis (single instance) | ~100,000+ ops/sec | Single-threaded, in-memory, sub-ms latency |
| Single Kafka partition | ~10 MB/s write throughput | Scale by adding partitions, not by making one partition faster |
| Single application server (typical REST) | ~1,000–5,000 req/sec | Depends heavily on payload size and downstream calls |

These are the numbers you multiply against your traffic estimate to decide "do I need one server or a fleet of 50?"

### Storage conversions

The pattern is always: **bytes per entity × entities per day × retention period**.

```
storage = (avg row size in bytes) × (entities created per day) × (retention in days)
```

Example: if each entity is 500 bytes, you create 100M/day, and you retain data for 5 years (1,825 days):

```
500 bytes × 100,000,000 = 50,000,000,000 bytes/day = 50 GB/day
50 GB/day × 1,825 days  = 91,250 GB ≈ 90 TB
```

Always state your assumptions out loud ("I'm assuming ~500 bytes per row including the URL, short code, user ID, and timestamps") — the interviewer cares more that your math is sound than that your assumed row size is exactly right.

## Common pitfalls

- **Jumping straight to a diagram.** Without requirements and estimation, your design is guesswork the interviewer can't evaluate.
- **Skipping estimation entirely.** Numbers are what justify decisions like "we need a cache" or "we need to shard." Without them, every design choice sounds like a guess.
- **Over-engineering for hypothetical scale.** If the interviewer says 1,000 users, don't open with a multi-region Kafka cluster. Match the architecture to the stated scale, and *then* discuss how it changes at 10x.
- **Treating the deep dive as optional.** Candidates who stay at the "boxes and arrows" level the whole interview rarely pass — the deep dive is where the real signal is.
- **Presenting one option with no alternatives.** "I'll use NoSQL" without acknowledging "but that costs us transactional guarantees" reads as inexperience, not confidence.


---

# Chapter 2: Design Building Blocks

These are the pieces you'll reuse in every design in this book. Understand them once here; later chapters assume you know them.

## Load Balancing

A load balancer distributes incoming traffic across a fleet of servers so no single server is overwhelmed, and so the system survives individual server failures.

**L4 (transport layer) vs L7 (application layer):**

| | L4 (TCP) | L7 (HTTP) |
|---|---|---|
| Operates on | IP + port, raw TCP/UDP | HTTP headers, URL paths, cookies |
| Speed | Faster (no payload inspection) | Slower (parses requests) |
| Routing intelligence | None — just forwards connections | Can route `/api/v1/*` to one fleet, `/static/*` to another |
| Use case | High-throughput, protocol-agnostic | Microservices, content-based routing, SSL termination |

**Algorithms:**
- **Round-robin** — requests distributed sequentially. Simple, but ignores server load.
- **Least connections** — sends traffic to the server with the fewest active connections. Better for long-lived or variable-duration requests.
- **IP hash** — `hash(client_IP) % N` always routes the same client to the same server. Useful for naive session stickiness, but rebalances badly when `N` changes (every server gets a new set of clients).
- **Consistent hashing** — maps both servers and request keys onto a hash ring; only `1/N` of keys remap when a server is added/removed. This is the standard solution for sticky sessions and cache sharding at scale (used in Chapter 6's WebSocket routing and Chapter 7's geo-sharding).

```
Consistent hash ring (servers as points on a circle):

              S1
           /      \
        key_A      S4
         |            \
        S2            key_B
           \          /
              S3 --- key_C

key_A → next server clockwise (S1)
Adding S5 between S3 and S4 only remaps keys between S3→S5,
everything else is untouched.
```

## Caching

**Where to cache** (each layer trades freshness for speed):

```
Client (browser/app) → CDN (edge) → API Gateway → Application cache (Redis) → Database (buffer pool)
   fastest, staleest                                                          slowest, freshest
```

- **Client-side**: avoids the network round trip entirely (e.g., HTTP cache headers).
- **CDN/edge**: caches static or semi-static content close to the user.
- **Application cache (Redis/Memcached)**: caches hot rows/computed results so the DB isn't hit on every request.
- **Database buffer pool**: the DB's own in-memory page cache — last line of defense before disk.

**Patterns:**
- **Cache-aside (lazy loading)**: app checks cache → miss → reads DB → writes to cache. Most common pattern; cache only holds what's actually requested.
- **Write-through**: every write goes to cache and DB synchronously. Keeps cache fresh at the cost of write latency.
- **Write-back**: write goes to cache first, flushed to DB asynchronously. Fast writes, risk of data loss if the cache node dies before flush.

**Eviction policies**: LRU (evict least-recently-used — good general default), LFU (evict least-frequently-used — better when popularity is skewed and stable), TTL (time-based expiry — good for data with a natural freshness window).

## CDN (Content Delivery Network)

A CDN is a globally distributed set of edge servers that cache content close to users, cutting cross-continent round trips (150ms) down to same-region ones (~10-40ms).

- **Push CDN**: origin proactively uploads content to edge nodes ahead of time. Good for known, finite content (e.g., a video catalog).
- **Pull CDN**: edge node fetches from origin on first request (cache miss), then serves from cache for subsequent requests (cache hit). Good for unpredictable/long-tail content — this is the default for most web traffic.
- **Cache invalidation**: either set a short TTL and accept brief staleness, or explicitly purge/invalidate the edge cache when origin content changes (more control, more operational complexity).

## Message Queues

Queues decouple producers from consumers in time and in failure domain.

```
Producer → [ Queue ] → Consumer(s)
```

- **Async decoupling**: the producer doesn't block waiting for the consumer to finish — it just enqueues and moves on. This converts a synchronous dependency (if the consumer is slow, the producer is slow) into an async one.
- **Fan-out**: one message delivered to multiple independent consumer groups (e.g., one event triggers an email worker, an analytics pipeline, and a fraud-check service, all reading the same stream independently).
- **Back-pressure handling**: when consumers fall behind, the queue absorbs the burst instead of the burst crashing downstream services. You then either scale consumers horizontally or apply load-shedding upstream.

## API Gateway

A single entry point in front of your services that handles cross-cutting concerns so individual services don't each reimplement them:

- **Authentication** — validate tokens/API keys before traffic reaches services.
- **Rate limiting** — enforce per-user/per-IP quotas (Chapter 4 goes deep here).
- **Routing** — map external paths to internal services.
- **SSL termination** — decrypt TLS once at the edge so internal services communicate over plain (but private-network) HTTP, saving CPU across the fleet.

## Database Selection Guide

| Type | Good for | Examples | Why |
|---|---|---|---|
| SQL (relational) | Transactional data, relationships, strong consistency | PostgreSQL, MySQL | ACID guarantees, joins, mature tooling |
| NoSQL — key-value | Simple lookups by key, extreme scale | Redis, DynamoDB | O(1) access, easy horizontal sharding |
| NoSQL — wide-column | Massive write throughput, time-ordered data | Cassandra, HBase | Partition + clustering key model scales linearly |
| Time-series | Metrics, events, sensor data | InfluxDB, TimescaleDB | Optimized for time-range queries + downsampling |
| Graph | Relationship-heavy queries (friends-of-friends) | Neo4j | Traversal is native, not a chain of joins |
| Search | Full-text / fuzzy search, faceted filtering | Elasticsearch, OpenSearch | Inverted index built for relevance ranking |

The decision usually reduces to one question: **do you need joins and strong consistency (→ SQL), or do you need to scale writes/reads horizontally past what one machine can do (→ NoSQL, picking the sub-type that matches your access pattern)?** Chapter 14 revisits this trade-off in more depth.


---

# Chapter 3: Design 1 — URL Shortener

## Requirements

**Functional**
- Given a long URL, generate a short URL (e.g., `short.ly/abc123`).
- Given a short URL, redirect to the original long URL.
- Track basic analytics (click count, referrer, timestamp) per short URL.

**Non-functional**
- 100M new URLs shortened per day.
- Reads (redirects) are ~10x writes — shortening is rare, clicking is common.
- Redirects must be low-latency (p99 < 100ms) — nobody waits for a redirect.
- Short codes must be unique; once created, a mapping never changes.
- High availability for redirects (this is the user-facing critical path); shortening can tolerate slightly lower availability.

## Estimation

```
Writes (shortens):     100,000,000 / day ÷ 86,400 s/day  ≈ 1,160  ≈ ~1,200 writes/sec (avg)
Reads (redirects):     10x writes                          ≈ 12,000 reads/sec (avg)
                        (peak traffic is typically 2-3x average → design for ~25-35K reads/sec peak)

Storage per record:    long URL (~200B) + short code (~7B) + user_id + timestamps + metadata
                        ≈ 500 bytes/record

Storage over 5 years:  500 bytes × 100,000,000/day = 50 GB/day
                        50 GB/day × 365 × 5 ≈ 91,250 GB ≈ ~90 TB
```

90TB rules out keeping everything in memory and tells us we need a horizontally-scalable persistent store with a cache in front for the hot subset of URLs (the ones currently being clicked).

## Key algorithm question: how to generate short codes

This is the question the interview is actually testing. Three approaches, in order of maturity:

**1. Hash-based (MD5/SHA-256, truncate to 7 chars) — problematic**
```
short_code = base62(md5(long_url))[:7]
```
Looks elegant, but two different long URLs can truncate to the same 7 characters (collision). You then need a retry loop ("try again with a salt") which adds latency and complexity under load. Generally avoided in production designs for exactly this reason.

**2. Auto-increment + Base62 encoding — predictable, no collisions**
```
id = next value from an auto-incrementing counter (e.g., DB sequence)
short_code = base62(id)     // 0-9, a-z, A-Z → 62 symbols
```
7 Base62 characters give 62^7 ≈ 3.5 trillion unique codes — far beyond what we need. No collisions by construction, since `id` is unique. The downside: a single global auto-increment counter is a write bottleneck and single point of contention at 1,200 writes/sec across a distributed fleet.

**3. Distributed ID ranges (ZooKeeper/etcd) — the production answer**
Each API server, on startup, requests a *range* of IDs (e.g., 1,000 IDs) from a coordination service and hands them out locally without talking to ZooKeeper again until the range is exhausted.
```
Server A: ZooKeeper, give me a range  →  gets [1 - 1000]
Server B: ZooKeeper, give me a range  →  gets [1001 - 2000]
```
This removes per-request coordination entirely — ZooKeeper is touched roughly once per 1,000 requests, not once per request — while still guaranteeing global uniqueness. This is the approach used in this design.

## Architecture

```
                         ┌──────────────┐
   Client ───────────────▶ Load Balancer├──────────────┐
                         └──────────────┘               │
                                                          ▼
                                              ┌────────────────────┐
                                              │   API Servers       │
                                              │  (Shorten + Redirect)│
                                              └──────┬──────┬────────┘
                                                      │      │
                       writes/lookups (uncached)      │      │ on shorten: get ID range
                                                      ▼      ▼
                                       ┌───────────────┐  ┌────────────┐
                                       │ Redis (cache)  │  │ ZooKeeper   │
                                       │ short_code →   │  │ (ID ranges) │
                                       │   long_url     │  └────────────┘
                                       └───────┬────────┘
                                               │ cache miss
                                               ▼
                                       ┌────────────────┐
                                       │  PostgreSQL     │
                                       │ (sharded by     │
                                       │  short_code)    │
                                       └───────┬─────────┘
                                               │ click events
                                               ▼
                                       ┌────────────────┐      ┌──────────────┐
                                       │     Kafka       │─────▶│  Aggregator  │──▶ Time-series DB
                                       │ (click stream)  │      │ (Flink/Spark)│    (analytics dashboards)
                                       └────────────────┘      └──────────────┘
```

## Deep dive: redirect flow

1. Client requests `GET short.ly/abc123`.
2. API server checks Redis for `abc123` → cache hit (the common case, since traffic follows a Pareto distribution — a small set of URLs get most clicks) → return immediately.
3. On cache miss, query PostgreSQL, populate Redis with a TTL, then respond.
4. Respond with **HTTP 302 (Found)**, not 301 (Moved Permanently).

**Why 302, not 301?** A 301 tells the browser "this redirect is permanent — cache it and never ask my server again." That breaks click analytics, since the browser will skip your server on subsequent visits. A 302 says "redirect now, but ask me again next time," which keeps every click flowing through your servers for counting.

## Analytics pipeline

Each redirect emits a click event (short_code, timestamp, referrer, geo) to Kafka asynchronously — never on the synchronous redirect path, since analytics must not add latency to the user-facing redirect. A stream aggregator (Flink/Spark Streaming) consumes the topic, rolls up counts per short_code per time window, and writes results to a time-series store for dashboards.

## What if the scale is 10×?

At 12,000 writes/sec and 120,000 reads/sec:
- **Database**: shard PostgreSQL by `short_code` hash (consistent hashing, so adding shards doesn't reshuffle everything) — a single Postgres instance tops out around 5-10K writes/sec.
- **Cache**: move from a single Redis instance (~100K ops/sec, already plenty for 120K reads if hit rate is high) to a Redis Cluster mainly for *memory* capacity (hot-set size grows with traffic) rather than raw throughput.
- **CDN**: cache the redirect response itself at the CDN edge for the small set of extremely hot URLs (viral links), removing them from your origin entirely.
- **ID generation**: increase the range size handed out per server (e.g., 1,000 → 10,000) so ZooKeeper contention doesn't grow linearly with traffic.

## Trade-offs

- **Base62 auto-increment vs hashing**: chose auto-increment for guaranteed uniqueness at the cost of (slightly) predictable/sequential codes — acceptable since short codes aren't meant to be secret.
- **302 vs 301**: chose 302 to preserve analytics at the cost of a marginally slower redirect for the client (one extra request per click instead of zero on repeat visits).
- **Cache-aside with TTL** for redirects: simpler than write-through, accepts brief staleness in the rare case a mapping is updated (which, by design, never happens).

## Interview follow-ups

**Q: "What happens if a server crashes after taking an ID range but before using it all?"**
A: Those IDs are simply lost — never reused. With 62^7 ≈ 3.5 trillion possible codes against ~180 billion codes needed over 5 years, wasting a few thousand IDs per crash is a non-issue. This is a deliberate trade-off: lose a negligible amount of ID space in exchange for removing per-request coordination.

**Q: "How would you support custom aliases (user picks their own short code)?"**
A: Check existence with `INSERT ... ON CONFLICT DO NOTHING` (or `SELECT FOR UPDATE` then insert) instead of generating from the counter; reject if taken. This path bypasses the ID-range generator entirely since the "ID" is user-supplied.

**Q: "How do you prevent someone from enumerating all short URLs by incrementing the code?"**
A: Don't expose codes sequentially to the *client* even though they're sequential internally — e.g., shuffle the bit pattern of the ID before Base62-encoding it (a reversible permutation, like a Feistel cipher on the integer) so consecutive IDs don't produce consecutive-looking codes.


---

# Chapter 4: Design 2 — Rate Limiter

## Requirements

**Functional**: limit the number of requests a client (user or IP) can make in a given time window, and reject (HTTP 429) requests beyond that limit.

**Non-functional**: the limiter itself must add minimal latency (<5ms), must work correctly across a fleet of distributed gateway nodes (not just per-server), and must survive node failures without letting the limit be bypassed or wrongly enforced.

## Algorithms

```
1. FIXED WINDOW                         2. SLIDING WINDOW LOG
   |--window--|--window--|                 [t1][t2][t3]...[tn]  (every request timestamped)
   count resets to 0 at                    window = now - N seconds, count entries inside it
   each boundary
   Pro: simple, O(1) memory               Pro: perfectly accurate
   Con: burst at boundary can             Con: O(N) memory — stores every
        let 2x the limit through               timestamp in the window

3. SLIDING WINDOW COUNTER               4. TOKEN BUCKET
   weighted avg of current +                bucket holds up to N tokens,
   previous fixed window,                   refills at rate R/sec,
   based on time elapsed                    each request consumes 1 token
   Pro: smooths the boundary               Pro: allows controlled bursts
        burst problem cheaply                   up to bucket size
   Con: approximation, not exact           Con: needs to track refill time
                                                 per client

5. LEAKY BUCKET
   requests queue up, processed
   (leak out) at a constant rate
   Pro: smooths bursts into a
        constant outflow rate
   Con: bursty clients experience
        queuing delay, not rejection
```

| Algorithm | Use case |
|---|---|
| Fixed window | Simple quotas where occasional boundary bursts are acceptable (e.g., "1000 req/hour" billing limits) |
| Sliding window log | Strict accuracy needed, low-volume clients (cost of storing every timestamp is bounded) |
| Sliding window counter | The common production default — good accuracy, cheap |
| Token bucket | APIs that want to allow legitimate bursts (e.g., a client catching up after a network blip) |
| Leaky bucket | Smoothing traffic into a downstream system that needs a constant rate (e.g., protecting a fixed-capacity worker pool) |

This design uses the **sliding window counter** as the default, with **token bucket** as the documented alternative for endpoints that want to allow bursts.

## Distributed rate limiting: the atomicity problem

A naive "GET count, check, INCR" from the gateway has a race condition: two concurrent requests can both read count=99 (limit 100), both pass the check, and both increment — letting 101 through. The fix is to make check-and-increment **atomic** using a Redis Lua script (Lua scripts run atomically inside Redis, with no other command interleaving):

```lua
-- KEYS[1] = rate limit key (e.g. "rl:user123")
-- ARGV[1] = limit, ARGV[2] = window in seconds
local current = redis.call("INCR", KEYS[1])
if current == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[2])
end
if current > tonumber(ARGV[1]) then
    return 0   -- reject
end
return 1       -- allow
```
One round trip to Redis, executed atomically — no race condition, regardless of how many gateway nodes call it concurrently.

## Architecture

```
                 ┌──────────────┐
 Client ─────────▶ API Gateway   │
                 └──────┬───────┘
                        │ every request
                        ▼
              ┌───────────────────┐
              │ Rate Limiter        │
              │ (Lua script, atomic │
              │  check-and-incr)    │
              └─────────┬───────────┘
                        │
                        ▼
              ┌───────────────────┐
              │  Redis (cluster)    │
              │  key = user/IP id   │
              └───────────────────┘
                        │
            allowed ────┴──── rejected → HTTP 429
                │
                ▼
        ┌───────────────┐
        │ App Servers     │
        └───────────────┘
```

## Where to place the limiter

- **At the API Gateway (centralized)**: one enforcement point, simplest to reason about, protects every downstream service uniformly. Chosen here as the default.
- **Per-service (distributed)**: each service enforces its own limits — necessary when different services need wildly different limits (e.g., a search endpoint vs a file-upload endpoint), at the cost of duplicated logic and multiple Redis round trips per request if a single user-facing action touches several services.

## What if the scale is 10×?

- Redis itself isn't the bottleneck (100K+ ops/sec per node) — but at very high client cardinality (millions of distinct users), shard Redis by `hash(user_id)` so no single node holds every key.
- Move from a synchronous Redis call per request to a **local in-memory approximate counter** at each gateway node that syncs to Redis every ~100ms, trading perfect accuracy for far fewer round trips — acceptable since rate limits are inherently a soft guarantee, not a financial guarantee.

## Trade-offs

- **Sliding window counter vs sliding window log**: chose the counter for O(1) memory at the cost of being an approximation rather than perfectly exact.
- **Centralized Redis vs local in-memory state**: chose centralized for correctness across the fleet at the cost of a network round trip per request (mitigated by Redis's sub-ms latency).

## Interview follow-ups

**Q: "What happens if Redis goes down?"**
A: Fail open (allow all requests) or fail closed (reject all), and this is a product decision, not a technical one — failing open risks abuse during an outage, failing closed turns a Redis blip into a full outage. Most production systems fail open for short blips and rely on Redis being deployed as a highly-available cluster (replicas + sentinel/cluster mode) to make this rare.

**Q: "How do you rate-limit per-user *and* per-IP simultaneously?"**
A: Run two independent checks (two different Redis keys, two Lua script calls or one script checking both) and reject if *either* limit is exceeded — this catches both "one user abusing across many IPs" and "many users behind one abusive IP/proxy."


---

# Chapter 5: Design 3 — Notification System

## Requirements

**Functional**: send push notifications, email, SMS, and in-app notifications, triggered by application events (e.g., "payment failed," "new comment," "weekly digest").

**Non-functional**: 10M users; 1M notifications/hour average, with bursts far higher during broadcast events; delivery must respect priority — a payment-failure alert must not sit behind a marketing blast in the queue; no duplicate sends.

## Estimation

```
Average:  1,000,000 / hour ÷ 3,600 s  ≈ 278 notifications/sec
Peak (broadcast to all users at once): up to 1M notifications dispatched within
                                        a few minutes → tens of thousands/sec burst
```
The gap between average (278/sec) and burst (tens of thousands/sec) is the entire design problem: the system must absorb huge spikes without falling over or starving high-priority traffic — which is why this goes through a queue rather than direct synchronous sends.

## Priority queues

Not all notifications are equal. A naive single queue processed FIFO means a 1M-user marketing broadcast can delay a critical payment-failure alert by minutes. The fix: separate Kafka topics per priority tier, each consumed independently, with consumer capacity allocated so higher tiers are never starved.

```
CRITICAL  (payment failed, security alert)   → topic: notif.critical  → dedicated worker pool, drained first
HIGH      (order shipped, OTP code)          → topic: notif.high
MEDIUM    (new comment, mention)             → topic: notif.medium
LOW       (marketing, weekly digest)         → topic: notif.low      → processed with leftover capacity
```

## Deduplication

Many events can trigger the same logical notification twice (retries, multiple services emitting the same event). Idempotency is enforced with a Redis SET check before sending:

```
key = "notif:sent:" + idempotency_key   (idempotency_key derived from event_id + channel + user_id)
SET key "1" NX EX 86400                  -- NX = only set if not exists, 24h TTL
if SET succeeded → this is the first time → send
if SET failed     → already sent → skip
```
The 24-hour TTL bounds Redis memory usage while comfortably covering the window in which duplicate events are likely to arrive (retries, replays).

## Architecture

```
 App Events ───▶ ┌─────────────────────┐
                  │  Notification API     │
                  └──────────┬────────────┘
                             │ dedup check (Redis SET NX)
                             ▼
              ┌──────────────────────────────────┐
              │              Kafka                 │
              │  topics: critical / high / medium /│
              │          low (priority-partitioned)│
              └───┬─────────┬─────────┬────────────┘
                  ▼         ▼         ▼
           ┌───────────────────────────────┐
           │      Channel Workers            │
           │  (Push / Email / SMS / In-app)  │
           └───┬─────────┬─────────┬─────────┘
               ▼         ▼         ▼
          ┌────────┐┌────────┐┌────────┐
          │  FCM/   ││ SendGrid││ Twilio │   ← 3rd-party providers
          │  APNs   ││         ││        │
          └────┬───┘└────┬───┘└────┬────┘
               │         │         │
               ▼         ▼         ▼
        ┌───────────────────────────────┐
        │   Delivery Tracking (DB)        │
        │ PENDING→SENT→DELIVERED→FAILED   │
        │   updated via webhook callbacks │
        └───────────────────────────────┘
```

## Delivery tracking

Each notification has a state machine: `PENDING → SENT → DELIVERED → FAILED`. `SENT` is set once the provider (FCM/SendGrid/Twilio) accepts the request; `DELIVERED` is set asynchronously when the provider's webhook confirms actual delivery to the device/inbox; `FAILED` triggers a retry (with backoff) up to a max attempt count, after which it's surfaced for investigation rather than retried indefinitely.

## Scale challenge: fan-out to 1M users for a broadcast

Sending to 1M users from a single API call is the core scaling problem here. The approach: the API doesn't loop over users synchronously — it writes **one** "broadcast" event to Kafka, and a dedicated fan-out worker expands it into per-user messages, publishing those to the priority topics in batches. This keeps the originating API call fast (it returns as soon as the single broadcast event is durably written) and lets the fan-out worker scale horizontally (partition the user base across multiple worker instances) independent of the API tier.

## What if the scale is 10×?

- 2,780 notifications/sec average, broadcast bursts in the hundreds of thousands: scale Kafka partition count and channel-worker consumer group size together (more partitions = more parallel consumers).
- Move deduplication from a single Redis instance to a Redis Cluster sharded by `idempotency_key` hash.
- Pre-batch provider API calls (most push/email/SMS providers support batch send endpoints) to reduce per-message HTTP overhead, since at this scale the bottleneck shifts from your infrastructure to third-party provider rate limits.

## Trade-offs

- **Kafka topics per priority** vs a single topic with priority field: chose separate topics so consumer scaling and starvation-avoidance are structural (separate consumer groups) rather than relying on application-level sorting logic, at the cost of slightly more operational topics to manage.
- **Idempotency via Redis SET NX**: simple and fast, at the cost of a 24h window outside of which a genuine duplicate could theoretically slip through (acceptable trade-off given how unlikely a >24h-delayed retry is).

## Interview follow-ups

**Q: "How do you guarantee CRITICAL notifications aren't delayed behind a LOW broadcast even with shared infrastructure?"**
A: Separate consumer groups per topic mean CRITICAL has its own dedicated worker pool that's never blocked waiting on LOW's queue — the worst case is CRITICAL workers being CPU/network constrained, which is solved by giving that pool more capacity headroom than its average load requires.

**Q: "What if a user opts out of a notification type after the broadcast fan-out has already started?"**
A: Check opt-out status at the channel-worker stage (just before calling the provider), not just at fan-out time — fan-out can take minutes for 1M users, so a late opt-out should still be honored for users not yet processed.


---

# Chapter 6: Design 4 — WhatsApp

## Requirements

**Functional**: 1-to-1 messaging, group messaging (up to 256 members), online/last-seen status, delivery and read receipts.

**Non-functional**: 50M DAU; 100B messages/day; message delivery <500ms when both parties are online; messages must not be lost even if the recipient is offline for days.

## Estimation

```
Messages/sec (avg):   100,000,000,000 / 86,400 s  ≈ 1,157,000 ≈ ~1.16M messages/sec (avg)
                       (peak, concentrated in evening hours, easily 3-5x avg → ~4-5M msgs/sec peak)

Concurrent WebSocket
connections (peak DAU
online simultaneously):  up to ~50M

Storage per message:   ~100-150 bytes (sender, recipient/group, ciphertext ref, timestamp, status)
                        at 100B msgs/day: ~15 TB/day of message metadata alone (before media)
```

These numbers immediately rule out a single chat server design — no single machine accepts 50M concurrent TCP connections, and no single database accepts 1.16M writes/sec. Everything in this design is about horizontal partitioning of connections and storage.

## WebSocket connections: maintaining 50M concurrent connections

A single modern server can hold roughly 50K-100K concurrent idle WebSocket connections (limited by file descriptors and memory per connection, not CPU). To hold 50M connections you need a fleet of **chat servers**, each owning a subset of connections — roughly 500-1,000 chat server instances at 50-100K connections each.

**The core problem this creates**: if user A is connected to chat-server-7 and wants to message user B, who's connected to chat-server-203, how does server 7 know to route the message to server 203?

```
                  ┌─────────────────────┐
                  │  Connection Registry  │   maps: user_id → chat_server_id
                  │   (Redis, sharded)     │
                  └──────────┬────────────┘
                             │ on connect: SET user_id → server_id
                             │ on lookup: GET recipient's server_id
                             │
   User A ──ws──▶ Chat Server 7 ──lookup(B)──▶ Connection Registry ──▶ "B is on Server 203"
                       │
                       └──publish to Kafka topic for Server 203──▶ Chat Server 203 ──ws──▶ User B
```

When a user connects, their chat server registers `user_id → server_id` in a sharded Redis registry (sharded by `hash(user_id)`, consistent hashing so registry nodes can scale). To send a message, the sending server looks up the recipient's server in the registry, then routes the message there — typically via a Kafka topic-per-chat-server-shard, which also gives durability (if Server 203 briefly restarts, the message waits in Kafka instead of being dropped).

## Message flow

```
Sender ──▶ Chat Server (sender's) ──▶ Kafka (per-recipient-shard topic) ──▶ Chat Server (recipient's) ──▶ Recipient
                  │
                  └──▶ Cassandra (durable write — happens in parallel, not blocking delivery)
```

The message is written to Cassandra for durability *in parallel* with being routed for live delivery — the user shouldn't wait for a Cassandra write to get a "delivered" receipt, but the message must survive even if delivery to a currently-offline recipient fails.

## Storage: Cassandra

```
Partition key:   conversation_id   (1-1 chat: hash of the two user IDs, sorted;
                                     group chat: the group's ID)
Clustering key:  message_timestamp (descending)

PARTITION: conversation_id = "userA_userB"
  ├─ message_ts=2026-06-20T10:03:01  { sender: A, text_ref, status: DELIVERED }
  ├─ message_ts=2026-06-20T10:02:45  { sender: B, text_ref, status: READ }
  └─ message_ts=2026-06-20T10:01:12  { sender: A, text_ref, status: READ }
```
This layout makes "fetch the last N messages of a conversation" a single-partition range scan — Cassandra's strength — rather than a cross-partition query. Partitioning by `conversation_id` also naturally distributes write load across the cluster, since no single conversation dominates total traffic the way a single "all messages" table would create hotspots.

## Offline delivery

If the recipient's `user_id → server_id` lookup finds no active connection, the message is:
1. Written to Cassandra (already happens for every message, online or not).
2. A push notification (FCM/APNs) is sent to wake the recipient's device.
3. On reconnect, the client fetches any messages with timestamp greater than its last-synced timestamp for each conversation — Cassandra's clustering-by-timestamp layout makes this an efficient range query.

## Group messaging: fan-out

When a user sends a message to a 256-member group, the sender's chat server sends it **once** to a group-fan-out step, which expands it into per-recipient routing (registry lookup + Kafka publish) for each of the 256 members. The client only makes one network call; the fan-out cost (256x) is absorbed server-side, where it can be parallelized and is far cheaper than 256 round trips from the sender's device.

## What if the scale is 10×?

- ~11.6M messages/sec average: shard the chat-server-registry Redis further and increase Kafka partition count proportionally (partitions are the unit of parallelism for both writes and consumer fan-out).
- 500M concurrent connections: this is where the chat-server fleet itself becomes the bottleneck — invest in connection density per server (e.g., moving from a thread-per-connection model to an event-loop model, or to lighter-weight runtimes) rather than purely adding more servers, since registry lookups and inter-server routing cost also scale with fleet size.
- Cassandra: add nodes (linear scalability is Cassandra's core selling point) and consider time-bucketing the partition key (e.g., `conversation_id + month`) so old, cold conversations don't bloat the same partition indefinitely.

## Trade-offs

- **Cassandra over PostgreSQL** for message storage: chosen for write-heavy, horizontally-scalable, time-ordered access at the cost of giving up multi-row transactions and ad-hoc query flexibility (Cassandra queries must match the partition/clustering key design chosen up front).
- **At-least-once delivery with client-side dedup** (each message has a client-generated UUID) rather than complex distributed exactly-once delivery — simpler to build, and idempotent message IDs make duplicates harmless on the client.

## Interview follow-ups

**Q: "How do you handle a chat server crashing with active connections?"**
A: All those connections drop; clients detect the disconnect and reconnect (with backoff) to a *different* server via the load balancer, which re-registers them in the connection registry. Any messages sent to the crashed server in the brief gap are sitting safely in Kafka and get redelivered once the user reconnects and the new server picks up their backlog.

**Q: "How do read receipts work without doubling message volume?"**
A: A read receipt is a small control message (conversation_id, message_id, READ status) routed through the exact same chat-server-to-chat-server path as a normal message — it's cheap (a few bytes) compared to the message itself, so it doesn't meaningfully add to the 1.16M msgs/sec figure even though, strictly, it doubles message *count*.


---

# Chapter 7: Design 5 — Uber

## Requirements

**Functional**: drivers continuously share GPS location; riders request a trip; the system matches riders to nearby available drivers in real time.

**Non-functional**: 5M trips/day; 3M active drivers; each driver sends a location update every 4 seconds; matching must complete in low seconds, not minutes.

## Estimation

```
Location update throughput: 3,000,000 drivers ÷ 4 sec/update ≈ 750,000 location updates/sec

Trips/sec (avg):            5,000,000 / 86,400 ≈ 58 trips/sec (avg, much higher at peak hours —
                             commute peaks can be 5-10x average)
```
The 750K updates/sec figure dwarfs the trip-matching rate — location ingestion, not trip creation, is the throughput bottleneck this design has to solve.

## The geo-indexing problem

Given a rider's location, find available drivers within ~2km. A naive `SELECT * FROM drivers WHERE distance(lat,lng, rider_lat,rider_lng) < 2km` requires scanning every driver row and computing distance for each — infeasible at 3M drivers updating every 4 seconds.

### Geohash

Geohash encodes a (lat, lng) pair into a string where **nearby locations share a common prefix**. Each additional character narrows the bounding box.

```
geohash("12.97, 77.59")  →  "tdr1y"
geohash("12.971,77.591") →  "tdr1y"   (same prefix → same ~2.4km × 2.4km cell)

Precision (chars) → cell size:
  5 chars  ≈ 2.4km × 2.4km     ← good fit for "drivers within ~2km"
  6 chars  ≈ 0.6km × 0.6km
  7 chars  ≈ 150m × 150m
```
To find nearby drivers, compute the rider's geohash at the chosen precision, then query that cell **and its 8 neighboring cells** (to catch drivers just across a cell boundary) instead of scanning the whole driver set.

### Redis GEOADD / GEORADIUS — built-in geo indexing

Rather than hand-rolling geohash-cell lookups, Redis natively supports geospatial indexing using geohashing internally:

```
GEOADD drivers:geo  77.5946 12.9716  "driver_8841"     -- driver updates location every 4s
GEORADIUS drivers:geo 77.60 12.97 2 km                  -- find all drivers within 2km
```
This gives sub-millisecond nearby-driver lookups without building a custom spatial index — Redis stores locations as a sorted set internally, ordered by geohash, making radius queries an efficient range scan.

## Architecture

```
 Driver App ──(loc every 4s)──▶ ┌────────────────────┐
                                  │  Location Service     │
                                  └──────────┬─────────────┘
                                             │ GEOADD (overwrite driver's position)
                                             ▼
                                  ┌────────────────────┐
                                  │   Redis GEO           │  (sharded by geohash region)
                                  └──────────┬─────────────┘
                                             │ GEORADIUS (nearby drivers)
                                             ▼
 Rider App ──(request trip)──▶  ┌────────────────────┐
                                  │  Matching Service     │── ranks by: distance, rating, availability
                                  └──────────┬─────────────┘
                                             │ assign + notify
                                             ▼
                                  ┌────────────────────┐
                                  │   Trip Service        │──▶ PostgreSQL (trip record, billing)
                                  └────────────────────┘
                                             │ location stream (all updates)
                                             ▼
                                  ┌────────────────────┐
                                  │   Kafka Streams       │── counts rides requested / drivers
                                  │  (surge pricing)      │   available, per geohash, per 5-min window
                                  └────────────────────┘
```

## Matching algorithm

1. Compute rider's geohash; `GEORADIUS` against Redis for candidate drivers within 2km.
2. Filter to drivers currently marked **available** (not already on a trip).
3. Rank candidates by a weighted score: distance (closer is better), driver rating, and how long they've been idle (to fairly rotate trip offers rather than always picking the single closest driver).
4. Offer the trip to the top-ranked driver with a short timeout (e.g., 10-15 seconds); on decline or timeout, offer to the next candidate.

## Surge pricing

A Kafka Streams job consumes the raw location/request event stream and maintains a sliding 5-minute window count of **ride requests** vs **available drivers**, grouped by geohash cell. When the ratio of requests to available drivers in a cell crosses a threshold, a surge multiplier is computed and published for that cell — applied to new fare quotes in real time without needing to query a database per quote.

```
geohash cell "tdr1y", 5-min window:
   requests = 340     available_drivers = 60     ratio = 5.7  →  surge x1.8
```

## What if the scale is 10×?

- 7.5M location updates/sec: shard Redis GEO by geographic region (e.g., one Redis Cluster per metro/geohash-prefix) rather than one global instance — this also reduces the blast radius of a single node failure to one region.
- Matching service: scale horizontally behind the location-update sharding boundary, so a matching request never needs to cross regional Redis shards for a local search.
- Consider downsampling location update frequency for drivers far from any pending rider demand (adaptive update intervals) to cut unnecessary write volume in low-demand areas.

## Trade-offs

- **Redis GEO over a custom geospatial DB (e.g., PostGIS)**: chosen for sub-ms in-memory lookups at massive update rates, at the cost of weaker query expressiveness (no complex polygon queries — just radius/box) and the durability concerns of an in-memory store (mitigated since driver location is inherently ephemeral and self-heals on the next 4-second update).
- **Eventual consistency on driver availability**: a driver could be offered to two riders almost simultaneously in a race; resolved by the trip-service treating "accept" as a conditional write (first acceptance wins, second gets "driver no longer available") rather than trying to prevent the race upstream.

## Interview follow-ups

**Q: "What happens if a driver's app loses connectivity for 30 seconds?"**
A: Their last known location in Redis GEO becomes stale but isn't proactively removed; the matching service can apply a freshness check (ignore drivers whose last update is older than, say, 15-20 seconds) so they're naturally excluded from new matches until they reconnect and resume updates.

**Q: "How would you avoid matching a rider with a driver who's about to go off-shift?"**
A: Add driver-declared availability windows as a filter applied after the geo-radius candidate list, before ranking — geo-proximity finds *who's nearby*, a separate availability check decides *who's eligible*, keeping the two concerns independent.


---

# Chapter 8: Design 6 — Netflix

## Requirements

**Functional**: content owners/Netflix upload videos; users stream videos at adaptive quality; users search the catalog; users see personalized recommendations.

**Non-functional**: 200M subscribers; 500M streaming hours/day, worldwide; streaming must adapt smoothly to each viewer's network conditions with minimal buffering.

## Estimation

```
Average concurrent streams:  500,000,000 hours/day ÷ 24h  ≈ 20.8M concurrent streams (uniform avg)
                              Real viewing is concentrated in evening hours per region —
                              peak concurrency is commonly 3-4x the naive average →
                              ~60-80M concurrent streams at peak.

Bandwidth at peak:           ~70M concurrent streams × ~5 Mbps avg bitrate (mixed SD/HD/4K)
                              ≈ 350 Tbps of egress at global peak
```
That bandwidth figure is the entire reason Netflix's architecture centers on a CDN — no centralized data center setup serves 350 Tbps directly to consumer ISPs; the content has to live physically close to viewers.

## Video upload pipeline

```
 Content owner ──upload──▶ S3 (raw master file)
                                │
                                ▼
                     ┌────────────────────┐
                     │  Transcoding Service  │  (EMR / distributed transcoding cluster)
                     │  → multiple resolutions │
                     │    (240p…4K) × multiple │
                     │    bitrates per resolution│
                     └──────────┬─────────────┘
                                ▼
                     S3 (processed, chunked into
                          multi-second segments)
                                ▼
                     ┌────────────────────┐
                     │   CDN (Open Connect)  │ ──▶ pre-positioned in ISP data centers
                     └────────────────────┘        worldwide, close to viewers
```
A single master file is transcoded into **many** resolution/bitrate variants up front (not on-demand), because transcoding is CPU-expensive and the same processed output is reused by millions of subsequent viewers — paying the cost once at upload time is far cheaper than paying it per-stream.

## Adaptive bitrate streaming (HLS/DASH)

The video is split into short segments (typically 2-10 seconds each), with each segment encoded at multiple bitrates. The client downloads a manifest listing available bitrates, then picks segments dynamically:

```
Manifest:
  240p  @ 0.4 Mbps  → segment_001_240p.ts, segment_002_240p.ts, ...
  480p  @ 1.5 Mbps  → segment_001_480p.ts, segment_002_480p.ts, ...
  1080p @ 5   Mbps  → segment_001_1080p.ts, segment_002_1080p.ts, ...
  4K    @ 15  Mbps  → segment_001_4k.ts, segment_002_4k.ts, ...

Client logic (runs every ~4s, once per segment):
  measure recent download throughput
  → throughput comfortably covers 1080p bitrate? request next segment at 1080p
  → throughput drops?                            request next segment at 480p
```
Because each bitrate's segments are aligned to the same timestamps, the client can switch quality **mid-stream, between segments**, without a visible restart — this is what lets a viewer's stream degrade gracefully on a weakening WiFi signal instead of stalling.

## CDN strategy: Open Connect Appliances

Rather than relying purely on third-party CDNs, Netflix places its own caching appliances ("Open Connect Appliances," OCAs) physically inside ISP data centers. A request from a viewer is served from an OCA inside (or very near) their own ISP's network — often just one network hop away — rather than traversing the broader internet to a centralized origin. This is the single biggest lever against the 350 Tbps peak-bandwidth figure: it converts a problem of "serve enormous bandwidth from our data centers" into "pre-position content so the ISP serves most of the bandwidth on our behalf."

## Recommendations

```
 Viewing events ──▶ Kafka ──▶ Batch/streaming ML pipeline
                               (collaborative filtering: users who watched
                                similar things tend to enjoy similar things)
                                          │
                                          ▼
                                  Feature Store
                                          │
                                          ▼
                                  Redis (precomputed per-user
                                          recommendation lists)
                                          │
                                          ▼
                              served instantly on app open
                              (no real-time ML inference on
                               the critical path)
```
Recommendations are **precomputed** offline/near-real-time and cached per user in Redis, rather than computed live on each app open — running collaborative filtering against the full catalog at request time would be far too slow for a sub-second home-screen load.

## What if the scale is 10×?

- 2B subscribers, ~5B streaming hours/day: this mostly stresses the CDN footprint (more OCAs, deeper into more ISPs) rather than the origin infrastructure, since the design's whole point is that origin traffic is a small fraction of total egress.
- Transcoding throughput scales by adding more distributed transcoding workers (embarrassingly parallel — each video segment transcodes independently).
- Recommendation feature store: shard by user_id; the precompute job becomes a larger, more frequently-running batch/streaming pipeline, but the serving path (Redis lookup) doesn't change in shape.

## Trade-offs

- **Pre-transcoding all bitrates upfront** vs transcoding on demand: chosen for fast playback start at the cost of significant upfront storage (every video stored in many resolution/bitrate variants) and compute at ingest time.
- **Own CDN (Open Connect) vs pure third-party CDN reliance**: chosen for cost control and ISP-level proximity at massive scale, at the cost of operating physical hardware deployed across thousands of external networks — a major operational undertaking only justified at Netflix's traffic volume.

## Interview follow-ups

**Q: "How does the client decide when to switch bitrates, exactly?"**
A: Most ABR algorithms combine two signals: recent measured throughput (How fast did the last few segments download?) and current buffer health (How many seconds of video are already buffered?). A healthy buffer allows a more conservative/aggressive quality bump; a draining buffer forces a drop to a lower bitrate even if throughput looks fine, to avoid stalling.

**Q: "What happens on a cache miss at the OCA — i.e., a less popular title an ISP's appliance doesn't have cached?"**
A: The OCA fetches it from a regional/origin tier (a smaller number of larger fill servers), caches it locally for subsequent viewers in that ISP, and serves the requesting viewer with marginally higher latency just for that first fetch — exactly the pull-CDN pattern from Chapter 2, applied at Netflix's specific scale.


---

# Chapter 9: Design 7 — Payment System

## Requirements

**Functional**: accept payments from customers, process them through a payment processor, settle funds to merchants, support refunds.

**Non-functional**: the single hardest non-functional requirement in this book — **never lose money or double-charge**; exactly-once *effect* (not necessarily exactly-once delivery — see deep dive below); high availability; full auditability for every state change.

## Why this design is different from the others

Every other system in this book can tolerate some sloppiness — a duplicated notification, a stale recommendation, a slightly-late chat message are all annoying but not catastrophic. A duplicated *charge* is a regulatory and trust problem. This reframes nearly every decision: this design favors strong consistency and durability over latency or throughput, in direct contrast to, say, Chapter 6's WhatsApp design.

## Idempotency

The client (or a retry from your own service) might send the same payment request twice — due to a network timeout where the first request actually succeeded but the client never saw the response. The fix is an **idempotency key** supplied by the caller:

```
Client sends: POST /charge
              Header: X-Idempotency-Key: "client-generated-uuid-abc"

Server logic:
  1. Check Redis/DB: has this idempotency key been seen before?
     - Yes, and it's still processing  → return 409 (in-flight, don't double-process)
     - Yes, and it completed           → return the SAME stored result (don't reprocess)
     - No                              → proceed to step 2
  2. Process the charge.
  3. Store the result keyed by idempotency key (durably, not just in Redis —
     Redis is a fast-path cache; the database row is the source of truth).
```
This converts "the network is unreliable, so the client may retry" from a correctness risk into a non-issue: retries with the same key always return the original outcome instead of charging twice.

## Saga pattern for the distributed payment flow

A single payment touches multiple systems that can't be wrapped in one ACID transaction (your payment service, the card network, the merchant's ledger, your own ledger). The **saga pattern** breaks this into a sequence of local transactions, each with a defined **compensating action** if a later step fails:

```
Step 1: Reserve funds (hold) on customer's card        → compensate: release hold
Step 2: Charge the card (capture)                       → compensate: refund
Step 3: Credit merchant's internal ledger                → compensate: debit ledger
Step 4: Mark order as paid                                → compensate: mark order as payment-failed

If step 3 fails after step 2 succeeded:
   → run step 2's compensating action (refund the charge)
   → the customer is never charged for a payment that didn't fully complete
```
Each step publishes an event on completion or failure; a saga orchestrator (or a choreography of services each listening for the previous step's event) drives the sequence forward or triggers compensation backward.

## Database: PostgreSQL + event sourcing

Rather than just storing the *current* state of a payment ("status = COMPLETED"), every state transition is stored as an immutable event:

```
payment_id=PAY-9921
  event: CREATED          ts=10:00:01
  event: FUNDS_RESERVED   ts=10:00:02
  event: CHARGE_CAPTURED  ts=10:00:04
  event: MERCHANT_CREDITED ts=10:00:05
  event: COMPLETED        ts=10:00:05

current state = fold(all events) = COMPLETED
```
This gives a complete, immutable audit trail (required for financial compliance and dispute resolution) and lets you reconstruct the exact state of any payment at any point in time — something a simple "current status" column can never do, since it overwrites history.

## Architecture

```
 Client ──charge request (with idempotency key)──▶ ┌──────────────────┐
                                                       │  Payment API       │
                                                       └────────┬───────────┘
                                                                │ idempotency check
                                                                ▼
                                                       ┌──────────────────┐
                                                       │  Redis (fast-path  │
                                                       │  idempotency cache)│
                                                       └────────┬───────────┘
                                                                ▼
                                                       ┌──────────────────┐
                                                       │  Saga Orchestrator │
                                                       └───┬────┬────┬─────┘
                                                            │    │    │
                                              ┌─────────────┘    │    └──────────────┐
                                              ▼                  ▼                   ▼
                                    ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐
                                    │ Card Network   │   │  PostgreSQL    │   │ Merchant Ledger    │
                                    │ (external)     │   │ (event-sourced │   │ Service             │
                                    └──────────────┘   │  payment log)  │   └──────────────────┘
                                                         └──────────────┘
                                                                │
                                                                ▼ (nightly batch)
                                                       ┌──────────────────┐
                                                       │  Reconciliation     │── compares internal
                                                       │  Job                │   sum vs bank settlement
                                                       └──────────────────┘
```

## Reconciliation

Even with idempotency and sagas, distributed systems can drift from external truth (a card network outage, a webhook silently lost). A nightly batch job sums all `COMPLETED` transactions internally and compares the total against the bank's settlement report for the same period. Any mismatch is flagged for manual investigation rather than silently trusted — this is the system's last line of defense, independent of all the real-time correctness mechanisms above.

## PCI DSS: tokenization

Raw card numbers are never stored in your own database. On first use, the card is sent directly to a PCI-compliant vault (often the payment processor's own tokenization service), which returns an opaque token; your systems store and reference only that token going forward. This drastically shrinks the scope of what must be PCI-DSS audited, since the systems handling raw card data are isolated to the vault provider.

## What if the scale is 10×?

- PostgreSQL event log: partition by time range (e.g., monthly tables) so old, settled payments don't bloat hot indexes used by in-flight transaction lookups.
- Saga orchestrator: scale horizontally, partitioned by `payment_id` hash, so no single orchestrator instance is a bottleneck or single point of failure.
- Idempotency cache: shard Redis by idempotency-key hash; this scales linearly since idempotency checks are independent per key.

## Trade-offs

- **Saga pattern over distributed two-phase commit (2PC)**: chosen for availability and loose coupling across services (2PC requires all participants to be available and blocks on the slowest one) at the cost of eventual rather than immediate cross-system consistency, requiring well-designed compensating actions.
- **Event sourcing over simple status columns**: chosen for full auditability and replayability at the cost of more complex queries (you fold events to get current state, rather than reading one column) and higher storage volume.

## Interview follow-ups

**Q: "What if the compensating action itself fails (e.g., the refund call fails)?"**
A: Compensating actions must themselves be retried with their own idempotency guarantees, and if retries are exhausted, the payment moves to a `MANUAL_REVIEW` state rather than being silently dropped — financial systems should never fail silently; an unresolved case must surface to a human.

**Q: "Why event sourcing instead of just an audit log table alongside a normal status column?"**
A: They sound similar, but event sourcing makes the events the *single source of truth* (current state is derived, never stored independently), which eliminates an entire class of bugs where the status column and the audit log table disagree because they were updated by two separate writes that aren't atomic with each other.


---

# Chapter 10: Design 8 — Search Autocomplete

## Requirements

**Functional**: as a user types a search query character by character, return the top-10 most relevant suggestions for the current prefix, within 100ms.

**Non-functional**: 10M queries/day; results should ideally be personalized (or at least regionally relevant); must feel instant — every keystroke triggers a request, so latency budget is extremely tight.

## Estimation

```
Queries/sec (avg):  10,000,000 / 86,400 ≈ 116 queries/sec (avg)
                     Each *keystroke* triggers a request, so actual request volume
                     is several times the "search" count — a query of length 8
                     can generate up to 8 autocomplete requests if not debounced
                     client-side → design for ~500-1,000 req/sec realistically.
```

## Two implementation approaches

### 1. Trie

A trie (prefix tree) stores strings character-by-character, where each node represents one character and a path from root to node spells a prefix.

```
                root
               /    \
              c      t
             /        \
            a          o
           / \          \
          r   t          p
         /     \
       "car"  "cat"
       (each leaf/marked node stores
        the top-K completions + scores
        for that prefix, precomputed)
```
Lookup is O(length of prefix) to walk to the right node, then O(1) to read the precomputed top-K list stored there. The challenge is keeping per-node top-K lists updated as popularity shifts, and the memory cost of a trie over a huge vocabulary (mitigated by only storing top-K at each node rather than every completion).

### 2. Redis ZSET (sorted set) approach — simpler to operate

```
key:   "prefix:ca"
value: ZSET of (suggestion, score) pairs, score = search frequency

ZADD prefix:ca  15000 "california"
ZADD prefix:ca   8200 "car insurance"
ZADD prefix:ca   4100 "cat food"

ZREVRANGE prefix:ca 0 9    -- top 10 suggestions for prefix "ca", O(log N) per op
```
This is the approach used in this design: it reuses Redis's existing sorted-set primitive instead of building and maintaining a custom trie data structure, at the cost of one key per prefix (a 5-character search space across a large vocabulary produces a large but bounded number of prefix keys).

## Update pipeline

Suggestion rankings shouldn't be computed live per request — they're precomputed and refreshed periodically from real search behavior:

```
 Search events ──▶ Kafka ──▶ Hourly Spark job
                              (aggregate: count searches per
                               prefix → completed query, last 30 days
                               with recency weighting)
                                       │
                                       ▼
                              Bulk ZADD into Redis
                              (replaces/updates prefix:* keys)
```
Hourly batch (rather than real-time streaming) is an explicit choice here: autocomplete popularity shifts on the scale of hours/days, not seconds, so the freshness gained by streaming updates isn't worth the added system complexity.

## Architecture

```
 Client (keystroke) ──▶ ┌─────────────┐
                          │   CDN (edge)  │── caches top-1000 most common prefixes
                          └──────┬────────┘    (covers a large fraction of total
                                  │ miss         traffic, since query distribution
                                  ▼              is heavily skewed toward short,
                          ┌─────────────┐        common prefixes)
                          │  API Servers  │
                          └──────┬────────┘
                                  ▼
                          ┌─────────────┐
                          │ Redis ZSETs   │
                          │ prefix → top10│
                          └─────────────┘
```

## CDN caching of top-1000 prefixes

Search prefix popularity follows a heavy long tail — a small number of common prefixes ("a", "am", "ama"...) account for a disproportionate share of total autocomplete requests. Caching the top ~1,000 prefixes' results at the CDN edge serves a large fraction of total traffic without ever reaching the origin Redis layer, leaving Redis to handle only the long tail.

## What if the scale is 10×?

- 100M queries/day: shard Redis by prefix hash (consistent hashing) — ZSET operations are already O(log N) and cheap per-op, so the scaling lever is distributing *keys* across more nodes, not making individual lookups faster.
- Update pipeline: move from hourly Spark batch to a streaming aggregation (e.g., Kafka Streams with a sliding window) if popularity shifts fast enough (e.g., breaking-news-driven search spikes) that hourly refresh feels stale.
- Personalization: blend the global top-10 with a per-user recent-search list, merged client-side or via a lightweight per-user cache lookup added to the request path — kept as a thin addition so it doesn't compromise the sub-100ms budget.

## Trade-offs

- **Redis ZSET over a custom trie service**: chosen for operational simplicity (reusing a well-understood Redis primitive) at the cost of slightly less elegant prefix-sharing than a true trie (a trie can share computation across overlapping prefixes; a ZSET-per-prefix approach stores each prefix's top-K somewhat independently).
- **Hourly batch updates over real-time**: chosen for simplicity given autocomplete's naturally slow-moving popularity, at the cost of being unable to reflect a sudden trending-topic spike within the hour.

## Interview follow-ups

**Q: "How do you handle a brand-new, never-searched prefix (e.g., a just-announced product name)?"**
A: Fall back gracefully — if the Redis ZSET for a prefix is empty, return the next-shorter prefix's results filtered to those still matching, or fall back to a lightweight live query against a search index (Elasticsearch) for that specific case, accepting higher latency only on this cold-start path rather than on every request.

**Q: "How would you personalize without blowing the 100ms budget?"**
A: Keep personalization client-side where possible (cache the user's own recent searches in the app, merge locally with the global top-10 from the server) — this avoids adding a server-side per-user lookup to the critical path entirely for the common case.


---

# Chapter 11: Design 9 — BookMyShow

## Requirements

**Functional**: browse events/movies, view seat maps, select and book seats, handle high-concurrency flash sales (e.g., a hugely popular concert going on sale at a fixed time).

**Non-functional**: zero double-booking of the same seat under any concurrency; flash sales can see hundreds of thousands of users hitting "book" for a few thousand seats within seconds.

## Estimation

```
Example flash sale: 50,000 seats across a venue's events on sale at once,
                     500,000 concurrent users attempting to book within the
                     first 5 minutes of sale opening.
```
The core numbers here aren't throughput in the steady-state sense — they're **contention**: orders of magnitude more simultaneous *attempts* than available *seats*. The entire design exists to handle that contention correctly and fairly.

## The seat availability race condition

If two users both see seat A5 as "available" and both click "book" within milliseconds of each other, a naive check-then-write (`SELECT seat WHERE status='available'` then `UPDATE status='booked'`) lets both succeed — the classic race condition.

### Step 1: Redis hold (fast, short-lived reservation)

```
SET seat:show123:A5 "userId_789" EX 600 NX

NX  = only set if the key does not already exist (atomic check-and-set)
EX  = expire in 600 seconds (10-minute hold — long enough to complete payment,
      short enough that an abandoned cart releases the seat automatically)
```
If the `SET ... NX` succeeds, this user (and only this user) now holds seat A5 — Redis's single-threaded execution model makes this check-and-set atomic, closing the race condition that a separate "check then write" would have.

### Step 2: Database confirmation on payment

Once payment succeeds, the hold is converted into a permanent booking, with a final guard against any edge-case race using a row-level lock:

```sql
BEGIN;
SELECT * FROM seats WHERE show_id = 123 AND seat_id = 'A5' FOR UPDATE;
-- confirm status is still 'held' by this user (defense in depth, even though
-- the Redis hold should already guarantee this)
UPDATE seats SET status = 'booked', user_id = 789 WHERE show_id = 123 AND seat_id = 'A5';
COMMIT;
```
`SELECT ... FOR UPDATE` locks the row for the duration of the transaction, so even a concurrent process attempting to touch the same seat row blocks until this transaction commits — a second, database-level layer of protection beneath the Redis hold.

## Architecture

```
 Client (seat map) ──▶ ┌────────────────────┐
                          │   Booking API         │
                          └──────────┬─────────────┘
                                     │ SET seat:show:A5 NX EX 600
                                     ▼
                          ┌────────────────────┐
                          │  Redis (seat holds)   │
                          └──────────┬─────────────┘
                                     │ on payment success
                                     ▼
                          ┌────────────────────┐
                          │ PostgreSQL             │
                          │ (SELECT FOR UPDATE →   │
                          │  confirm booking)      │
                          └────────────────────┘

 Flash sale, high contention:

 Client ──▶ ┌──────────────────┐    ┌─────────────────┐
            │  Virtual Waiting    │──▶│  WebSocket          │── periodic queue-position
            │  Room               │    │  (position updates) │   updates while waiting
            └──────────────────┘    └─────────────────┘
                       │ admitted in controlled batches
                       ▼
            ┌──────────────────┐
            │  Booking API        │ (same flow as above)
            └──────────────────┘
```

## Flash sale architecture: virtual waiting room

Rather than letting 500,000 users hit the booking API simultaneously (which would overwhelm Redis/Postgres regardless of how well the hold mechanism is built), users are first placed in a **virtual waiting room** — a queue with a WebSocket connection that pushes periodic position updates ("You are #4,213 in line"). The system admits users into the actual booking flow in controlled batches matched to backend capacity, smoothing the request curve from a instantaneous spike into a manageable, steady stream — directly applying the message-queue back-pressure concept from Chapter 2 at the user-experience layer.

## What if the scale is 10×?

- 5M concurrent waiting-room users: shard the WebSocket layer (Chapter 6's connection-registry pattern applies directly — route each user to one of many waiting-room servers, broadcast position updates per-shard).
- Redis seat holds: shard by `show_id` (a single popular show's seats stay on one shard, keeping the `NX` atomicity guarantee intact within that shard, while spreading load across many concurrent shows).
- Increase admission-batch granularity (smaller, more frequent batches) so backend load stays smoother rather than admitting in large, bursty waves.

## Trade-offs

- **Redis hold + DB confirmation (two-phase) over DB-only locking**: chosen because a 10-minute hold via `SELECT FOR UPDATE` would hold a database row lock for the entire payment flow — unacceptable, since DB connections/locks are a scarce resource. Redis holds are cheap and naturally self-expiring; the DB lock is only held for the brief final confirmation transaction.
- **Virtual waiting room over direct request handling**: chosen to protect backend stability during extreme contention at the cost of added perceived friction for users (waiting in a queue rather than instant access) — an explicit, justified trade-off given that "instant access for everyone" against 10x more demand than supply isn't actually deliverable.

## Interview follow-ups

**Q: "What if a user closes their browser tab after holding a seat but before paying?"**
A: Nothing extra needs to happen — the `EX 600` TTL on the Redis hold expires automatically, releasing the seat for others without any manual cleanup job, which is exactly why a TTL-based hold (rather than a hold with no expiry, requiring an explicit release) was chosen.

**Q: "How do you keep the waiting-room queue fair (first-come, first-served) under high concurrency?"**
A: Assign each entrant a monotonically increasing position token at admission time (e.g., from a single atomic counter, or per-shard atomic counters with a global ordering hint), and admit strictly in token order — this avoids needing a centralized, contention-prone "queue" data structure while still preserving a deterministic ordering.


---

# Chapter 12: Design 10 — Feed Generation (Instagram/Twitter)

## Requirements

**Functional**: users create posts, follow other users, and view a personalized, reverse-chronological-or-ranked feed of posts from people they follow.

**Non-functional**: large-scale social graph (e.g., 300M DAU); some accounts ("celebrities") have tens of millions of followers, creating an extreme power-law skew in the follower-count distribution; feed loads must feel instant (sub-second).

## Estimation

```
Posts/sec (avg, illustrative): ~6,000 posts/sec at Twitter-like scale
Timeline reads/day:            ~200M+ (feed is opened far more often than posts are created —
                                 a classic read-heavy workload, similar in shape to Chapter 3's
                                 URL shortener but with a much harder "what do I show" problem)
```

## Fan-out on write

When a user posts, the system immediately computes and writes that post into the **precomputed feed** of every one of their followers.

```
User posts ──▶ ┌────────────────────┐
                 │  Fan-out Worker      │
                 └──────────┬─────────────┘
                            │ for each follower:
                            ▼
                 ┌────────────────────┐
                 │ Redis List per user   │   feed:user_42 → [post_991, post_988, post_975, ...]
                 │ (precomputed feed)    │
                 └────────────────────┘

Reading the feed: O(1) — just read the user's own precomputed Redis list.
```
**Pro**: reads are extremely cheap — O(1) list read, no computation at request time, which is exactly what you want given how read-heavy this workload is.
**Con**: a celebrity with 10M followers triggers **10M individual writes** for a single post — a massive write amplification that can take minutes to fully propagate and puts enormous load on the fan-out worker fleet for that one event.

## Fan-out on read

The alternative: don't precompute anything. When a user opens their feed, fetch the most recent posts from everyone they follow, merge, and rank on the spot.

```
User opens feed ──▶ ┌────────────────────┐
                      │  Feed Service         │
                      └──────────┬─────────────┘
                                 │ for each followed user (could be hundreds):
                                 │   fetch their recent posts
                                 ▼
                      ┌────────────────────┐
                      │  Merge + Rank          │── compute at request time
                      └────────────────────┘
```
**Pro**: no write amplification at all — posting is always O(1) regardless of follower count.
**Con**: reading is now expensive — fetching and merging posts from potentially hundreds of followed accounts on every feed load, which is exactly the workload that needs to be fast and cheap.

## Hybrid approach (the production answer)

```
                     ┌─────────────────────────────────────┐
                     │   On post: how many followers?         │
                     └───────┬─────────────────────┬──────────┘
                  < 1M followers (regular user)   ≥ 1M followers (celebrity)
                             │                              │
                             ▼                              ▼
                  Fan-out on write                  Skip fan-out — post is
                  (push to every follower's          NOT pushed to follower
                   precomputed Redis feed list)       feed lists

  Feed read (for any user):
    1. Read precomputed Redis feed list (covers everyone they follow who's a
       "regular" user — fast, O(1)).
    2. Separately fetch recent posts from the small set of celebrities they follow
       (most users follow only a handful of true celebrities — this list is short).
    3. Merge the two sources, rank, return.
```
This gives the best of both: the common case (regular users posting, which is the overwhelming majority of posts) gets cheap O(1) reads via fan-out-on-write, while the expensive case (celebrity posts) avoids 10M-write amplification by being fetched on read instead — and step 2's cost stays bounded because any individual user follows only a small number of celebrities, even if each celebrity has millions of followers.

## Architecture

```
 Post created ──▶ ┌─────────────┐
                    │  Post Service │──▶ PostgreSQL/Cassandra (durable post storage)
                    └──────┬────────┘
                           │ follower_count check
                           ▼
              ┌─────────────────────┐
              │   Fan-out decision     │
              └──┬──────────────────┬──┘
         regular │                  │ celebrity
                  ▼                  ▼
       ┌──────────────────┐   (no fan-out — read-time fetch instead)
       │  Fan-out Worker     │
       │  → Redis Lists       │
       │    (per-follower      │
       │     feed)             │
       └──────────────────┘

 Feed read ──▶ ┌─────────────┐    ┌──────────────────┐
                │ Feed Service  │──▶│ Redis (precomputed │
                └──────┬────────┘    │ feed list)          │
                       │             └──────────────────┘
                       │ + fetch followed celebrities' recent posts directly
                       ▼
              ┌─────────────────┐
              │  Merge + Rank      │──▶ returned to client
              └─────────────────┘
```

## What if the scale is 10×?

- Fan-out workers: this is the component under the most pressure at 10x scale — partition the follower list itself (shard fan-out work across many workers by follower-ID range) so a single celebrity-adjacent post (just under the celebrity threshold, but still with millions of followers) doesn't bottleneck on one worker.
- Redis feed lists: shard by user_id; cap each user's stored feed list length (e.g., last 800 posts) and rely on the celebrity-merge step plus pagination for anything beyond that, bounding per-user memory regardless of how prolific the people they follow are.
- Consider lowering the celebrity threshold (e.g., from 1M to 100K followers) as overall scale grows, since write amplification at the threshold boundary grows with total user count too.

## Trade-offs

- **Hybrid fan-out over either pure strategy**: chosen specifically to avoid both failure modes (celebrity write storms on pure write-fan-out; expensive reads for everyone on pure read-fan-out), at the cost of added system complexity — two code paths to build, test, and operate instead of one.
- **Ranked vs strictly reverse-chronological feed**: a ranking step (engagement prediction, recency, affinity) generally improves engagement metrics at the cost of predictability for users and added ML infrastructure — this design treats ranking as a pluggable step after the merge, so it can start as simple reverse-chronological and evolve independently of the fan-out architecture.

## Interview follow-ups

**Q: "How do you decide the celebrity threshold, and what happens right at the boundary?"**
A: It's tuned empirically against fan-out worker capacity (pick the follower count above which write amplification meaningfully degrades worker fleet health) rather than a fixed number — and accounts near the boundary are typically given some hysteresis (don't flip strategies on every follower gained/lost) to avoid thrashing between fan-out modes.

**Q: "What if a user unfollows someone after that person's post was already fanned out to their feed?"**
A: The post already sitting in their precomputed Redis list isn't retroactively removed (that would require a reverse index of "which feeds contain this post," adding real complexity for a low-value cleanup); it's filtered at read/render time instead if the read path checks current follow status, or simply left to scroll out of relevance naturally as new posts push it down — a deliberate "good enough" trade-off rather than a strict consistency guarantee.


---

# Chapter 13: Design 11 — Distributed Job Scheduler

## Requirements

**Functional**: schedule one-time jobs ("run this at 3pm tomorrow") and recurring jobs ("run this every hour," cron-style); execute jobs at-least-once even across worker/scheduler failures.

**Non-functional**: no job should silently never run; no recurring job should run on two schedulers simultaneously and execute twice; the system must survive individual node crashes without manual intervention.

## Estimation

```
Example scale: 1,000,000 scheduled jobs total (mix of one-time and recurring),
               with up to ~10,000 jobs becoming due and executing per minute
               at peak (e.g., everyone's hourly cron jobs clustering near
               common times like the top of the hour).
```

## Leader election: only one active scheduler

If you naively run multiple scheduler instances for availability, each one might independently decide "job X is due" and fire it twice. The fix is **leader election** — only one scheduler instance is ever actively dispatching jobs at a time; the rest stand by as hot backups.

```
 Scheduler instances:  S1, S2, S3

 ZooKeeper ephemeral node: /scheduler/leader

 S1 ──create ephemeral node──▶ succeeds → S1 is leader, actively dispatches jobs
 S2 ──create ephemeral node──▶ fails (already exists) → S2 watches the node, stands by
 S3 ──create ephemeral node──▶ fails (already exists) → S3 watches the node, stands by

 If S1 crashes:
   → S1's session with ZooKeeper times out
   → its ephemeral node is automatically deleted
   → S2 and S3 are notified (they were watching), race to create the node again
   → one of them (say S2) succeeds → S2 becomes the new leader
```
ZooKeeper's **ephemeral node** primitive is what makes this safe: the node only exists while the creating client's session is alive, so a crashed leader's "lock" is released automatically — no manual cleanup, no risk of a permanently stuck lock from a dead process.

## Database-based locking for distributed workers

Once the leader decides a job is due, it needs to hand it to **one** worker out of a fleet, without two workers grabbing the same job. `SELECT FOR UPDATE SKIP LOCKED` is the standard primitive here:

```sql
-- Each worker polls with this query:
SELECT * FROM jobs
WHERE status = 'DUE' AND run_at <= NOW()
ORDER BY run_at
LIMIT 1
FOR UPDATE SKIP LOCKED;     -- skip rows already locked by another worker's
                            -- concurrent transaction, instead of blocking/waiting

UPDATE jobs SET status = 'RUNNING', worker_id = ? WHERE id = ?;
COMMIT;
```
`SKIP LOCKED` is what makes this scale to many concurrent workers polling the same table: instead of workers queuing up waiting for each other's locks (which would serialize job pickup), each worker simply skips past rows another worker already has locked and grabs the next available one — turning job distribution into a naturally parallel operation.

## Architecture

```
                  ┌─────────────────────┐
                  │  Scheduler (leader)    │── only one active at a time (ZooKeeper
                  │                        │   leader election, see above)
                  └──────────┬─────────────┘
                             │ marks jobs DUE when run_at <= now
                             ▼
                  ┌─────────────────────┐
                  │  PostgreSQL             │   jobs table: id, run_at, status,
                  │  (job table)            │   cron_expr (if recurring), payload
                  └──────────┬─────────────┘
                             │ SELECT FOR UPDATE SKIP LOCKED
                  ┌──────────┴───────────┬─────────────────┐
                  ▼                      ▼                  ▼
            ┌──────────┐          ┌──────────┐       ┌──────────┐
            │ Worker 1   │          │ Worker 2   │       │ Worker 3   │
            └─────┬─────┘          └─────┬─────┘       └─────┬─────┘
                  │ heartbeat while running                  │
                  ▼                                            ▼
            ┌─────────────────────────────────────────────────┐
            │   Heartbeat monitor — if a RUNNING job's worker     │
            │   stops heartbeating, mark job DUE again for retry  │
            └─────────────────────────────────────────────────┘
```

## Exactly-once execution challenge

The hardest case: a worker executes a job successfully, but crashes *after* execution but *before* it can mark the job `COMPLETED` in the database. From the system's point of view, this looks identical to "the worker crashed before doing anything" — it can't tell the difference.

```
Worker timeline:
  pick up job → RUNNING → [execute job] → ??? crash here ??? → mark COMPLETED

If it crashes before the COMPLETED write:
  → heartbeat monitor sees no recent heartbeat → times out
  → job is marked DUE again → another worker picks it up → executes AGAIN
```
This means the system can only honestly guarantee **at-least-once** execution, not exactly-once — and the resolution isn't to chase a perfect exactly-once guarantee (which is provably very hard in a distributed system with independent failures), but to **require job handlers to be idempotent**: e.g., a "charge $10" job should really be "ensure a $10 charge exists for idempotency-key X" (directly reusing the idempotency pattern from Chapter 9), so executing it twice produces the same end state as executing it once.

## What if the scale is 10×?

- 10M scheduled jobs, 100K/min becoming due at peak: a single PostgreSQL `jobs` table becomes a bottleneck for `SELECT FOR UPDATE SKIP LOCKED` polling at this volume — shard the jobs table (e.g., by job_id hash) across multiple database instances, with the leader scheduler dispatching to the correct shard.
- Worker fleet: scale horizontally (workers polling are stateless and independent by design) — this is the easy part of scaling this system.
- Consider moving from poll-based pickup to a push-based model (leader publishes due jobs to a Kafka topic, workers consume) once polling overhead itself becomes significant, trading some implementation simplicity for reduced database polling load.

## Trade-offs

- **At-least-once + idempotent handlers over chasing exactly-once**: chosen because true exactly-once execution across independent failure domains is not reliably achievable, while at-least-once + idempotency is both achievable and sufficient for nearly all real job types.
- **ZooKeeper leader election over a simpler single-scheduler-no-failover design**: chosen for availability (the system survives a scheduler crash without manual intervention) at the cost of operating an additional coordination service.

## Interview follow-ups

**Q: "How do you handle a recurring job whose previous run is still executing when the next run is due?"**
A: This is a policy decision exposed per job: `SKIP` (don't run again until the current run finishes — the safe default for jobs that shouldn't overlap), `QUEUE` (let it run immediately after the current one finishes), or `PARALLEL` (allow concurrent runs — only safe for genuinely independent, idempotent jobs).

**Q: "How does the leader avoid re-scanning the entire jobs table every tick to find due jobs?"**
A: An index on `run_at` (and `status`) makes "find jobs due now" an efficient range scan rather than a full table scan — exactly the kind of indexing decision that turns a O(N) poll into something proportional to the (small) number of currently-due jobs, regardless of how large the total `jobs` table grows.


---

# Chapter 14: System Design Trade-offs

Every design in this book made explicit choices that traded one good property for another. This chapter collects the recurring dimensions so you can reason about *any* new design, not just the eleven covered here.

## SQL vs NoSQL: consistency vs flexibility vs scale

```
SQL (PostgreSQL/MySQL)              NoSQL (Cassandra/DynamoDB/Redis/Mongo)
─────────────────────               ──────────────────────────────────────
Strong consistency, ACID            Often eventual consistency by default
Joins, flexible ad-hoc queries      Query patterns must be designed up front
Vertical scaling has a ceiling      Horizontal scaling is the core design point
Best fit: payments (Ch.9),          Best fit: chat messages (Ch.6),
          booking confirmation       location data (Ch.7), feed lists (Ch.12)
          (Ch.11)
```
The decisive question isn't "which is better" — it's "does this data need transactional joins and strong consistency (→ SQL), or does it need to scale writes/reads past a single machine with a known, fixed access pattern (→ NoSQL)?" Most production systems use both, for different data, in the same overall architecture (e.g., Chapter 9 uses PostgreSQL for the payment ledger but would use Redis for the idempotency cache).

## Sync vs Async: latency vs resilience vs complexity

```
Synchronous                          Asynchronous (queue-mediated)
──────────────                       ──────────────────────────────
Caller waits for the full result     Caller enqueues and moves on
Simpler to reason about              Decouples producer/consumer failure domains
Slow downstream = slow caller        Slow downstream just grows the queue, doesn't
                                      block the caller
Best fit: redirect lookup (Ch.3),    Best fit: notification delivery (Ch.5),
          payment charge confirm      analytics events (Ch.3), feed fan-out (Ch.12)
          (Ch.9 — caller needs the
          result to proceed)
```
The rule of thumb: if the caller *needs the result to make its next decision* (did the charge succeed?), it has to be synchronous somewhere in the chain. If the caller just needs the *side effect to eventually happen* (send a push notification), async is almost always better — it isolates the caller from downstream latency and failures.

## Push vs Pull: simplicity vs freshness vs resource usage

```
Push                                 Pull
──────                               ──────
Source proactively sends updates     Consumer requests data when needed
Fresher data, lower latency          Simpler, consumer controls its own load
Wastes resources on uninterested     Can be stale between pulls
consumers; harder to scale fan-out   Best fit: search autocomplete refresh
Best fit: push notifications (Ch.5),  (hourly pull-style batch, Ch.10)
          WebSocket delivery (Ch.6)
```
Push wins when freshness/latency matters and you know exactly who needs the update (a specific recipient's chat message). Pull wins when the consumer's need is intermittent or unpredictable, or when proactively pushing to everyone would waste resources on recipients who don't need it right now.

## Consistency vs Availability (CAP, applied)

The CAP theorem says that under a network partition, you must choose between consistency (every read sees the latest write) and availability (every request gets a response, even if possibly stale). In practice, this isn't an abstract choice — it's visible directly in the designs above:

```
Chose Consistency (CP):                    Chose Availability (AP):
  Payment system (Ch.9) — a stale            Feed generation (Ch.12) — a feed
  read on "did this charge succeed"           that's a few seconds stale is
  could cause a double-charge or a            completely fine; refusing to
  missed charge. Unacceptable.                load the feed at all is not.

  Seat booking confirmation (Ch.11) —         Driver location (Ch.7) — slightly
  SELECT FOR UPDATE explicitly                stale location data is fine; it
  sacrifices availability (the row            self-corrects on the next 4-second
  is locked, blocking other writers)          update. Refusing to serve nearby-
  to guarantee no double-booking.             driver queries is not.
```
Every design in this book picked a side for *each piece of data it manages* — not once for the whole system. A single application (e.g., BookMyShow) is consistency-favoring for the seat-booking write path and availability-favoring for the "browse events" read path.

## Monolith vs Microservices: operational simplicity vs independent scaling

```
Monolith                             Microservices
───────────                          ─────────────────
One deployable unit                  Many independently deployable services
Simpler to develop, test, deploy     Each service can scale independently
                                      (e.g., Chapter 6's chat-server fleet scales
                                      separately from its connection-registry)
Scaling means scaling everything     Network calls between services add latency
together, even underused parts       and failure modes (timeouts, retries, partial
                                      failure handling) that a monolith doesn't have
Best for: smaller teams, early-      Best for: large systems with components that
stage products, simpler domains      have genuinely different scaling profiles
                                      (most of the designs in this book, at their
                                      stated scale, are implicitly microservices —
                                      e.g., Notification System's Channel Workers
                                      scale independently from its API layer)
```
The trade-off is operational: microservices buy independent scalability and team autonomy at the cost of distributed-systems complexity (network failures, eventual consistency between services, more moving parts to operate and monitor). Most of the large-scale designs in this book adopt a microservices-shaped architecture not out of dogma, but because their components (e.g., Chapter 5's Channel Workers vs Notification API) genuinely have different scaling needs that benefit from independent deployment.

## How to present trade-offs in interviews

A weak answer states one option as objectively correct. A strong answer:

1. **States the decision explicitly** — "I'm choosing eventual consistency here."
2. **Names what it costs** — "...which means a follower count might be a few seconds stale."
3. **Justifies it against the actual requirements** — "...which is acceptable because nothing in our non-functional requirements demanded real-time accuracy on that number, and the alternative (synchronous strong consistency) would add latency to every single post."
4. **Acknowledges the alternative would also be defensible** — "If this were a financial balance instead of a follower count, I'd make the opposite choice."

This four-part structure — decision, cost, justification against requirements, acknowledgment of the alternative — is what separates a candidate who *understands* trade-offs from one who's memorized a list of technologies. Every deep-dive and trade-offs section in this book follows exactly this structure; internalizing the pattern is more valuable than memorizing any single design.

```
──────────────────────────────────────────────────────────────────────────────
  HOW TO PRESENT TRADE-OFFS IN A SYSTEM DESIGN INTERVIEW
  The Formula That Interviewers Reward
──────────────────────────────────────────────────────────────────────────────

Interviewers penalize two failure modes equally:
  1. Making a design decision without acknowledging its trade-off
     → "I'm choosing Cassandra" (no reasoning, no trade-off)
  2. Endlessly listing trade-offs without making a decision
     → "Well, Cassandra has these pros... but PostgreSQL has these pros..."

The formula that demonstrates SDE-2 thinking:

  "I'm choosing [OPTION A] because [SPECIFIC REASON tied to the stated requirements].
   The trade-off is [SPECIFIC DOWNSIDE — not vague]. I'd mitigate that by [MITIGATION].
   [OPTION B] would be the right choice if [DIFFERENT REQUIREMENT] were the priority."

Key rules:
  - The reason must tie to a specific requirement you clarified at the start
  - The downside must be specific ("doesn't scale writes horizontally")
    not vague ("doesn't scale" or "has trade-offs")
  - The mitigation shows you can handle the downside in production
  - The "option B scenario" shows you understand both options, not just the one you chose

──────────────────────────────────────────────────────────────────────────────
  WORKED EXAMPLE 1: Database Choice
──────────────────────────────────────────────────────────────────────────────

Question: "How would you store order data in a high-traffic e-commerce system?"

POOR answer (no trade-off acknowledged):
  "I'd use PostgreSQL because it's relational and has ACID compliance."

POOR answer (no decision made):
  "PostgreSQL has ACID but doesn't scale horizontally. Cassandra scales
   horizontally but has eventual consistency. It depends on your requirements."

SDE-2 answer:
  "I'm choosing PostgreSQL for the orders and order_items tables because
   our requirements specified ACID compliance for payment transactions —
   we cannot afford to process a payment that creates an order without
   recording the order items, or vice versa. PostgreSQL's transactional
   guarantees make that impossible.

   The trade-off is that PostgreSQL's write throughput is limited to a
   single primary node. If we hit 10,000+ writes per second, we'd need
   to shard by user_id and add read replicas to handle the read traffic.

   I'd mitigate that by: first adding read replicas (they handle ~80%
   of our read traffic), then introducing a Redis cache layer for product
   catalog reads (reducing DB load further), and only considering sharding
   if we genuinely hit primary write capacity limits.

   Cassandra would be the right choice if our transaction volumes exceeded
   what sharded PostgreSQL could handle, AND if we could accept eventual
   consistency for order status updates — which is not the case here given
   the payment requirement."

──────────────────────────────────────────────────────────────────────────────
  WORKED EXAMPLE 2: Synchronous vs Asynchronous Processing
──────────────────────────────────────────────────────────────────────────────

Question: "After an order is placed, how would you send the confirmation email?"

POOR answer:
  "I'd send it synchronously in the same transaction as the order creation."

POOR answer:
  "It depends. Sync is simpler but slower. Async is faster but more complex."

SDE-2 answer:
  "I'm making the email asynchronous — decoupled from the order creation
   transaction via a Kafka event. The order creation commits to PostgreSQL
   and publishes an OrderCreated event to Kafka. The notification service
   consumes that event and sends the email.

   The reason: email delivery can take 100–500ms (SMTP server latency).
   If I include that in the order creation response, every customer waits
   an extra 500ms for checkout confirmation. That's a poor user experience
   at scale.

   The trade-off is eventual consistency: the customer might receive the
   confirmation email 2–3 seconds after the order appears in their account,
   not simultaneously. For email, that's completely acceptable.

   I'd mitigate the risk of lost events by: using a Kafka Dead Letter Queue
   for emails that fail after 3 retries, and adding idempotency (track
   order_id in the notification service to prevent duplicate emails if the
   event is replayed).

   Synchronous would be the right choice if the email had to be sent as
   part of the order confirmation itself — for example, if the email
   contained a one-time payment link that the customer needed immediately
   and we couldn't surface in the UI."

──────────────────────────────────────────────────────────────────────────────
  WORKED EXAMPLE 3: Fan-Out Strategy for News Feed
──────────────────────────────────────────────────────────────────────────────

Question: "How would you design the news feed for a social platform?"

POOR answer:
  "I'd use fan-out on write — pre-compute each user's feed when someone posts."

POOR answer:
  "Fan-out on write is fast to read but slow to write. Fan-out on read is
   slow to read but fast to write. There are trade-offs to both."

SDE-2 answer:
  "I'm using a hybrid approach. For users with fewer than 10,000 followers,
   fan-out on write: when they post, we immediately push the post ID to each
   follower's feed cache (Redis sorted set scored by timestamp). Their followers
   get O(1) feed reads.

   For users with 10,000+ followers — celebrities and influencers — fan-out
   on read: their posts are not pre-distributed. Instead, when a follower
   fetches their feed, we merge the cached fan-out feed with a live query
   for any followed celebrity posts.

   The trade-off of fan-out on write for regular users: the write amplification.
   If a user has 5,000 followers and posts, we write to 5,000 Redis sorted
   sets. At 1,000 posts/second platform-wide, that's 5 million Redis writes/sec.
   We handle that by batching the fan-out via Kafka consumers.

   The trade-off of fan-out on read for celebrities: slightly slower feed
   reads because we merge two data sources. We mitigate this by caching the
   celebrity post list with a short TTL (60 seconds).

   Pure fan-out on write would be the right choice if we had no celebrities
   (all users have roughly equal follower counts) — it simplifies the read
   path significantly. Pure fan-out on read would be right if write throughput
   were more critical than read latency."

──────────────────────────────────────────────────────────────────────────────
  THE THREE THINGS TO ALWAYS MENTION
──────────────────────────────────────────────────────────────────────────────

  1. Your decision — stated decisively, not hedged
     NOT: "I might go with PostgreSQL, or maybe Cassandra..."
     YES: "I'm choosing PostgreSQL because..."

  2. The specific downside — named precisely
     NOT: "It doesn't scale as well"
     YES: "Its write throughput is limited to a single primary node"

  3. Your mitigation — what you'd do about the downside in production
     NOT: "We'd deal with that later"
     YES: "I'd mitigate that first with read replicas, then sharding..."

When you present trade-offs this way, interviewers write "strong hire"
in their notes because you're thinking like an engineer who has built and
operated production systems — not like a student who has only read about them.
```

---

*End of book.*
