---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, architecture, web]
---

# Web Applications and the Client-Server Model

A web application consists of two separate programs communicating over a network:
- **Client (Frontend):** Runs in the user's browser (HTML/CSS/JS). Handles UI and user input.
- **Server (Backend):** Runs on remote hardware. Handles business logic, data storage, and security.

## The Complete Request Lifecycle
When a user clicks a button:
1. **Frontend:** JavaScript `fetch()` sends an HTTP request.
2. **Network:** OS performs DNS resolution, TCP handshake, and TLS handshake.
3. **Infrastructure:** The HTTP request reaches a Load Balancer, which forwards it to a specific backend server.
4. **Backend (Spring Boot):** 
   - Request passes through the Filter Chain (e.g. JwtFilter for authentication).
   - Controller validates input and calls the Service layer.
   - Service checks cache (Redis) or reads/writes to the database (PostgreSQL).
   - Service may publish an event to a message broker (Kafka).
5. **Response:** Backend returns an HTTP response (e.g. `201 Created` with JSON).
6. **Frontend:** Browser parses the JSON and updates the DOM to show the result.
