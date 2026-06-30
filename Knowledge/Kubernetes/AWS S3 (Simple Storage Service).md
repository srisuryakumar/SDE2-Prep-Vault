---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 8 — AWS Fundamentals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [aws, storage, security]
---

# AWS S3 (Simple Storage Service)

## Intuition
S3 is an object storage service with effectively unlimited capacity. Files (objects) are stored in buckets and addressed by a flat key, not a real filesystem directory tree.

## Presigned URLs
If a user needs to upload a large file, routing it through your backend API server is inefficient. 
Instead, your backend (which has AWS IAM credentials) can generate a **Presigned URL**: a time-limited, cryptographically-signed URL that grants permission for *exactly one operation* (e.g., `PUT` this specific object key) for a short window (e.g., 15 minutes). The client then uploads the file directly to S3 using that URL, keeping the heavy traffic off your API servers.
