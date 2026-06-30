---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 7 — CI/CD with GitHub Actions and Helm"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [kubernetes, helm, deployments, templating]
---

# Helm Charts Overview

## Intuition
Maintaining separate folders of raw YAML for Dev, Staging, and Production leads to severe configuration drift. Someone fixes a bug in Prod YAML but forgets to backport it to Staging YAML.

## The Helm Solution
Helm packages Kubernetes manifests as a **chart**. It separates the *structure* (the templated YAML in `templates/`) from the *values* (the environment-specific overrides like replica counts and hostnames).
- `values.yaml`: Sensible defaults.
- `values-prod.yaml`: Overrides for production.
- `values-dev.yaml`: Overrides for dev.

A structural fix (like fixing a typo in a volume mount) is made exactly once in the template, and automatically applies to every environment on the next deploy. Helm also provides a single-command `helm rollback`.
