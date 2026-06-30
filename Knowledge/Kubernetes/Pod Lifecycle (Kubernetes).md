---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 4 — Kubernetes Objects"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kubernetes Pods"]
tags: [kubernetes, architecture, pods]
---

# Pod Lifecycle (Kubernetes)

## Intuition
A Kubernetes Pod moves through a specific set of phases during its lifespan:

## Phases
- **Pending:** The pod has been accepted, but one or more containers aren't running yet (e.g., waiting to be scheduled, or pulling images).
- **Running:** The pod is scheduled to a node, and at least one container is running (or starting/restarting).
- **Succeeded:** All containers terminated successfully (exit code 0). Usually seen with run-to-completion Jobs, not web APIs.
- **Failed:** All containers terminated, and at least one failed (non-zero exit code), and the restart policy does not allow a restart.
- **Unknown:** The API Server cannot obtain the pod's status (usually because the node is unreachable).
