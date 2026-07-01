---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 5 — Security JWT"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [security, web]
---

# CORS vs CSRF

## Intuition
They sound similar but protect against completely different threat models.

## CORS (Cross-Origin Resource Sharing)
**What it is:** A browser security mechanism that blocks a web page from making AJAX requests to a different origin (domain/port) than the page itself — *unless* the server explicitly allows it via CORS headers.
**Why we configure it:** So our frontend SPA (e.g. `localhost:3000`) can legally call our backend API (`localhost:8080`) without the browser blocking the request.

## CSRF (Cross-Site Request Forgery)
**What it is:** An attack where a malicious site tricks a user's browser into making an *authenticated* request to your API without the user's knowledge. This relies on the browser automatically attaching the user's **session cookie** to cross-site requests.
**Why we disable it for JWT APIs:** JWTs are not cookies. They must be explicitly attached (in the `Authorization` header) by JavaScript code. Malicious cross-site scripts cannot read the JWT or attach it, because CORS blocks them. Therefore, the CSRF attack vector doesn't apply to stateless JWT APIs, and we disable CSRF protection.
