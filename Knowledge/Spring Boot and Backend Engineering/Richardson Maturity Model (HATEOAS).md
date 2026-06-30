---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 2 — REST API Design Principles"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [rest, hateoas, architecture]
---

# Richardson Maturity Model (HATEOAS)

## Intuition
Leonard Richardson proposed a 4-level scale to describe how "RESTful" an API is.

## The Levels
- **Level 0 (The Swamp of POX):** One URL, one method (`POST`), and the action is described in the body (RPC style). (e.g. SOAP).
- **Level 1 (Resources):** Multiple URLs exist (one per resource), but everything still uses `POST` with the action named inside the body.
- **Level 2 (HTTP Verbs):** Proper use of `GET`, `POST`, `PUT`, `DELETE`, and meaningful status codes. **This is where most production APIs live.**
- **Level 3 (HATEOAS):** Hypermedia as the Engine of Application State. Responses include `_links` describing what the client can do next, based on the resource's current state.

## HATEOAS Example
```json
{
  "id": 9001,
  "status": "PENDING",
  "_links": {
    "self":   { "href": "/v1/orders/9001" },
    "cancel": { "href": "/v1/orders/9001/cancel" }
  }
}
```
If the order was already `SHIPPED`, the `cancel` link would not be present.

## Interview Strategy
If asked "Is your API fully RESTful?", the strong answer is to name the level. "It's Level 2. We use proper resources and verbs, but we don't use HATEOAS because the added implementation complexity isn't justified for an internal B2B API where developers read the docs anyway."
