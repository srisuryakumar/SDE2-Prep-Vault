---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 10 — Deployment"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Multi-Stage Docker Builds (Spring Boot)"]
tags: [java, jvm, docker, operations]
---

# JVM Memory Limits in Containers

## Intuition
Historically, the JVM looked at the *host machine's* RAM to decide its maximum heap size. If running inside a Docker container with a 512MB limit on a 16GB host, the JVM might allocate a 4GB heap. The OS would then OOM-kill the container.

## Modern Solution
Always run Java in containers with container support enabled (enabled by default in modern Java, but good to make explicit) and define heap size as a percentage of the container limit:

```dockerfile
ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-jar", "app.jar"]
```

`-XX:MaxRAMPercentage=75.0` tells the JVM to use up to 75% of the *container's* memory limit for the heap, leaving the remaining 25% for off-heap use (thread stacks, Metaspace, native memory).
