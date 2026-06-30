---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 1 — How Java Works"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, jvm, classloader]
---

# Java ClassLoaders

The ClassLoader is a subsystem of the JVM that loads `.class` files into memory when they are needed.

## The Parent-Delegation Model
Java uses a hierarchical parent-delegation model for class loading. When the JVM needs a class, it asks the lowest ClassLoader, which immediately delegates the request to its parent, all the way to the top. Only if the parent cannot find the class does the child attempt to load it. 

1. **Bootstrap ClassLoader (Top):** Loads core Java classes from the JDK (e.g., `java.lang.String`, `java.util.List`). Written in native code.
2. **Extension ClassLoader:** Loads classes from the JDK extension directories.
3. **Application ClassLoader (Bottom):** Loads your application's classes from the classpath (your `-cp` flag or `target/classes`).

## Why Parent-Delegation?
This prevents user code from replacing or hijacking core Java classes. If you create a class named `java.lang.String` in your project, the Application ClassLoader will delegate the request for `String` up to the Bootstrap ClassLoader, which will find the real `String` class and return it. Your malicious/fake `String` class will never be loaded.
