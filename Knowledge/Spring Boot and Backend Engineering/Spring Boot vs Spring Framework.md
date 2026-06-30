---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, spring-boot, architecture]
---

# Spring Boot vs Spring Framework

## Intuition
Spring Framework is a dependency-injection container and a collection of modules (MVC, data access). Historically, it required heavy XML or Java configuration.
Spring Boot sits on top of Spring Framework and provides two main features:
1. **Convention over Configuration:** It ships with opinionated defaults. If you add JPA and a PostgreSQL driver, it configures a DataSource, JpaTransactionManager, and Hibernate automatically.
2. **Auto-Configuration:** The mechanism that makes convention over configuration work, evaluating the classpath to decide what defaults to activate.

## Lombok
Lombok (`@Getter`, `@Setter`, `@RequiredArgsConstructor`) is an annotation processor that runs at **compile time**. It generates boilerplate Java source code directly into your `.class` files before `javac` finishes. It is NOT runtime reflection magic.
