---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 6 — Developer Environment, Git, and Tooling"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, tooling, terminal]
---

# Terminal Productivity and CLI Commands

## API Testing (curl and jq)
- **`curl`:** The standard CLI HTTP client.
  - `curl -H "Authorization: Bearer $JWT" http://localhost:8080/api`
  - `curl -X POST -H "Content-Type: application/json" -d '{"key":"val"}' http://...`
- **`jq`:** A powerful CLI JSON processor.
  - Pretty print: `curl ... | jq '.'`
  - Extract field: `curl ... | jq '.status'`
  - Filter array: `curl ... | jq '.[] | select(.status == "PENDING")'`

## Process Investigation
Commands to debug a misbehaving service:
- Find process: `ps aux | grep java` or `jps -v`
- Memory/CPU: `top -p <pid>`, `jmap -heap <pid>`, `jstack <pid>`
- Network: What ports are listening? `ss -tlnp | grep java` or `netstat -tlnp`
- Open files: `lsof -p <pid>`
- Disk I/O: `iotop -o`, `iostat -x 1`

## Log Analysis
Using `grep`, `awk`, `sort`, and `uniq` to parse logs:
```bash
# Count errors per minute:
grep "ERROR" app.log | awk '{print $1, $2}' | cut -c1-16 | sort | uniq -c | sort -rn | head -20
```
