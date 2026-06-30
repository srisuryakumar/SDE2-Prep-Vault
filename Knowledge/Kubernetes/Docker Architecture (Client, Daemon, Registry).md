---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 2 — Docker Deep Dive"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Docker Image Layers and Caching"]
tags: [docker, architecture]
---

# Docker Architecture (Client, Daemon, Registry)

## Intuition
When you type `docker run nginx`, four distinct pieces of software cooperate to make it happen.

## Components
1. **Docker Client:** The `docker` CLI binary. It doesn't do the work; it translates your commands into REST API calls.
2. **Docker Daemon (`dockerd`):** The long-running background process on the host. It does the actual work of building, pulling, running, and managing containers and networks.
3. **Images & Containers:** Images are read-only templates. Containers are running instances of images with a thin writable layer on top.
4. **Registry:** A server that stores and distributes images (e.g., Docker Hub, AWS ECR). Images must be pulled from a registry to the local daemon before they can be run.
