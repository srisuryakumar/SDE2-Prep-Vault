---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 5 — Security JWT"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [security, jwt, architecture]
---

# Stateless Authentication

## Intuition
Traditional authentication uses **server-side sessions**, where the server stores a session object in memory (or Redis) and gives the client a session ID (in a cookie). The server looks up this ID on every request to know who the user is.

**Stateless authentication** stores nothing on the server. The client holds all state needed to prove identity — typically a signed JWT — and sends it with every request. The server independently validates the signature to trust the token's claims.

## Advantages
- **Horizontal Scalability:** Any server instance can authenticate any request without coordinating with a central session store. (No need for "sticky sessions" or shared Redis instances).
- **Reduced Infrastructure:** No session store to maintain, scale, or worry about going down.

## Drawbacks
- **Token Revocation:** Since tokens are validated purely via cryptography without a server lookup, you cannot easily revoke a token before it expires (e.g. if a user is banned or logs out). 
- **Mitigation:** Use short-lived access tokens (e.g. 15 minutes) and longer-lived refresh tokens. If immediate revocation is required, you must implement a server-side "blocklist" of revoked tokens (which reintroduces some statefulness).
