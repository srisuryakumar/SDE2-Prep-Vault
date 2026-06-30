---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 5 — Networking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kubernetes NetworkPolicy"]
tags: [kubernetes, networking, cni]
---

# Kubernetes CNI (Container Network Interface)

## Intuition
Kubernetes itself does not implement pod networking. It defines a "flat network" contract and delegates the implementation to a pluggable **CNI (Container Network Interface)** like Calico, Flannel, or Cilium.

## The Flat Network Contract (3 Rules)
1. Every pod gets its own unique IP address.
2. **No NAT for pod-to-pod:** A pod on Node A can send a packet to a pod on Node B directly. The destination pod receives the packet with the *original sender's IP intact* (no NAT hiding the source).
3. Nodes can reach all pods (and vice versa) without NAT.

## Why "No NAT" matters
Because the real source IP is preserved end-to-end, network policies and access logs can identify exactly *which* pod sent a request. In traditional NAT architectures, the source IP gets obscured by the host's IP, making granular security impossible.
