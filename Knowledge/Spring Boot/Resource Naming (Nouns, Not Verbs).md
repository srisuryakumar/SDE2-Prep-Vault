---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 2 — REST API Design Principles"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [rest, api-design, naming]
---

# Resource Naming (Nouns, Not Verbs)

## Intuition
A URL identifies a **resource** (a noun) and the HTTP method describes the **action** on it (the verb). The URL should never need a verb of its own.

## Bad vs Good
```
Bad:   POST /createOrder
Bad:   POST /v1/orders/cancelOrder
Good:  POST /v1/orders                  (The verb is POST itself)
Good:  PATCH /v1/orders/9001            (The verb is PATCH)
```
A `PATCH` with a body of `{ "status": "CANCELLED" }` is the RESTful way to express "cancel this order". 

## Conventions
- **Plural, not singular:** `/v1/orders`, not `/v1/order`.
- **Hierarchy reflects ownership:** Nest resources when one cannot exist without the other (e.g. `/v1/orders/9001/items`). Keep it flat when they are just associated (e.g. `/v1/products/42`).
