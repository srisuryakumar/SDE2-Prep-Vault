---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, architecture, state]
---

# Stateless vs Stateful Architecture

## Stateful Servers
A stateful server stores session information (like "User X is logged in") in its local memory. 
- **The problem:** If a client makes a second request and the load balancer sends it to Server B (which doesn't have the session data), the request fails. This requires "sticky sessions," which complicates load balancing and makes scaling difficult.

## Stateless Servers
A stateless server stores NO session state. Every request must be entirely self-contained, containing all the information the server needs to process it.
- **JWT (JSON Web Token):** This is the standard mechanism for stateless auth. The token itself contains the user's identity and permissions, cryptographically signed by the server.
- **Why it scales:** Because the server holds no state, a load balancer can route any request to any available server instance. All instances can independently verify the JWT signature. You can add or remove servers effortlessly to handle varying load.
