---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, bean, scope]
---

# Bean Scopes

## Intuition
By default, every bean in Spring is a **singleton** (one instance for the entire application context).

## The Scopes
1. **`singleton` (default):** One instance total. (Stateless services, repositories, controllers).
2. **`prototype`:** A brand new instance every time the bean is requested. (Mutable, request-specific state).
3. **`request`:** One instance per HTTP request.
4. **`session`:** One instance per HTTP session.

## The Scoped Proxy Problem
> "What happens if you inject a `prototype`-scoped bean directly into a `singleton` bean's constructor?"

**Answer:** You get exactly ONE instance of the prototype bean. It is created once, when the singleton is constructed, and held by the singleton forever. This defeats the purpose of the prototype scope. 

To fix this, you must use a **scoped proxy** (which intercepts every method call and looks up the real instance for the active request/prototype), or inject an `ObjectFactory<T>` / `ObjectProvider<T>` and call `.getObject()` every time you need a fresh instance.
