---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 8 — AWS Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [aws, networking, vpc, security]
---

# AWS VPC (Virtual Private Cloud)

## Intuition
A VPC is a logically isolated slice of the AWS network, subdivided into subnets across different Availability Zones (AZs) for fault tolerance.

## Public vs Private Subnets
- **Public Subnets:** Have a route to an Internet Gateway. Resources here are reachable from the internet (e.g., Load Balancers).
- **Private Subnets:** Have **no** route to the Internet Gateway. Nothing inside is reachable from the internet, regardless of security groups. This is where databases and Kubernetes worker nodes belong, providing structural defense-in-depth.

## NAT Gateway
Resources in private subnets often need *outbound* internet access (to download images or updates). A NAT Gateway (placed in a public subnet) allows them to initiate outbound connections while remaining completely hidden from inbound connections.
