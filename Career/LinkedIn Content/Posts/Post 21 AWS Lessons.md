---
type: linkedin-post
post_number: 21
scheduled_week: 11
scheduled_day: Tuesday
status: drafted
---
Deployed to AWS for the first time. Here's what I got wrong.

What I expected: click a few buttons, app runs in the cloud.

What actually happened:

Mistake 1: Opened port 22 to 0.0.0.0/0 in the security group.
Fix: restrict SSH to your IP only. 0.0.0.0/0 is an open door.

Mistake 2: Hard-coded database password in application.yml.
Fix: AWS Secrets Manager → Spring Boot reads at startup via env variable.

Mistake 3: RDS in a public subnet.
Fix: RDS belongs in a private subnet. Only the app server can reach it.

Mistake 4: No CloudWatch alarm on CPU.
Fix: Alert when CPU > 80% for 5 minutes. Caught a runaway query on day 2.

Mistake 5: Deployed with root-level IAM credentials.
Fix: Create an IAM role for the EC2 instance with only the permissions it needs.

The rule: the cloud is secure by default only if you make it insecure.
Every mistake above was a deliberate configuration choice I made wrong.

GitHub: [link to infrastructure notes in docs/]

#AWS #DevOps #BackendEngineering
