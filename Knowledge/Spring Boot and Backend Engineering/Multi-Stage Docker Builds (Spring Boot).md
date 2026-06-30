---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 10 — Deployment"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["JVM Memory Limits in Containers"]
tags: [deployment, docker, spring]
---

# Multi-Stage Docker Builds (Spring Boot)

## Intuition
A multi-stage Dockerfile uses one image (the "builder" with a full JDK and Maven) to compile the application, and a second, much smaller image (the "runtime" with only a JRE) to run it.

## Why it matters
1. **Smaller Image Size:** The final image doesn't include the JDK, source code, or Maven cache. Smaller images push/pull faster and have a smaller attack surface.
2. **Caching Efficiency (Layered JARs):** Spring Boot supports extracting the application into layers (dependencies, spring-boot-loader, snapshot-dependencies, application classes). By copying these layers independently in the Dockerfile, Docker can cache the dependencies. When you only change your source code, the dependencies layer is reused from cache, turning a 60-second build into a 5-second build.

## Example Runtime Stage
```dockerfile
FROM eclipse-temurin:21-jre-jammy AS runtime
WORKDIR /app
# Dependencies change rarely — cached by Docker
COPY --from=builder /app/target/extracted/dependencies/ ./
# Application code changes frequently
COPY --from=builder /app/target/extracted/application/ ./
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```
