---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 3 — Kubernetes Architecture"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kubernetes etcd (Single Source of Truth)"]
tags: [kubernetes, architecture, control-plane]
---

# Kubernetes API Server

## Intuition
The API Server (`kube-apiserver`) is the **single entry point** to the entire Kubernetes cluster. Every interaction (from `kubectl`, the Scheduler, the Kubelet, or Controllers) happens by calling its REST API. Nothing in Kubernetes talks directly to `etcd` except the API Server.

## Request Flow
When a request arrives, the API Server processes it through four stages:
1. **Authentication:** Identifies who is making the request (e.g., client certs, bearer tokens).
2. **Authorization:** Checks if the identity is allowed to perform the action (typically using RBAC).
3. **Admission Controllers:** Plugins that **validate** the request (reject if it violates policy) or **mutate** it (inject defaults, like adding a sidecar container).
4. **Persistence:** Writes the validated, mutated object to `etcd`.

Centralizing reads and writes allows consistent enforcement of security and policy across all actors.
