---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 6 — Developer Environment, Git, and Tooling"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [cs-foundations, tooling, java]
---

# Java Development Environment (SDKMAN and JDK 21)

## SDKMAN
SDKMAN is a version manager for JVM-based tools (Java, Maven, Gradle). It allows you to install multiple versions of Java and switch between them instantly (e.g., from Java 17 to Java 21) without manually updating environment variables like `JAVA_HOME`. This ensures project consistency and solves the "works on my machine" problem caused by mismatched JDKs.

## JDK 21
Java 21 is an LTS (Long-Term Support) release featuring virtual threads, records, pattern matching, and sealed classes. 
- **Eclipse Temurin:** The recommended open-source distribution of OpenJDK (built by the Eclipse Foundation). Since Java 17, Oracle JDK requires a commercial license for production, so developers use OpenJDK distributions like Temurin, Amazon Corretto, or Azul Zulu.
