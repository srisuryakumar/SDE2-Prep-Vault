---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, os]
---

# Kernel Space vs User Space

The OS is split into two fundamental domains, enforced by hardware privilege rings on the CPU (Ring 0 vs Ring 3).

## User Space
Where applications (like your Spring Boot app, JVM, browser) run. 
- Code operates in a restricted mode (Ring 3). 
- Cannot directly access hardware or memory outside its own address space. 
- A bug (like a NullPointerException) crashes only that specific application.

## Kernel Space
Where the OS core (kernel) runs. 
- Has unrestricted access to all hardware and manages resources (Ring 0). 
- A bug here can corrupt shared OS data structures and crash the entire system (Kernel Panic).

This separation limits the blast radius of application bugs. To cross from user space to kernel space, a program must execute a **system call**.
