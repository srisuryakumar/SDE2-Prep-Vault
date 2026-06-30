---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 9 — Observability"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Prometheus Metrics and PromQL"]
tags: [observability, metrics, sre]
---

# The Four Golden Signals

## Intuition
Every service-level dashboard should answer these four questions (popularized by Google SRE) before anything else.

## The Signals
1. **Request Rate (Traffic):** Throughput. How much demand is being placed on the service?
2. **Error Rate:** What fraction of requests are failing (e.g., HTTP 5xx responses)?
3. **Latency:** How long do requests take? Crucially, measure the **P99** (99th percentile), not just the average. An average hides severe delays experienced by a minority of users.
4. **Saturation:** How "full" is your service? (e.g., CPU usage relative to limits, connection pool utilization, memory).

These signals tell you if the user experience is currently degraded.
