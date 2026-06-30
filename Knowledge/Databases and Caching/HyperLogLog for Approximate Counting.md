---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 3 — Redis"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [redis, hyperloglog, analytics]
---

# HyperLogLog for Approximate Counting

## Intuition
**HyperLogLog** counts unique values with a fixed memory footprint of **12KB**, regardless of cardinality (whether it's 10 items or 10 billion items). 

## The Trade-off
It provides an **approximate count** with a standard error of ~0.81%.
For counting 10 million unique user IDs:
- A regular Redis SET would consume ~200MB of RAM.
- HyperLogLog consumes exactly 12KB (16,000x smaller).
- The count would be accurate to within ±81,000.

**When to use:** Perfect for analytics dashboards (e.g., daily unique visitors). Not acceptable for billing or exact counts (use a SET or `COUNT(DISTINCT)` instead).

## Commands
```bash
# Add elements (duplicates automatically handled)
PFADD daily:visitors:2024-01-15 "user:1" "user:2" "user:3" "user:1"

# Get count
PFCOUNT daily:visitors:2024-01-15   # Returns 3

# Merge multiple HyperLogLogs (e.g., weekly from daily)
PFMERGE weekly:visitors:2024-W03 \
    daily:visitors:2024-01-15 \
    daily:visitors:2024-01-16
PFCOUNT weekly:visitors:2024-W03
```
