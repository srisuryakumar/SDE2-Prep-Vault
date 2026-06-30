---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 8 — Spring AOP"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [spring, aop]
---

# AOP Vocabulary

## Intuition
AOP has specific terminology:
- **Aspect:** The class that contains the advice (annotated with `@Aspect` and `@Component`).
- **Advice:** The code that runs at a specific point (`@Before`, `@AfterReturning`, `@AfterThrowing`, `@After`, `@Around`).
- **Pointcut:** A predicate expression that selects which methods the advice applies to.
- **Join point:** A specific method invocation that matched a pointcut. (In Spring AOP, join points are ALWAYS method calls).
- **ProceedingJoinPoint:** An object passed to `@Around` advice representing the actual method invocation. Calling `pjp.proceed()` invokes the target method.
