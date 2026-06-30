---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 10 — Design 8 — Search Autocomplete"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [hld, case-study, search, redis, trie]
---

# HLD Case Study: Search Autocomplete

## Problem Overview
Return top-10 autocomplete suggestions as a user types, within 100ms.
- **Scale:** 10M queries/day. (Actual request volume is 500-1,000 req/sec since every keystroke triggers a request).
- **Latency constraint:** Must feel instant.

## Approaches
### 1. Trie (Prefix Tree)
Stores strings character-by-character. Lookup is O(prefix length) to find the node, then O(1) to read a precomputed top-K list stored at that node.
- *Pros:* Elegant, space-efficient for overlapping prefixes.
- *Cons:* Hard to keep top-K lists updated, complex to build a distributed trie.

### 2. Redis ZSET (Recommended)
Use Redis Sorted Sets (`ZSET`).
```
Key: "prefix:ca"
Value: ZSET of (suggestion, score)
ZADD prefix:ca 15000 "california"
ZREVRANGE prefix:ca 0 9
```
- *Pros:* Reuses a mature primitive (Redis). O(log N) per operation. Very simple to operate.

## Update Pipeline
Suggestion rankings are **not** computed live per request.
Search events go to Kafka -> Hourly Spark job aggregates counts (with recency weighting) -> Bulk updates Redis ZSETs.
*Why hourly?* Autocomplete popularity shifts on the scale of hours/days, not seconds.

## CDN Caching
Search prefix popularity has a heavy tail. A small number of very common prefixes ("a", "am", "ama") make up a huge chunk of traffic.
**Solution:** Cache the top 1,000 prefixes at the CDN edge. This serves a massive fraction of traffic without ever hitting your origin Redis.

## Common Questions
**Q: How do you personalize this without blowing the 100ms budget?**
A: Keep it client-side. Cache the user's recent searches locally on their device, and merge that list with the global top-10 returned by the server. This avoids adding a server-side DB lookup to the critical path.
