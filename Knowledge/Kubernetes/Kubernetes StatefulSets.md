---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 4 — Kubernetes Objects"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kubernetes Deployments and ReplicaSets"]
tags: [kubernetes, architecture, state]
---

# Kubernetes StatefulSets

## Intuition
A Deployment's pods are interchangeable and randomly named. This breaks for stateful systems (like databases) where replica identity matters. 
A **StatefulSet** provides three guarantees that Deployments do not:

## Guarantees
1. **Stable Pod Identity:** Pods are named sequentially (`postgres-0`, `postgres-1`). If a pod restarts, it comes back with the exact same name and ordinal.
2. **Stable Network Identity:** Each pod gets its own stable DNS name (e.g., `postgres-0.postgres.default.svc.cluster.local`), allowing you to route traffic to a *specific* replica.
3. **Stable Storage:** Each pod gets its own dedicated `PersistentVolumeClaim`. If the pod is rescheduled, that exact volume is re-attached to it. The data follows the pod.

**Use cases:** Databases (PostgreSQL, MySQL, MongoDB), message brokers (Kafka, ZooKeeper), and search indexes (Elasticsearch).
