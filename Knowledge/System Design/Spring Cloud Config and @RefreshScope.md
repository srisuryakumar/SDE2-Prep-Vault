---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 9 — Spring Cloud Microservices"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, config, deployment]
---

# Spring Cloud Config and @RefreshScope

## Intuition
Spring Cloud Config centralizes configuration for all microservices in a Git repository. It allows you to change config (like feature flags or timeout values) **without redeploying or restarting** the service.

## @RefreshScope
When a bean (like a Controller) is annotated with `@RefreshScope`, it can be dynamically refreshed at runtime.
If you update a property in Git and trigger a refresh (via `POST /actuator/refresh` or Spring Cloud Bus), the `@RefreshScope` bean is destroyed and re-created with the newly injected `@Value` fields. This provides zero-downtime configuration updates with a full audit trail.

## What it DOESN'T refresh
It cannot refresh heavy, stateful objects like `DataSource` or connection pools. These hold live TCP connections configured with the old settings; they still require a full restart to update. Use `@RefreshScope` for lightweight feature flags and thresholds.
