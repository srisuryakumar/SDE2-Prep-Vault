---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 9 — Spring Cloud Microservices"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [distributed-systems, microservices, spring]
---

# API Gateway (Spring Cloud)

## Intuition
An API Gateway provides a single entry point that sits in front of all your microservices. 

## Benefits
1. **Single Address:** Clients only need to know one domain/IP instead of the specific addresses of 20 different microservices.
2. **Centralized Cross-Cutting Concerns:** Things like JWT validation, rate limiting, and CORS configuration can live in the gateway instead of being duplicated into every single service.

For example, the Gateway can validate a JWT token and forward the request downstream with a trusted `X-User-Id` header, saving downstream services from having to parse and validate the JWT themselves.
