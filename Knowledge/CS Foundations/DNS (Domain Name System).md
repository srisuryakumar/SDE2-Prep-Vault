---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 4 — Networking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, networking, dns]
---

# DNS (Domain Name System)

The Domain Name System (DNS) translates human-readable domain names (like `api.example.com`) to machine-usable IP addresses.

## DNS Resolution Steps
1. **Local cache:** OS checks if it has the IP cached.
2. **Recursive resolver:** Typically your ISP or Google (8.8.8.8). Checks its cache; if missing, performs the recursive lookup.
3. **Root servers:** The resolver asks a Root server, which points it to a TLD server (like `.com`).
4. **TLD servers:** The `.com` server points the resolver to the authoritative name server for `example.com`.
5. **Authoritative name server:** Returns the IP address for `api.example.com`.
6. The resolver caches the IP and returns it to the client.

## Common DNS Record Types
- **A:** Maps a name to an IPv4 address.
- **AAAA:** Maps a name to an IPv6 address.
- **CNAME:** Alias to another name (e.g., `www.shop.com` to `shop.com`).
- **MX:** Mail server for the domain.
- **TXT:** Arbitrary text, often used for email verification or domain ownership.
- **NS:** Authoritative name servers for the domain.

## TTL (Time To Live)
Every DNS record has a TTL (in seconds) indicating how long resolvers should cache the record. 
- Low TTL (e.g. 60s): Fast failovers/migrations, but more traffic.
- High TTL (e.g. 86400s): Lower load on DNS servers, but changes take up to 24 hours to propagate.

## DNS in Kubernetes
Kubernetes uses **CoreDNS** for service discovery. A Kubernetes Service gets a DNS record like `service-name.namespace.svc.cluster.local`, which resolves to the Service's ClusterIP, allowing Pods to communicate without hardcoding IPs.
