---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, modifiers, encapsulation]
---

# Java Access Modifiers

Java provides four levels of visibility for classes, fields, and methods.

1. **`private`**: Accessible ONLY within the same class. (Most restrictive).
2. **(Package-Private / Default)**: No modifier keyword used. Accessible within the same class AND any other class in the **same package**.
3. **`protected`**: Accessible within the same package AND by **subclasses** in other packages.
4. **`public`**: Accessible from **anywhere**.

## Best Practice
Always default to `private` for fields. Expose state modification only through explicitly defined `public` methods (getters/setters/business methods). This enforces encapsulation.
