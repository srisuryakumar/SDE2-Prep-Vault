---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 9 — Observability"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Prometheus Metrics and PromQL"]
tags: [observability, logging, loki, grafana]
---

# Grafana and Loki

## Intuition
Grafana is a visualization layer that renders metrics and logs from backends. **Loki** is a log aggregation system heavily optimized to work alongside Prometheus.

## The Loki Difference
Unlike Elasticsearch (which full-text indexes every word in every log line), Loki **only indexes the labels** (the metadata, like `app=order-service`, `namespace=production`), leaving the log text unindexed. 
This makes Loki incredibly cheap to run at scale. Because it uses the exact same labeling system as Prometheus, you can easily pivot in a Grafana dashboard from a metric spike on a specific pod to the logs for that exact pod in the same time window.
