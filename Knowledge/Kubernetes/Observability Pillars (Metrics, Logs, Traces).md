---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 9 — Observability"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Prometheus Metrics and PromQL", "OpenTelemetry and Distributed Tracing", "Structured Logging and MDC"]
tags: [observability, monitoring, architecture]
---

# Observability Pillars (Metrics, Logs, Traces)

## Intuition
In a distributed microservice system, "which of our 200 pods is slow and why?" is impossible to answer without observability. It is built on three pillars:

## The Three Pillars
1. **Metrics:** Aggregated numbers over time (e.g., CPU saturation, request rate, P99 latency). Answers *"Is something wrong, and roughly where?"* Tool: Prometheus.
2. **Logs:** Discrete, structured JSON records of events. Answers *"What exactly happened, in detail?"* Tool: Loki / ELK.
3. **Traces:** A span-by-span breakdown of a single request's journey across multiple services. Answers *"Where did this request spend its time?"* Tool: OpenTelemetry, Jaeger.

True observability requires linking all three via a shared `trace_id`.
