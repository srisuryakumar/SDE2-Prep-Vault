---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 4 — Kubernetes Objects"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["kubelet (Node Agent)"]
tags: [kubernetes, reliability, architecture]
---

# Kubernetes Probes (Liveness vs Readiness vs Startup)

## Intuition
Probes are how the `kubelet` determines if a container is actually working, enabling self-healing and zero-downtime routing.

## Probe Types
- **`livenessProbe`:** Asks "Is the container alive?" If it fails, the kubelet **kills and restarts** the container. Use for deadlocks.
- **`readinessProbe`:** Asks "Is the container ready to receive traffic *right now*?" If it fails, the pod is **removed from the Service endpoints** (no traffic is routed to it), but it is NOT restarted. Use for temporary overload or initialization.
- **`startupProbe`:** Asks "Has this slow-starting app finished booting?" Liveness and readiness probes are disabled until this succeeds. It provides a long grace period for startup without forcing you to relax your liveness timeouts.
