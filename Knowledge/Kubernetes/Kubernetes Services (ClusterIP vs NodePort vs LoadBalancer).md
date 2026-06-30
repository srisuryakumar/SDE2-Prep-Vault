---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 5 — Networking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["kube-proxy", "Kubernetes Ingress"]
tags: [kubernetes, networking, service-discovery]
---

# Kubernetes Services (ClusterIP vs NodePort vs LoadBalancer)

## Intuition
Because Pod IPs are ephemeral and change constantly (crashes, rollouts), connecting to them directly is brittle. A **Service** provides a single, stable virtual IP (and DNS name via CoreDNS) that routes traffic to a dynamic group of healthy Pods.

## Service Types
1. **ClusterIP (Default):** The Service is reachable *only* from inside the cluster. Used for 95% of internal microservice traffic.
2. **NodePort:** Exposes the Service on every node's physical IP at a fixed high port (30000–32767). Rarely used directly in prod.
3. **LoadBalancer:** Provisions a real, external cloud load balancer (e.g., AWS NLB) and points it at the Service. Used for external entry points.
4. **ExternalName:** A DNS CNAME record. Allows in-cluster code to address external resources (like managed RDS databases) using native Kubernetes DNS.
