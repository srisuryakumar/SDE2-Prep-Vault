---
type: star-story
story_id: 1
title: "Customer Obsession — Dashboard Performance"
amazon_lps: ["Customer Obsession"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
At my current company, our customer support team was overwhelmed with tickets about our dashboard loading too slowly, causing users to abandon their workflows.

### Task
As a frontend engineer, I needed to identify the bottleneck and reduce load times without completely rewriting the backend API.

### Action
I instituted a performance tracking tool and discovered that a single massive JSON payload was blocking the main thread. Instead of just adding a loading spinner, I implemented a GraphQL-style field-filtering proxy layer in a Node.js BFF (Backend-for-Frontend) that only requested the exact fields needed for the initial view. I also added aggressive client-side caching for static taxonomy data.

### Result
Dashboard initial load time dropped from 4.2 seconds to 1.1 seconds. Customer support tickets regarding performance dropped by 80% within a week, and I learned that true customer obsession means fixing the root frustration, not just masking it with UI loaders.
