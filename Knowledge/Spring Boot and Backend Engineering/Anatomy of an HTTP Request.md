---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 1 — The HTTP Protocol"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [http, networking, backend]
---

# Anatomy of an HTTP Request

## Intuition
An HTTP request is genuinely just plain text sent over a TCP socket. Everything a framework like Spring does (e.g. `@RequestBody`, `@RequestHeader`) is just programmatic parsing of this text format.

## Request Structure
Four parts, always in this order:
1. **The Request Line**: `POST /v1/orders HTTP/1.1` (Method, path, protocol version).
2. **Headers**: Key-value metadata (e.g., `Content-Type: application/json`). Terminated by an empty line.
3. **An Empty Line**: Separates headers from the payload. Not optional.
4. **The Body (Optional)**: The actual payload (usually present in `POST`, `PUT`, `PATCH`).

## Response Structure
Identical shape, but with a status line instead of a request line.
1. **The Status Line**: `HTTP/1.1 201 Created`
2. **Headers**: Key-value metadata.
3. **An Empty Line**.
4. **The Body (Optional)**.
