---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 5 — Networking"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kubernetes Services (ClusterIP vs NodePort vs LoadBalancer)"]
tags: [kubernetes, networking, routing, tls]
---

# Kubernetes Ingress

## Intuition
Creating a `LoadBalancer` Service for every single API is expensive (you pay for one cloud LB per Service) and a management nightmare (TLS certs everywhere).
**Ingress** puts *one* cloud load balancer in front of the cluster, routing incoming requests to different internal Services based on **hostname** (`api.example.com` vs `admin.example.com`) or **URL path** (`/orders` vs `/payments`).

## How it works
The `Ingress` object is just a configuration rule. It requires an **Ingress Controller** (e.g., Nginx, Traefik) running as pods in the cluster to actually parse the HTTP requests and execute the routing.

## TLS Termination
Ingress is often paired with `cert-manager`, which watches for annotations, performs Let's Encrypt domain validation, provisions a TLS certificate, and automatically renews it—providing fully hands-off HTTPS for all routed domains.
