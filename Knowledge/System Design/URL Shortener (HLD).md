---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 3 — Design 1 — URL Shortener"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Building Blocks"]
tags: [hld, case-study, url-shortener]
---

# HLD Case Study: URL Shortener

## Problem Overview
Design a system to shorten a long URL and redirect a short URL back to the long URL.
- **Scale:** 100M shortens/day, reads are 10x writes (1.2k writes/sec, 12k reads/sec).
- **Latency:** Reads must be very low latency (p99 < 100ms).
- **Storage:** ~90 TB over 5 years.

## Core Component: Short Code Generation
This is the heart of the interview. Three approaches:
1. **Hash-based (MD5/SHA-256 truncated):** Generates collisions. Requires retry loops. *Not recommended for production.*
2. **Auto-increment + Base62:** Unique by definition. But a single global DB sequence is a bottleneck.
3. **Distributed ID ranges (ZooKeeper/etcd) [Recommended]:** Each API server requests a *range* of IDs (e.g. 1-1,000) from ZooKeeper and hands them out locally. This removes per-request coordination.

## Architecture
1. **Redirect Flow:**
   Client -> Load Balancer -> API Server -> Redis Cache -> PostgreSQL.
2. **HTTP 302 vs 301:**
   Return **HTTP 302 (Found)**, not 301. A 301 is permanently cached by the browser, meaning repeat clicks bypass your server, ruining click analytics. A 302 ensures all clicks hit your server.
3. **Analytics:**
   Redirects emit click events to Kafka asynchronously. A Flink/Spark stream aggregator rolls them up into a Time-Series DB.

## Handling 10x Scale
- **Database:** Shard PostgreSQL by `short_code` hash using Consistent Hashing.
- **Cache:** Use a Redis Cluster (to scale memory capacity, not just throughput).
- **ID Generation:** Increase the range size from ZooKeeper (e.g. 1,000 -> 10,000).

## Common Questions
**Q: How to prevent enumeration of short URLs?**
A: Shuffle the bit pattern of the ID before Base62-encoding it (e.g., Feistel cipher) so consecutive IDs don't look consecutive.
