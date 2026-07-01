---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 1 — The HTTP Protocol"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [http, methods, idempotency]
---

# HTTP Methods (Safety and Idempotency)

## Intuition
HTTP methods aren't just conventions—properties like **safety** and **idempotency** are part of the spec and dictate how load balancers and proxies handle retries.

- **Safe:** Does not change server state (e.g. `GET`).
- **Idempotent:** Making the request N times produces the same end server state as making it once.

| Method | Safe? | Idempotent? | Explanation |
| :--- | :--- | :--- | :--- |
| **`GET`** | Yes | Yes | Safe to retry, cache, or prefetch. |
| **`POST`** | No | **No** | Creates a new resource every time. Not safe to blindly retry on a timeout. |
| **`PUT`** | No | Yes | Replaces the entire resource. Sending the replacement 5 times results in the same state. |
| **`PATCH`** | No | Not guaranteed | Depends on the payload (`{"status": "CANCELLED"}` is idempotent, `{"quantity": "+5"}` is not). |
| **`DELETE`** | No | Yes | After the first DELETE, the resource is gone. It remains gone on the 2nd attempt, even if the 2nd returns a `404`. |

## Idempotency in Distributed Systems
Network failures often occur *after* the server processed the request but *before* the client got the response. The client must retry.
If a `POST` isn't idempotent, retrying it causes a duplicate (e.g., charging a customer twice).
**Solution:** The client generates a unique `Idempotency-Key` (UUID) per operation and sends it as a header. The server records this key. If a retry arrives with the same key, the server returns the cached successful response instead of processing it again.
