---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, architecture, servers]
---

# Web Servers vs Application Servers

## Web Server (e.g., Nginx, Apache)
Handles HTTP requests. It specializes in:
- Serving static files (HTML, CSS, JS, images) from disk at hardware speed.
- Reverse proxying (forwarding requests to backend apps).
- Load balancing.
- SSL/TLS termination.
It does not execute application logic (like Java code).

## Application Server (e.g., Tomcat, Jetty, Undertow)
Executes your application code. It manages threads, connection pools, and the HTTP request lifecycle, converting raw HTTP bytes into Java objects (like `HttpServletRequest`).

## Spring Boot and Embedded Tomcat
Traditionally, you would deploy a `.war` file into a standalone Tomcat installation. Spring Boot embeds Tomcat (as a library) directly into your application's "fat JAR". Running `java -jar myapp.jar` starts the JVM, which starts Tomcat internally, which then runs your Spring code.

## Production Architecture
In production, you never expose Spring Boot directly to the internet. You put Nginx (or an ALB/Ingress) in front. Nginx handles SSL termination and serves static assets efficiently, forwarding only dynamic API requests (over plain HTTP) to your Spring Boot application servers on the private network.
