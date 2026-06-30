---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 1 — The System Design Framework"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [hld, framework, estimation]
---

# The System Design Framework

## The 5-Step Framework
Every system design interview should follow this exact sequence:
1. **Requirements** (What to build) — Separate functional from non-functional.
2. **Estimation** (How big is it) — Convert requirements into numbers (requests/sec, storage/year).
3. **High-Level Design** (Boxes and arrows) — Draw the end-to-end architecture.
4. **Deep Dive** (The hard part) — Drill into 1-2 core components.
5. **Trade-offs** (What did we give up) — State the costs of your decisions (e.g. eventual vs strong consistency).

## Functional vs Non-Functional Requirements
- **Functional:** What the user can do (e.g. "Users can shorten a URL and get redirected"). Defines your APIs.
- **Non-Functional:** How well it must perform (e.g. "100M shortens/day, p99 latency < 100ms"). **This dictates the architecture.**

## Back-of-the-Envelope Estimation

### Latency Hierarchy (Orders of Magnitude)
- **L1 cache / Branch mispredict / L2 cache / Mutex:** Nanoseconds (0.5ns - 25ns)
- **Main memory (RAM):** 100ns
- **Read 1 MB sequentially from RAM:** 250µs
- **Same-datacenter round trip:** 500µs (0.5ms)
- **Read 1 MB sequentially from SSD:** 1ms
- **Disk seek (HDD):** 10ms
- **Cross-continent round trip:** ~150ms

*Takeaways:* Memory is ~100k times faster than a disk seek. Regional deployments exist because cross-continent is 300x slower than same-datacenter.

### Throughput Estimates
- **SQL (Writes):** ~1,000–5,000 writes/sec
- **SQL (Reads):** ~5,000–10,000 reads/sec
- **Redis (Single Instance):** ~100,000+ ops/sec
- **Application Server (Typical REST):** ~1,000–5,000 req/sec

### Storage Calculation
`Storage = (avg row size) × (entities per day) × (retention in days)`
*Example:* 500 bytes × 100M/day = 50 GB/day. Over 5 years (1825 days) = ~90 TB.
