---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 3 — Kubernetes Architecture"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kubernetes Probes (Liveness vs Readiness vs Startup)"]
tags: [kubernetes, architecture, worker-node]
---

# kubelet (Node Agent)

## Intuition
The `kubelet` is the **node agent** running on every worker (and control plane) node. It acts as the bridge between the API Server and the node itself.

## Responsibilities
- Watches the API Server for Pods assigned to its node.
- Tells the container runtime (e.g., `containerd`) to pull images and start/stop containers.
- Continuously runs liveness, readiness, and startup **probes** defined on the pod, and takes action (e.g., restarting a failed container).
- Reports node and pod status back to the API Server.
