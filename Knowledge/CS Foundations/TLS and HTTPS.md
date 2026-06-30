---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 4 — Networking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, networking, tls, security]
---

# TLS and HTTPS

Plain HTTP sends all data as unencrypted text, vulnerable to Man-in-the-Middle (MITM) attacks. HTTPS solves this by running HTTP over TLS (Transport Layer Security).

## The TLS Handshake
TLS executes a handshake *before* HTTP data is transmitted:
1. Client and Server agree on a cipher suite and exchange random nonces.
2. The Server sends its digital certificate (containing its public key) to prove its identity.
3. The Client verifies the certificate against a trusted Certificate Authority (CA).
4. They use **asymmetric encryption** (public/private keys) to securely negotiate a shared symmetric session key (e.g. AES).
5. All subsequent HTTP data is encrypted and decrypted using this fast **symmetric encryption** session key.

This hybrid approach leverages asymmetric encryption for secure key exchange, and symmetric encryption for fast data transfer.

## Certificates and CAs
A Certificate Authority (like Let's Encrypt or DigiCert) verifies domain ownership and cryptographically signs a server's digital certificate. Browsers come pre-installed with root CA certificates to verify the chain of trust.

In microservices architectures (e.g. Kubernetes), TLS is typically terminated at the Ingress controller or load balancer, and internal service-to-service communication happens over plain HTTP (since the internal network is trusted).
