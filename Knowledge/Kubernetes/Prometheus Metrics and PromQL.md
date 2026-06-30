---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 9 — Observability"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["The Four Golden Signals"]
tags: [observability, metrics, prometheus]
---

# Prometheus Metrics and PromQL

## Intuition
Prometheus is a **metrics** system that uses a pull-based model. It periodically **scrapes** a `/metrics` endpoint exposed by your applications, parses the time series data, and stores it.

## PromQL Basics
Metrics are identified by a name and key-value labels.
- `http_requests_total` is a raw counter. It is useless on its own because counters only go up.
- You must use `rate()` to get the per-second increase: `rate(http_requests_total[5m])`.

## Alerting
Prometheus evaluates alert rules. A crucial feature is the `for:` clause (e.g., `for: 5m`), meaning the condition must remain true for 5 consecutive minutes before firing. This prevents brief, self-resolving blips from waking up engineers.
