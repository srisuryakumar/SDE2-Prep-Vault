---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, oop, design]
---

# Why OOP Exists (Procedural vs OOP)

Before Object-Oriented Programming (OOP), code was written procedurally—as a series of disconnected functions operating on loose global or local data. 

## The Procedural Problem at Scale
- **No data encapsulation:** Any function could modify a global variable directly (e.g., setting a bank balance to negative) without validation.
- **Scattered state:** The properties of a single entity (like a user's name, email, and age) existed as unrelated variables.
- **Difficult reuse:** Modifying behavior required copying/pasting functions and changing them slightly.

## The OOP Solution
OOP solves this by bundling data (fields) and the behavior (methods) that operate on that data into a single, secure unit called a **Class**.
