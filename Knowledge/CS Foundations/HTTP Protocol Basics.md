---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 4 — Networking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, networking, http]
---

# HTTP Protocol Basics

HTTP (HyperText Transfer Protocol) is a text-based, request-response protocol running over TCP.

## Structure
- **Request:** Request line (Method, Path, Version), Headers, Empty line, Body (optional).
- **Response:** Status line (Version, Status Code, Reason), Headers, Empty line, Body.

## HTTP Methods (Verbs)
- **GET:** Retrieve a resource (Idempotent, Safe).
- **POST:** Create a new resource or submit data (Not Idempotent, Not Safe).
- **PUT:** Replace an entire resource (Idempotent, Not Safe).
- **PATCH:** Partially update a resource (Not Idempotent, Not Safe).
- **DELETE:** Delete a resource (Idempotent, Not Safe).
- **HEAD:** Like GET, but returns headers only (no body).

## HTTP Status Codes
- **2xx (Success):** 200 (OK), 201 (Created), 204 (No Content).
- **3xx (Redirection):** Instructs the client to go to another URL.
- **4xx (Client Error):** 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 422 (Unprocessable Entity), 429 (Too Many Requests).
- **5xx (Server Error):** 500 (Internal Server Error), 502 (Bad Gateway), 503 (Service Unavailable), 504 (Gateway Timeout).

Understanding method semantics and status codes is essential for REST API design.
