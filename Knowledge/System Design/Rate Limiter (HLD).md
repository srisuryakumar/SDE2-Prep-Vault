---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 4 — Design 2 — Rate Limiter"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Building Blocks"]
tags: [hld, case-study, rate-limiter, redis]
---

# HLD Case Study: Rate Limiter

## Problem Overview
Limit the number of requests a client can make in a given time window, and reject requests beyond that limit with HTTP 429. Must add minimal latency and work across a distributed fleet.

## Algorithms
1. **Fixed Window:** Simple but suffers from boundary bursts (2x traffic at window edges).
2. **Sliding Window Log:** Stores every timestamp. Perfectly accurate but O(N) memory.
3. **Sliding Window Counter [Recommended Default]:** Weighted average of current + previous fixed window. Smooths boundary bursts cheaply.
4. **Token Bucket:** Allows controlled bursts (e.g. catching up after a network blip).
5. **Leaky Bucket:** Smooths traffic into a constant rate (queues requests).

## The Concurrency Problem
A naive "GET count, check, INCR" across distributed gateway nodes causes race conditions.
**Solution:** Use a **Redis Lua script**. Lua scripts execute atomically in Redis, guaranteeing check-and-increment happens without interleaving.

## Architecture
Usually implemented at the **API Gateway (Centralized)**.
Client -> API Gateway -> calls Redis Lua Script -> allows/rejects -> App Servers.

## Handling 10x Scale
At millions of distinct users, a single Redis node isn't enough memory.
- Shard Redis by `hash(user_id)`.
- If Redis throughput is an issue, move to a **local in-memory approximate counter** at each gateway node that syncs to Redis every ~100ms. Trades perfect accuracy for fewer round trips (rate limiting is a soft guarantee anyway).

## Common Questions
**Q: What happens if Redis goes down?**
A: Fail open (allow traffic) or fail closed (reject traffic) is a product decision. Most production systems **fail open** for short blips to avoid turning a Redis outage into a full site outage.
