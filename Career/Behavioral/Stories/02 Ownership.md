---
type: star-story
story_id: 2
title: "Ownership — Microservice Restoration"
amazon_lps: ["Ownership"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
An internal notification microservice, built by an engineer who had left the company, went down quietly over a weekend, causing 500+ welcome emails to fail.

### Task
Although I was on the frontend team and this was a backend node service, nobody was actively owning it, and marketing was furious. I decided to take ownership of restoring and stabilizing it.

### Action
I dug into the undocumented codebase, found that an expired third-party API token was crashing the process, and updated it. More importantly, I realized there was no alerting. I took the initiative to containerize the service, add a /health endpoint, and integrate it with our Slack alerting channel using a basic Datadog webhook. I then wrote a runbook for it.

### Result
The service was restored before Monday morning. It never failed silently again. This incident actually sparked my interest in backend infrastructure and is a core reason I am transitioning to backend engineering.
