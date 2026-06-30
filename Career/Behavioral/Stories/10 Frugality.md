---
type: star-story
story_id: 10
title: "Frugality — AWS Cost Reduction"
amazon_lps: ["Frugality"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
Our AWS bill was creeping up, and I noticed our staging environment was running 10 heavy EC2 instances 24/7.

### Task
As an engineer who cares about company resources, I wanted to cut unnecessary costs.

### Action
I wrote a simple AWS Lambda function triggered by EventBridge that automatically spun down the staging EC2 instances at 8 PM and spun them back up at 8 AM on weekdays, and kept them off completely on weekends. I also migrated our static assets from EC2 to S3 + CloudFront.

### Result
These small infrastructure changes reduced our monthly AWS staging bill by over 60%, saving the company roughly $1,500 a month with only 4 hours of my effort.
