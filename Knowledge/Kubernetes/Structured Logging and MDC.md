---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 9 — Observability"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["OpenTelemetry and Distributed Tracing"]
tags: [observability, logging]
---

# Structured Logging and MDC

## Intuition
Plain text log lines (`[ERROR] Timeout for user 123`) are useless at scale because you can't reliably filter or parse them across thousands of pods. **Structured logging** emits logs as machine-parseable JSON objects.

## MDC (Mapped Diagnostic Context)
When processing a request, you extract the `trace_id` from the incoming headers and store it in the **MDC** (a thread-local map provided by logging frameworks like SLF4J/Logback).
Once in the MDC, the logging framework automatically injects the `trace_id` into *every single log line* emitted during that request. 

**The Payoff:** When you see a single error log, you can query your log aggregator for that `trace_id` and instantly retrieve every log line, across every microservice, associated with that exact user request.
