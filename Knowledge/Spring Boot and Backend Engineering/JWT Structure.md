---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 5 — Security JWT"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [security, jwt]
---

# JWT Structure

## Intuition
A JSON Web Token (JWT) is three Base64URL-encoded JSON segments joined by dots: `header.payload.signature`.

## The Three Parts
1. **Header:** Contains the token type and the signing algorithm (e.g. `HS256` for symmetric HMAC-SHA256, or `RS256` for asymmetric RSA).
2. **Payload:** Contains the *claims* about the user. Standard claims include `sub` (subject/user ID), `iat` (issued at), and `exp` (expiration timestamp). Custom claims might be `email` or `role`. **Do NOT put secrets here — the payload is only base64 encoded, not encrypted. Anyone can read it.**
3. **Signature:** `HMAC-SHA256(Base64URL(header) + "." + Base64URL(payload), secret_key)`. The server uses this to verify the token hasn't been tampered with. If a user modifies the payload (e.g. changing their role to "ADMIN"), the signature validation fails because the secret key is required to forge a matching signature.
