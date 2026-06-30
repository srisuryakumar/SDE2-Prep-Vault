---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 6 — Resource Management and Autoscaling"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [kubernetes, scaling, automation]
---

# Horizontal Pod Autoscaler (HPA)

## Intuition
The HPA automatically adjusts a Deployment's replica count based on observed metrics (like CPU utilization or custom Prometheus metrics).

## The Algorithm
`desiredReplicas = ceil( currentReplicas × ( currentMetricValue / targetMetricValue ) )`

For example, if 4 replicas target 50% CPU but are running at 80% CPU:
`ceil( 4 * (80/50) ) = 7 replicas`

## Preventing Flapping
If the HPA scales up during a brief spike and scales down immediately after, you suffer "flapping" (constant pod churn). 
`stabilizationWindowSeconds` fixes this by looking back over a recent time window and picking the *highest* desired-replica value seen in that window for scale-down decisions, delaying the scale-down until the spike is definitively over.
