---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, boot, configuration, properties]
---

# application.yml Precedence Hierarchy

## Intuition
Spring Boot merges many sources of configuration into a single `Environment`, using a strict precedence order. When the same property is defined in multiple places, the highest precedence wins.

## The Hierarchy (Highest to Lowest)
1. **Command-line arguments** (`--server.port=9090`)
2. **OS Environment Variables** (`SERVER_PORT=9090`) - Spring "relaxes" bindings, mapping `SERVER_PORT` to `server.port`.
3. **Profile-specific files** (`application-prod.yml`)
4. **Base file** (`application.yml`)

## Practical Rule
- **Safe, non-secret defaults:** `application.yml`
- **Per-environment differences (e.g. log levels):** Profile-specific files (`application-prod.yml`).
- **Secrets (DB passwords, JWT keys, API keys):** OS Environment Variables. Secrets typed into a YAML file are one `git add .` away from being compromised forever.
