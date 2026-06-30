---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, cli, linux]
---

# CLI Tools and Unix Pipes

A CLI tool is a process with no GUI. It reads input from **stdin** (file descriptor 0), writes output to **stdout** (fd 1), and writes errors to **stderr** (fd 2).

## Exit Codes
When a CLI tool finishes, it returns an exit code to the shell.
- `0` means success.
- Any non-zero value (e.g., `1`) means an error occurred.

## Unix Pipes
The Unix philosophy is to write small tools that do one thing well and connect them. A pipe (`|`) connects the stdout of one process directly to the stdin of the next process. Data flows as a byte stream.

Example: `cat app.log | grep "ERROR" | sort | uniq -c`
This chains four separate processes together to count the frequency of unique errors in a log file.
