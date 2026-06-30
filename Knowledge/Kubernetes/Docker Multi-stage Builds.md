---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 2 — Docker Deep Dive"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Docker Image Layers and Caching"]
tags: [docker, optimization, security]
---

# Docker Multi-stage Builds

## Intuition
A naive Dockerfile leaves compilers, source maps, and dev dependencies in the final production image, making it huge and increasing the attack surface. 
Multi-stage builds solve this by splitting the build into two or more stages.

## How it works
You use multiple `FROM` statements. 
1. **Builder Stage:** Contains the full toolchain. It compiles the source code into finished artifacts.
2. **Runtime Stage:** Starts from a minimal base image (e.g., `node:slim`). It copies *only the compiled artifacts* out of the builder stage using `COPY --from=builder`. 

The builder stage is entirely discarded. This can reduce image size from 1GB+ down to 100MB, vastly improving pull times and security.
