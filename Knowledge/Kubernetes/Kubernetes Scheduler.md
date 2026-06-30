---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 3 — Kubernetes Architecture"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kubernetes Pods"]
tags: [kubernetes, architecture, scheduling]
---

# Kubernetes Scheduler

## Intuition
When a new Pod is created without a node assigned, the `kube-scheduler` decides where it should run. The scheduler does not start the container (that's the kubelet's job); it simply *binds* the pod to a node by writing the decision back to the API Server.

## Two-Phase Process
1. **Filter:** Eliminates nodes that *cannot* run the pod. Examples: not enough unallocated CPU/RAM, node taints the pod doesn't tolerate, port conflicts, or unmet node affinity rules.
2. **Score:** Ranks the surviving nodes to find the *best* fit. Examples of scoring plugins:
   - `LeastAllocated`: Prefers nodes with more free resources to spread load evenly.
   - `ImageLocality`: Prefers nodes that have already pulled the container image.
