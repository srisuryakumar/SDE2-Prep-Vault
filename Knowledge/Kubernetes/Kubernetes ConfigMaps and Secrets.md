---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 4 — Kubernetes Objects"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [kubernetes, configuration, security]
---

# Kubernetes ConfigMaps and Secrets

## Intuition
Both objects separate configuration from the container image, allowing the same immutable image to run across dev, staging, and prod with different settings injected at runtime (as environment variables or mounted files).

## Secrets are NOT Encrypted
This is a critical misconception: A `Secret` object's `data` field is **base64-encoded, not encrypted.** Anyone with read access to the API (or an etcd backup) can decode it trivially. 

## The Production Fix
Never commit plaintext Secrets to Git.
- **Sealed Secrets:** You encrypt the Secret client-side with a public key before committing. An in-cluster controller (holding the private key) decrypts it back into a native Secret.
- **External Secrets Operator:** Store secrets in AWS Secrets Manager or HashiCorp Vault. An in-cluster operator syncs them into native Kubernetes Secrets automatically.
