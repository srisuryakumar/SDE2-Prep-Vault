---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 1 — The HTTP Protocol"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [http, headers, networking]
---

# HTTP Headers

## Intuition
Headers are how a request or response carries metadata that the body shouldn't have to contain.

## Important Headers
- **`Content-Type`**: Describes the format of the *body that follows it* (e.g. `application/json`). Spring's `HttpMessageConverter` uses this to decide how to deserialize an incoming `@RequestBody`.
- **`Accept`**: Tells the server what format(s) the *client* is willing to receive back. (e.g., `Accept: application/xml`). Note: A request can have `Content-Type: application/json` but `Accept: application/xml`.
- **`Authorization`**: Carries credentials. `Bearer <token>` for JWTs, `Basic <base64-encoded-user:pass>` for HTTP Basic Auth. (Basic is base64 *encoded*, not encrypted—only safe over TLS).
- **`Cache-Control`**: Governs caching. `no-store` means don't cache at all. `max-age=3600` means it's good for an hour.
- **`X-Request-ID`**: A unique ID generated for a single request and propagated through every microservice it touches. Included in all log lines. Essential for distributed tracing and debugging.
- **`Location`**: Sent on a `201 Created` response, pointing to the URL of the newly created resource.
