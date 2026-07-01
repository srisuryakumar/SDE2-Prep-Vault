---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [java, syntax, methods]
---

# Java Methods

## Key Concepts
- **Return Types:** A method must declare its return type, or `void` if it returns nothing.
- **Static vs Instance:** `static` methods belong to the class and are called without an object instance (`Math.max()`). Instance methods require an object (`myList.add()`).
- **Varargs (`...`):** Allows passing a variable number of arguments. Inside the method, the varargs parameter is treated as an array.
  ```java
  public int sum(int... numbers) { // 'numbers' is an int[]
      int total = 0;
      for (int n : numbers) total += n;
      return total;
  }
  ```

## Method Overloading
Having multiple methods in the same class with the **same name but different parameters** (type, count, or order). 
- Resolved at **compile time** (static dispatch) based on the argument types provided.
- You *cannot* overload based solely on return type.

```java
public String describe(int n) { ... }
public String describe(double d) { ... }
```
