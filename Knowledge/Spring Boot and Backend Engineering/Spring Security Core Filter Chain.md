---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 5 — Security JWT"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, security]
---

# Spring Security Core Filter Chain

## Intuition
Spring Security is built around a chain of Servlet Filters (`FilterChainProxy`). You configure it via a `SecurityFilterChain` bean using the `HttpSecurity` builder.

## Configuration for Stateless JWT APIs
1. **CSRF Disabled:** `http.csrf().disable()`. Since we use stateless JWTs sent explicitly in headers rather than browser session cookies automatically sent with cross-site requests, CSRF protection is unnecessary.
2. **Session Management STATELESS:** `http.sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)`. This prevents Spring from creating an `HttpSession`.
3. **Custom Filter Insertion:** `.addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)`. We insert our custom JWT filter early in the chain so it can populate the `SecurityContext` before authorization checks happen.
4. **Authorization Rules:** We define which endpoints are public (e.g. `/v1/auth/**`) using `permitAll()` and specify that `anyRequest().authenticated()` for the rest.
