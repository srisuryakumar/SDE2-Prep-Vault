---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 10 — kubectl Mastery"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [kubernetes, debugging, kubectl]
---

# Debugging Kubernetes Pods

## Intuition
When a pod isn't running, follow a strict sequential funnel to debug it, rather than guessing.

## The Debugging Funnel
1. `kubectl get pods` - Look at the `STATUS` column (e.g., `CrashLoopBackOff`, `ImagePullBackOff`).
2. `kubectl describe pod <name>` - Read the `Events` section at the bottom. It usually states the exact error in plain English (e.g., missing secret, out of CPU).
3. `kubectl logs <name> --previous` - If the pod is crash-looping, the *current* container is likely just starting. `--previous` shows the logs of the container that actually crashed, revealing application-level errors (like DB connection failures).
4. `kubectl exec -it <name> -- /bin/sh` - Get an interactive shell to test DNS, connectivity, or check filesystem state.

## Common Failures
- **ImagePullBackOff:** Kubelet can't pull the image (typo, auth issue).
- **CrashLoopBackOff:** The app starts and crashes repeatedly. Always check logs.
- **OOMKilled:** The container exceeded its memory limit and was killed by the Linux kernel. Check for memory leaks or increase limits.
