---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 8 — AWS Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [aws, security, iam]
---

# AWS IAM (Identity and Access Management)

## Intuition
IAM controls who (or what) can do what to which AWS resources.

## Concepts
- **Users:** Long-lived credentials for humans or legacy apps.
- **Roles:** Identities without permanent credentials, **assumed temporarily** by users, services, or Kubernetes pods. Roles grant short-lived, auto-rotating credentials.
- **Policies:** JSON documents defining allowed/denied actions on specific resources.

## Principle of Least Privilege
Never grant `"Action": "*"` or `"Resource": "*"`. Grant exactly the permissions required to do the job on the specific resources needed (e.g., read/write on one specific S3 bucket). This limits the blast radius if a credential is compromised.
