---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 9 — Spring Cloud Microservices"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [kubernetes, microservices, architecture]
---

# Kubernetes Service Discovery vs Eureka

## Intuition
Historically, Spring Cloud architectures used Eureka as a standalone Service Registry. Services would register themselves with Eureka, and clients would query Eureka to find the IP addresses of the services they wanted to call.

## The Modern Approach
When running on Kubernetes, Eureka is usually redundant. Kubernetes `Service` resources already provide native, DNS-based service discovery and load balancing. 
A call to `http://shipping-service` resolves via cluster DNS to a stable virtual IP that load-balances across all healthy pods backing that service. Therefore, you can skip deploying a standalone service registry when leveraging Kubernetes.
