---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 3 — Kubernetes Architecture"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["The Reconciliation Loop (Kubernetes)"]
tags: [kubernetes, architecture, control-plane]
---

# Kubernetes Controller Manager

## Intuition
The `kube-controller-manager` runs dozens of **reconciliation loops** bundled into one process. Each loop is responsible for managing one type of resource by constantly matching the actual state to the desired state.

## Examples
- **ReplicaSet Controller:** Compares desired replicas to actual running pods. If actual < desired (due to a crash), it creates pods. If actual > desired, it deletes them.
- **Node Controller:** Watches for node heartbeats. If a node stops responding, it eventually marks the node `NotReady` and evicts its pods so they can be rescheduled elsewhere.
