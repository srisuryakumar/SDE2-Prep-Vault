---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 9 — Observability"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Observability Pillars (Metrics, Logs, Traces)"]
tags: [observability, tracing]
---

# OpenTelemetry and Distributed Tracing

## Intuition
When a user request touches 5 different microservices, debugging a failure requires seeing the entire request path. **Distributed tracing** captures this path as a tree of **spans** (units of work).

## Trace Context Propagation
When `Service A` calls `Service B`, it passes a `trace_id` in the HTTP headers (e.g., `traceparent`). `Service B` extracts that ID, creates its own child span, and passes the same ID along to `Service C`. 
This allows tracing backends (like Jaeger or Tempo) to reconstruct the entire request graph.

## OpenTelemetry (OTel)
Historically, metrics, logs, and traces used fragmented libraries. OpenTelemetry is a vendor-neutral standard that unifies all three pillars. It ensures that the same `trace_id` is automatically attached to every log line and metric exemplar, enabling seamless correlation across observability tools.
