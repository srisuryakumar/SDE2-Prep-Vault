---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 8 — Spring AOP"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, aop]
---

# Pointcut Expressions

## Intuition
Pointcut expressions dictate *which* methods an AOP Aspect intercepts.

## The 5 Main Types
1. **`execution()`**: Match by method signature.
   - Example: `@Pointcut("execution(* com.example.service.*.*(..))")` matches any method in the service package.
2. **`@annotation()`**: Match methods carrying a specific annotation.
   - Example: `@Pointcut("@annotation(com.example.LogPerformance)")` matches only methods explicitly annotated with `@LogPerformance`.
3. **`within()`**: Match all methods within a type or package.
   - Example: `@Pointcut("within(com.example.service..*)")` matches all methods in all classes in the service package or its subpackages.
4. **`target()`**: Match by the runtime type of the target object.
5. **`args()`**: Match by argument type at runtime.

You can combine pointcuts using `&&`, `||`, and `!`.
