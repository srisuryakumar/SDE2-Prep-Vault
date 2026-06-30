---
type: star-story
story_id: 7
title: "Insist on Highest Standards — Skipping Unit Tests"
amazon_lps: ["Insist on Highest Standards"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
We were rushing to launch a new feature before a marketing deadline. The team agreed to skip writing unit tests to save time, promising to "do it later."

### Task
I had to push back against the team and the product manager to ensure we didn't ship fragile code.

### Action
I refused to approve the PRs without tests. To avoid being a blocker, I stayed late to write a core suite of integration tests covering the critical path myself, and I automated the Jest runner in our GitHub Actions pipeline so it couldn't be bypassed. I explained to the PM that shipping without tests would result in a broken demo on launch day.

### Result
The tests caught a critical state-mutation bug just two hours before launch. We shipped on time, bug-free, and the team permanently adopted a rule that no PR is merged without testing.
