---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, arrays, memory]
---

# Java Arrays

Arrays in Java are fixed-size, contiguous blocks of memory containing either primitives directly or object references. They are objects themselves, stored on the Heap.

## Declaration and Initialization
```java
// Declaration + allocation (elements initialized to default values e.g., 0)
int[] scores = new int[5];

// Declaration + initialization
int[] primes = {2, 3, 5, 7, 11};
```

## `java.util.Arrays` Utility Class
The standard library provides powerful utilities for arrays:
- `Arrays.sort(arr)`: In-place sort.
- `Arrays.binarySearch(arr, target)`: O(log n) search (array must be sorted).
- `Arrays.copyOf(arr, length)`: Creates a new deep copy of the array.
- `Arrays.toString(arr)`: Pretty-prints the array (otherwise `System.out.println(arr)` prints the memory address).

## Multidimensional and Jagged Arrays
Java arrays can hold other arrays. They do not have to be perfectly rectangular (jagged arrays).
```java
// 2D Matrix (3 rows, 4 columns)
int[][] matrix = new int[3][4];

// Jagged Array (rows have different lengths)
int[][] jagged = new int[3][];
jagged[0] = new int[]{1};
jagged[1] = new int[]{2, 3};
```

## Aliasing Trap
Because arrays are objects on the Heap, copying the variable only copies the reference, not the data.
```java
int[] a = {1, 2, 3};
int[] b = a; // Aliasing! 'b' points to the same Heap array as 'a'.
b[0] = 99;   // Modifies a[0] as well.
```
Use `Arrays.copyOf()` to duplicate the actual array data.
