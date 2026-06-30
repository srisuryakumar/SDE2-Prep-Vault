---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 1 — The HTTP Protocol"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [http, https, tls, security, encryption]
---

# HTTPS and TLS

## Intuition
HTTPS is just HTTP sent over a TLS-encrypted connection. 

## The Certificate Chain
A server presents a certificate signed by a Certificate Authority (CA). The client doesn't trust it blindly; it walks a chain. The server's cert is signed by an intermediate CA, which is signed by a root CA. The root CA ships pre-trusted in the client's OS/browser. If any certificate in this chain expires, the chain of trust breaks and the connection is rejected.

## The TLS 1.3 Handshake (Asymmetric to Symmetric)
Asymmetric encryption (public/private key) is too slow for bulk data transfer. So TLS uses asymmetric crypto for exactly one job: **the handshake**.
1. Client and Server use asymmetric crypto (Diffie-Hellman key exchange) to safely agree on a shared **symmetric session key** without ever transmitting the key itself.
2. Once both sides have the symmetric key, they switch to a fast symmetric cipher (like AES) for the actual HTTP traffic.

**Why both?** Asymmetric crypto solves the problem of establishing a shared secret over an insecure channel. Symmetric crypto solves the problem of encrypting bulk data fast enough to not bottleneck a high-throughput connection.
