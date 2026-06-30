---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 9 — Observability"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: ["Prometheus Metrics and PromQL"]
tags: [observability, prometheus, alerting]
---

# Alertmanager

## Intuition
Prometheus evaluates rules to see if an alert *should* fire. **Alertmanager** handles what happens next.

## Responsibilities
- **Deduplication:** Prevents multiple instances of the same issue from spamming you.
- **Grouping:** If 12 pods crash simultaneously, Alertmanager groups them into a single Slack message instead of sending 12 separate pages.
- **Routing:** Routes alerts to different destinations based on severity (e.g., `critical` pages an engineer via PagerDuty; `warning` just posts to a Slack channel).
- **Silencing:** Allows on-call engineers to temporarily suppress notifications for known issues or during maintenance windows without altering the underlying Prometheus rules.
