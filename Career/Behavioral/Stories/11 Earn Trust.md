---
type: star-story
story_id: 11
title: "Earn Trust — JWT Security Flaw"
amazon_lps: ["Earn Trust"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
I discovered a security flaw in how we were handling JWT tokens (storing them in LocalStorage instead of HttpOnly cookies) that exposed us to XSS attacks.

### Task
I had to convince a senior backend engineer, who originally designed the system, that his implementation was flawed.

### Action
Instead of calling him out in a public channel, I scheduled a private 1-on-1. I approached the conversation with respect, explaining that while the current setup was standard a few years ago, modern security standards had shifted. I presented a working PoC of how an XSS attack could steal the token, and then showed a PR with a proposed fix using secure cookies.

### Result
He appreciated the private heads-up and the fact that I brought a solution, not just a problem. We worked together to implement the fix, and he later advocated for my promotion because I handled the situation professionally.
