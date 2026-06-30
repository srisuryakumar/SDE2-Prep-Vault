---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 8 — AWS Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["AWS IAM (Identity and Access Management)"]
tags: [aws, kubernetes, security]
---

# AWS EKS (Elastic Kubernetes Service)

## Intuition
EKS is AWS's managed Kubernetes offering. AWS operates the **control plane** (API Server, etcd, Scheduler) as a managed, highly-available service. You manage the **worker nodes** (EC2 instances or serverless Fargate) that run your pods.

## IRSA (IAM Roles for Service Accounts)
Historically, if a pod needed S3 access, you attached an IAM role to the entire EC2 worker node. This violated least privilege because *every* pod on that node inherited those permissions.
**IRSA** fixes this. You annotate a specific Kubernetes `ServiceAccount` with an IAM role ARN. Only pods using that specific `ServiceAccount` can assume the role and access the AWS resource. Permissions follow the application identity, not the physical node.
