---
type: star-story
story_id: 20
title: "Time you improved a process without being asked — Setup Script"
amazon_lps: []
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
New engineers joining our team were taking nearly three days just to set up their local development environments due to outdated README files and complex manual Docker commands.

### Task
I wanted to reduce this friction so new hires could commit code on their first day.

### Action
Without being assigned the task, I spent my Friday afternoon writing a `setup.sh` bash script that automatically installed dependencies, pulled the correct Docker images, and seeded the local database with mock data. I then completely rewrote the repository README, replacing pages of manual instructions with a simple 3-step quickstart guide.

### Result
The next engineer we hired had their environment running in 20 minutes and pushed a minor bug fix on Day 1. The script became the standard onboarding tool for the entire engineering department.
