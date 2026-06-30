---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 7 — CI/CD with GitHub Actions and Helm"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Helm Charts Overview"]
tags: [ci-cd, github-actions, automation]
---

# GitHub Actions for CI-CD

## Intuition
A robust CI/CD pipeline turns "engineer pushes code" into "tested, built, and safely deployed" without manual intervention.

## The Standard Pipeline
1. **Test Job:** Runs on every PR and push. Block merges via Branch Protection rules until this passes.
2. **Build and Push Job:** Runs only on merges to `main` (after tests pass). Builds the Docker image and pushes it to a registry (GHCR, ECR).
3. **Deploy Job:** Runs after the build. Updates the Kubernetes cluster (e.g., via `helm upgrade`).

## Environments and Approval Gates
To prevent fully automated deploys from touching production blindly, you can map the `deploy` job to a GitHub **Environment** with required reviewers. The pipeline will pause and wait for a human to click "Approve" before actually modifying production.
