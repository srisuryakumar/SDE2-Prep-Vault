---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 2 — Docker Deep Dive"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Docker Multi-stage Builds"]
tags: [docker, performance, caching]
---

# Docker Image Layers and Caching

## Intuition
Every instruction in a `Dockerfile` (`FROM`, `RUN`, `COPY`, etc.) produces a new, immutable, content-addressed **layer**. Layers stack on top of each other. 
Crucially, **Docker caches each layer**. If an instruction hasn't changed (and no layer above it has changed), Docker reuses the cached layer.

## Instruction Order Matters
Because changing one layer invalidates all subsequent layers, you must order instructions from **least-frequently-changed** to **most-frequently-changed**.

**Bad:**
```dockerfile
COPY . .           # Source code changes often
RUN npm install    # Will needlessly reinstall everything on every code change
```

**Good:**
```dockerfile
COPY package.json ./  
RUN npm install       # Cached unless package.json changes
COPY . .              # Source code changes only invalidate this final layer
```
