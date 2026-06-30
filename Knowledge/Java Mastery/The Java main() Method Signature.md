---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 1 — How Java Works"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, syntax]
---

# The Java main() Method Signature

Every Java application starts at this exact entry point:
`public static void main(String[] args)`

Each keyword is required for a specific reason:
- **`public`**: The JVM must be able to invoke this method from outside the class.
- **`static`**: The JVM calls this method *before* creating any objects. It belongs to the class itself, not an instance. If it weren't static, the JVM wouldn't know how to construct the object to call the method.
- **`void`**: The JVM does not use a return value. (To exit with an error code, you use `System.exit(1)`).
- **`main`**: The exact name the JVM startup routine looks for.
- **`String[] args`**: Command-line arguments passed to the program, parsed as an array of Strings.
