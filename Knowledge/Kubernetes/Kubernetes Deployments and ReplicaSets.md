---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 4 — Kubernetes Objects"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["The Reconciliation Loop (Kubernetes)"]
tags: [kubernetes, architecture, deployments]
---

# Kubernetes Deployments and ReplicaSets

## Intuition
A **Deployment** is the standard way to run stateless, replicated, long-lived workloads. It does not manage Pods directly; it manages **ReplicaSets**, which in turn manage Pods.

## Rolling Updates and ReplicaSets
When you update a Deployment's pod template (e.g., deploying a new image version), the Deployment creates a *new* ReplicaSet. It then orchestrates a rolling update, gradually scaling up the new ReplicaSet while scaling down the old one. 
If you need to rollback, the old ReplicaSet still exists (scaled to 0), providing a clean, instant rollback target.

## Configuration
- **`maxSurge`:** How many EXTRA pods (above the desired count) are allowed during a rollout.
- **`maxUnavailable`:** How many pods are allowed to be UNAVAILABLE during a rollout. Setting this to 0 ensures capacity never drops below the desired replica count.

*Note: Safe rolling updates require a properly configured `readinessProbe`, so the Deployment knows exactly when a new pod is ready to take traffic before terminating an old one.*
