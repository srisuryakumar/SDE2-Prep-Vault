---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, architecture, cdn]
---

# Content Delivery Networks (CDN)

A CDN (like Cloudflare, AWS CloudFront, Akamai) is a geographically distributed network of cache servers. 

Instead of all users worldwide fetching static assets (images, CSS, JS) from your single origin server in Mumbai, the CDN caches these assets at hundreds of edge locations (nodes) around the globe.

When a user in Tokyo requests an image, they fetch it from the Tokyo CDN node (5ms latency) rather than traversing the globe to Mumbai (150ms latency). The origin server only receives requests for cache misses or dynamic API content, dramatically reducing load on your infrastructure and improving load times for users.
