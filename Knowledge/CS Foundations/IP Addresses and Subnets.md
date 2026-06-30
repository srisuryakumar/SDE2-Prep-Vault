---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 4 — Networking"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, networking, ip]
---

# IP Addresses and Subnets

## IPv4 vs IPv6
- **IPv4:** 32-bit addresses (e.g., `192.168.1.100`), providing ~4.3 billion addresses.
- **IPv6:** 128-bit addresses (e.g., `2001:db8::8a2e:370:7334`), providing vastly more addresses to solve IPv4 exhaustion.

## Private IP Addresses and NAT
Private IP ranges (e.g., `10.0.0.0/8`, `192.168.0.0/16`) are not routable on the public internet. They are used in home networks and cloud VPCs. Network Address Translation (NAT) allows multiple devices with private IPs to share a single public IP to reach the internet.

In Kubernetes, Pods get private IPs (e.g., `10.244.0.0/16`) that are private to the cluster.

## CIDR Notation
CIDR (Classless Inter-Domain Routing) notation like `192.168.1.0/24` means the first 24 bits are the network identifier, and the remaining bits (8 bits = 256 addresses) are for hosts in that subnet.

## Ports
An IP address identifies a machine, while a **port** (a 16-bit number, 0-65535) identifies an application on that machine.
- **Well-known ports:** 80 (HTTP), 443 (HTTPS), 5432 (PostgreSQL).
- **Ephemeral ports (49152-65535):** Randomly assigned to outgoing connections from a client.
