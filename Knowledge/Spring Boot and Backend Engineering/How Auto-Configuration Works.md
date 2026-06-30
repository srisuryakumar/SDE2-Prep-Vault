---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, spring-boot, auto-configuration]
---

# How Auto-Configuration Works

## Intuition
Auto-configuration is not magic. It is a layered system of conditional checks evaluated at startup.

## Step 1: Discovery
Spring Boot needs a list of candidate auto-configuration classes. It reads this from a plain-text file in the starter JARs: `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (in Spring Boot 2.7+). *Note: In older versions, it used `META-INF/spring.factories`.*

## Step 2: Conditional Evaluation
Most candidate classes guard themselves with condition annotations. Only if the conditions are satisfied do they actually contribute beans.
- **`@ConditionalOnClass(DataSource.class)`**: Checks the classpath. Is the JDBC driver present?
- **`@ConditionalOnMissingBean(DataSource.class)`**: Checks the `ApplicationContext`. Has the developer already defined their own `DataSource` bean? If yes, back off and don't auto-configure.

## Interview Strategy
> "How does Spring Boot decide whether to auto-configure a `DataSource`, and how would you prevent it?"

**Answer:** It uses `@ConditionalOnClass` to check if a JDBC driver is present, and `@ConditionalOnMissingBean` to ensure you haven't defined one yourself. To prevent it, you can:
1. Not include the JDBC dependency.
2. Define your own `@Bean` of type `DataSource`.
3. Explicitly exclude it: `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)`.
