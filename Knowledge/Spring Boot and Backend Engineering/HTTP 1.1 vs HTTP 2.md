---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 1 — The HTTP Protocol"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [http, networking, http2]
---

# HTTP 1.1 vs HTTP 2

## Intuition
HTTP/1.1 requires requests on a single TCP connection to be processed strictly one at a time (head-of-line blocking). Browsers worked around this by opening multiple parallel TCP connections.

HTTP/2 fixes this at the protocol level.

## HTTP/2 Improvements
- **Multiplexing:** Many logical request/response exchanges share a *single* TCP connection simultaneously, interleaved as small frames. One slow request doesn't block others behind it.
- **Header Compression (HPACK):** HTTP/1.1 resends verbose headers on every request. HPACK compresses them using a shared context, saving bandwidth.
- **Server Push (Deprecated):** Originally allowed servers to proactively send resources. Mostly abandoned now.

## Connection Pooling
If HTTP/2 multiplexes over one connection, why do we still need connection pools on the server?
- Multiplexing solves the *client-to-edge* connection count problem.
- Behind your server, your Spring Boot app still needs a pool of database connections (e.g. HikariCP) because the DB speaks its own wire protocol over its own TCP connections. A single HTTP/2 connection carrying 1,000 multiplexed requests can still exhaust your database connection pool.
