---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 5 — Networking"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kubernetes CNI (Container Network Interface)"]
tags: [kubernetes, security, networking]
---

# Kubernetes NetworkPolicy

## Intuition
By default, Kubernetes networking is completely open: **every pod can talk to every other pod** across all namespaces. A compromised frontend pod can freely probe backend databases.

## The Standard Pattern
To secure a cluster, you define `NetworkPolicy` objects.
1. **Default Deny:** Apply a policy that selects all pods in a namespace and allows no ingress/egress.
2. **Explicit Allows:** Add specific policies to punch holes (e.g., "Allow `frontend` pods to reach `order-api` pods on port 3000").

## CNI Dependency
`NetworkPolicy` is just an API object. **It requires a compatible CNI plugin to actually enforce it.** Some plugins (like basic Flannel) will accept the policy in the API but silently fail to block traffic. You must use a CNI like Calico or Cilium for enforcement.
