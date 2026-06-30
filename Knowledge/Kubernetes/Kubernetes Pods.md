---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 4 — Kubernetes Objects"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Namespaces and cgroups"]
tags: [kubernetes, architecture, pods]
---

# Kubernetes Pods

## Intuition
A Pod is the smallest deployable unit in Kubernetes. It is *not* a container; it is a wrapper around one or more containers that are guaranteed to be co-located on the same node.

## Shared Resources
Containers within the same pod share:
- **Network Namespace:** They share a single IP address and can communicate with each other over `localhost`.
- **Volumes:** Storage volumes can be mounted into multiple containers within the pod.
- **Lifecycle:** They start and stop together.

## The Sidecar Pattern
Most production pods run multiple containers. The main container runs the application, while a **sidecar** container runs a helper process that needs to share the network or filesystem (e.g., an Envoy proxy for a service mesh, or a log-tailing agent).
