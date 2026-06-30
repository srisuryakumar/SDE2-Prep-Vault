---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, spring-boot, annotations, component-scan]
---

# @SpringBootApplication (The 3 Annotations)

## Intuition
`@SpringBootApplication` is a meta-annotation that bundles three distinct annotations:

## 1. @SpringBootConfiguration (meta-annotated with @Configuration)
Marks the class as a source of bean definitions (like any class with `@Bean` methods).

## 2. @EnableAutoConfiguration
Tells Spring Boot to inspect the classpath and conditionally activate auto-configuration classes based on what dependencies are present.

## 3. @ComponentScan
Tells Spring to scan for `@Component` (and its specializations like `@Service`, `@Repository`, `@Controller`) starting from the package the annotated class lives in, and recursively downward.

## Interview Trap
> "If you moved your main application class into a sub-package like `com.example.app`, what would break?"

**Answer:** Component scanning starts at the package of the `@SpringBootApplication` class and only scans downward. If you move it to `com.example.app`, all your actual code in `com.example.service` or `com.example.controller` will not be found because they are siblings, not descendants. No beans get registered, and the app fails to start or silently has no controllers. Fix it by moving it back to the root package, or explicitly using `@ComponentScan(basePackages = "com.example")`.
