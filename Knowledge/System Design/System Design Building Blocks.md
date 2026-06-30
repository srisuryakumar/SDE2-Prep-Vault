---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 2 — Design Building Blocks"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [hld, building-blocks, load-balancer, cache, queues, database]
---

# System Design Building Blocks

## Load Balancing
- **L4 (Transport Layer):** Operates on IP/port. Faster, no payload inspection. High throughput.
- **L7 (Application Layer):** Operates on HTTP headers, URLs. Slower, but enables smart routing (e.g. `/api/v1/` vs `/static/`).
- **Consistent Hashing:** Maps servers and keys on a hash ring. Only `1/N` keys remap when a server is added/removed. Standard solution for sticky sessions and cache sharding.

## Caching
Trades freshness for speed. Layers: Client → CDN → API Gateway → App Cache (Redis) → DB Buffer Pool.
- **Cache-aside (Lazy Loading):** App checks cache → miss → reads DB → writes to cache.
- **Write-through:** Write to cache and DB synchronously. Fresh, but slow writes.
- **Write-back:** Write to cache, flush to DB asynchronously. Fast writes, risk of data loss on crash.

## CDN (Content Delivery Network)
Globally distributed edge servers caching content close to users (reduces 150ms cross-continent to 10-40ms).
- **Push CDN:** Proactively upload to edge (good for known content).
- **Pull CDN:** Edge fetches from origin on cache miss (good for unpredictable traffic).

## Message Queues
Decouples producers from consumers in time and failure domain.
- **Async decoupling:** Producer doesn't wait for consumer.
- **Fan-out:** One event triggers multiple independent consumer groups.
- **Back-pressure:** Absorbs bursts so downstream services don't crash.

## API Gateway
Single entry point handling cross-cutting concerns:
- Authentication (validates tokens)
- Rate limiting (quotas per user/IP)
- Routing (map external paths to internal microservices)
- SSL Termination (decrypt TLS once at the edge)

## Database Selection Guide
- **SQL (Postgres, MySQL):** Strong consistency, ACID guarantees, relationships.
- **NoSQL Key-Value (Redis, DynamoDB):** Simple lookups, O(1) access, extreme scale.
- **NoSQL Wide-Column (Cassandra):** Massive write throughput, time-ordered data.
- **Time-series (InfluxDB):** Metrics, sensor data.
- **Graph (Neo4j):** Relationship-heavy queries (friends-of-friends).
- **Search (Elasticsearch):** Full-text/fuzzy search, relevance ranking.
