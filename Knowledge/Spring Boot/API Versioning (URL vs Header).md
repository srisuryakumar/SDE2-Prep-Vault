---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 2 — REST API Design Principles"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [rest, api-design, versioning]
---

# API Versioning (URL vs Header)

## Intuition
APIs evolve. Versioning lets you make changes without breaking existing clients. There are two dominant approaches.

## 1. URL Versioning
e.g. `/v1/orders` and `/v2/orders`.
- **Pros:** Impossible to miss. Easy to read in logs, browser address bars, and `curl` commands. Trivial to route at the infrastructure layer (e.g. load balancer routes `/v1/*` to one cluster and `/v2/*` to another).
- **Cons:** Conflates the resource's identity with its representation. Every endpoint needs to be touched for a version bump.

## 2. Header Versioning
e.g. `GET /orders/9001` with header `X-API-Version: 2` or `Accept: application/vnd.api.v2+json`.
- **Pros:** Keeps the URL "pure"—it always identifies the same resource regardless of version.
- **Cons:** Invisible in the URL (harder to share links or read logs). Harder to route at the infrastructure layer. Easy for clients to forget the header and accidentally hit the wrong version.

## Which to choose?
In practice, URL versioning wins in the majority of real-world APIs (like Stripe and GitHub) because of its operational simplicity. In an interview, argue both sides and explain that "it depends on your operational priorities".
