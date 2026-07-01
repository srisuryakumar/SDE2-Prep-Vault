---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 5 — Security JWT"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, security, jwt]
---

# JwtAuthenticationFilter (Spring Security)

## Intuition
The filter is responsible for intercepting the HTTP request, extracting the JWT, validating it, and telling Spring Security who the user is. 
It usually extends `OncePerRequestFilter` to ensure it only runs once per request.

## The Flow
1. The request hits the filter. It extracts the `Authorization` header and strips the `Bearer ` prefix to get the raw JWT.
2. If the token is missing or invalid (fails signature verification or is expired), it does nothing (just calls `filterChain.doFilter()`). Missing authentication will later be caught by the authorization rules and result in a `401 Unauthorized`.
3. If the token is valid, it extracts the user identity (e.g. email) from the payload.
4. It loads the full `UserDetails` object (often from the database, though claims can be used to optimize this).
5. It creates a `UsernamePasswordAuthenticationToken` and sets it on `SecurityContextHolder.getContext().setAuthentication(authToken)`.
6. The request continues down the chain. Now, any controller method can access the authenticated user via `@AuthenticationPrincipal`.
