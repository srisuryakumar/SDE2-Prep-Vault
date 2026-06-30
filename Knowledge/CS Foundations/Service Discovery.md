---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, architecture, microservices]
---

# Service Discovery

In a microservices environment, services scale up and down, and pods are ephemeral, meaning IP addresses change constantly. Service discovery solves the problem of how Service A finds the current IP of Service B.

## DNS-Based Discovery (Kubernetes)
Kubernetes assigns each logical service a stable virtual IP (ClusterIP) and a stable DNS record (e.g., `payment-service.default.svc.cluster.local`). 
- Service A just sends HTTP requests to `http://payment-service:8080`.
- Kubernetes CoreDNS resolves the name to the ClusterIP.
- Kubernetes kube-proxy routes the traffic to one of the healthy, underlying pods.

## Service Registry (Consul, Eureka)
Used in non-Kubernetes setups (like classic Spring Cloud).
- Each service instance registers its dynamic IP/port with a central registry (Eureka) when it starts.
- When Service A wants to call Service B, it asks the registry for a list of Service B's healthy IPs, and then performs client-side load balancing to pick one.
