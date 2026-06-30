---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 6 — Resource Management and Autoscaling"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: ["Kubernetes Resource Requests and Limits"]
tags: [kubernetes, resources, reliability]
---

# Kubernetes QoS Classes

## Intuition
When a node runs out of resources (memory pressure), the `kubelet` must evict pods to keep the node alive. It decides *which* pods to evict first based on their automatically assigned Quality of Service (QoS) class.

## The Three Classes
1. **Guaranteed:** Every container in the pod has `requests` perfectly equal to `limits` (for both CPU and memory). Evicted **last** (most protected).
2. **Burstable:** At least one container has requests/limits set, but they are not all equal. Evicted before Guaranteed, but after BestEffort.
3. **BestEffort:** **No** requests or limits set on any container. Evicted **first** without warning. *Never use this in production.*
