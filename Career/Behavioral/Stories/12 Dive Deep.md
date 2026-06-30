---
type: star-story
story_id: 12
title: "Dive Deep — Low-end Device Performance"
amazon_lps: ["Dive Deep"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
A small subset of users on older Android devices reported that our web app was completely unresponsive, but we couldn't reproduce it on our end.

### Task
I needed to find the root cause of a bug that only happened on specific low-end hardware.

### Action
I didn't just guess; I connected a low-end Android test device to Chrome remote debugging. I dug deep into the performance timeline and discovered that a regex used for input masking was causing catastrophic backtracking on certain inputs, locking up the single-threaded JS engine for up to 5 seconds on slow CPUs.

### Result
I rewrote the input masking logic to use standard string manipulation instead of complex regex. CPU utilization on low-end devices dropped by 95%, restoring full functionality for those users.
