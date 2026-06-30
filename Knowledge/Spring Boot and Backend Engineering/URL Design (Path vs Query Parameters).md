---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 2 — REST API Design Principles"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [rest, api-design, url]
---

# URL Design (Path vs Query Parameters)

## Intuition
Consider these two URLs:
```
RESTful:      GET /v1/users/123/orders
Not RESTful:  GET /v1/getUserOrders?userId=123
```
The second is an RPC (Remote Procedure Call) disguised as REST. It uses an action name and places the identity of the resource in the query string.

## The Rule
- **Path Parameter:** Use it if a value identifies *which* resource (or sub-collection) you mean. (e.g. `123` in `/users/123/orders` identifies whose orders).
- **Query Parameter:** Use it if a value filters, sorts, or paginates *within* an already-identified resource. (e.g. `?status=SHIPPED` in `/users/123/orders?status=SHIPPED`).

Conflating the two works technically, but destroys the structural predictability of REST.
