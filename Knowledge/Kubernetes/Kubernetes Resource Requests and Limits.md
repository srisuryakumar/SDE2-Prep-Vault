---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 6 — Resource Management and Autoscaling"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kubernetes QoS Classes", "Horizontal Pod Autoscaler (HPA)"]
tags: [kubernetes, resources, performance]
---

# Kubernetes Resource Requests and Limits

## Intuition
Every container should declare its CPU and memory needs. Failing to distinguish between requests and limits is a major source of production outages.

## Requests vs Limits
- **Requests:** "What the container is guaranteed to get." The Scheduler uses requests to find a node with enough *unallocated* capacity. It is a reservation, not a cap.
- **Limits:** "The hard ceiling the container can never exceed." 
  - **CPU Limits:** Exceeding CPU limits causes the kernel to **throttle** the container (slowing it down, causing latency spikes). It does not kill the container.
  - **Memory Limits:** Exceeding memory limits causes the kernel to immediately **OOMKill** (Out Of Memory Kill) the container. Memory is not compressible, so the process must be terminated and restarted.
