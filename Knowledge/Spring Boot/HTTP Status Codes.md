---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 1 — The HTTP Protocol"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [http, status-codes, rest]
---

# HTTP Status Codes

## Intuition
Status codes are grouped by their first digit: 2xx (Success), 3xx (Redirection), 4xx (Client Error), 5xx (Server Error). Clients and SDKs branch their logic based on these.

## Key Codes
- **`200 OK`**: Successful GET, PUT, or PATCH.
- **`201 Created`**: Successful POST. Should include a `Location` header.
- **`202 Accepted`**: Valid request, but processed asynchronously later.
- **`204 No Content`**: Succeeded, nothing to return (canonical for DELETE).
- **`301 / 302`**: Permanent / Temporary redirect.
- **`401 Unauthorized`**: *Unauthenticated*. You haven't proven who you are.
- **`403 Forbidden`**: The server knows who you are, but you are not authorized for this action.
- **`404 Not Found`**: Resource doesn't exist (or hidden for security).
- **`409 Conflict`**: Valid request, but cannot be applied due to the *current state* of the resource (e.g., attempting to cancel an already-shipped order, or an optimistic locking failure).
- **`500 Internal Server Error`**: Server crash. Never leak stack traces.
- **`502 Bad Gateway`**: Proxy got an invalid response from upstream (upstream crashed).
- **`503 Service Unavailable`**: Deliberately not handling requests right now (overloaded).
- **`504 Gateway Timeout`**: Proxy gave up waiting for upstream (upstream is too slow).

## 400 vs 422
- **`400 Bad Request`**: The server cannot even parse the request (malformed JSON, wrong structure). Fix the client code.
- **`422 Unprocessable Entity`**: The request is syntactically valid (parseable JSON) but semantically invalid (e.g., negative quantity, invalid email format). Fix the data.
